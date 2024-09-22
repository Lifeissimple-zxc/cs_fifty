import logging

from django.http import HttpRequest
from django.shortcuts import render, redirect

from . import util, cache


logger = logging.getLogger('wiki')
ERROR_TEMPLATE = "encyclopedia/error.html"

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request: HttpRequest, title: str):
    raw_title = title
    # assumption: most titles are capitalised, all upper is a fall back scenario
    title = title.capitalize()
    if (markdown := util.get_entry(title=title)) is None:
        logger.warning("capitalised search did not work")
        title = title.upper()
        markdown = util.get_entry(title=title)
    if markdown is None:
        return render(
            request=request,
            template_name=ERROR_TEMPLATE,
            context={
                "title": raw_title,
                "error_message": f"Title page for '{raw_title}' was not found"
            }
        )

    markdown = util.markdown_to_html(title=raw_title, markdown=markdown)
    if markdown is None:
        return render(
            request=request,
            template_name=ERROR_TEMPLATE,
            context={
                "title": raw_title,
                "error_message": "Unexpected server error, please try again."
            }
        )
    
    logger.info("title pre rendering: %s", title)
    return render(
        request=request,
        template_name="encyclopedia/title.html",
        context={
            "title": title.upper(),
            "markdown": markdown
        }
    )

def random_entry(request: HttpRequest):
    return redirect(to=f"wiki/{cache.entries_cache.get_random_entry()}")

def search_entry(request: HttpRequest):
    if request.method != "POST":
        return render(
            request=request,
            template_name=ERROR_TEMPLATE,
            context={
                "title": "ERROR",
                "error_message": f"Request error: {request.method} method is not supported"
            }
        )
    # getting here means request has the right method
    q = request.POST["q"]
    if cache.entries_cache.has_entry(query=q):
        return redirect(to=f"wiki/{q}")
    
    # no full match was located so we try a partial one
    results = cache.entries_cache.find_entries(query=q)
    if not results:
        return render(
            request=request,
            template_name=ERROR_TEMPLATE,
            context={
                "title": f"Search: {q}",
                "error_message": f"No search results for \"{q}\"."
            }
        )
    # render search page
    return render(
        request=request,
        template_name="encyclopedia/search.html",
        context={
            "query": q,
            "entries": results
        }
    )
    
def _get_new_entry_form(request: HttpRequest):
    return render(request=request,
                  template_name="encyclopedia/new_title.html")

def new_entry(request: HttpRequest):
    if request.method == "GET":
        return _get_new_entry_form(request=request)