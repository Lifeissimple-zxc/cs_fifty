import logging

from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect

from . import util, cache


logger = logging.getLogger('wiki')
ERROR_TEMPLATE = "encyclopedia/error.html"
ERROR_TITLE = "Error"

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

    markdown = util.string_to_markdown(title=raw_title, markdown=markdown)
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
                "title": ERROR_TITLE,
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

def _post_new_entry_form(request: HttpRequest):
    try:
        title_name = request.POST["title_name"]
        title_content = request.POST["title_content"]
    except KeyError as e:
        return render(
            request=request,
            template_name=ERROR_TEMPLATE,
            context={
                "title": ERROR_TITLE,
                "error_message": f"Request is missing data: {e}"
            }
        )
    
    if cache.entries_cache.has_entry(query=title_name):
        return render(
            request=request,
            template_name=ERROR_TEMPLATE,
            context={
                "title": ERROR_TITLE,
                "error_message": f"\"{title_name}\" is an already existing title."
            }
        )
    
    # getting here means a new entry is being added
    md = util.string_to_markdown(title=title_name, markdown=title_content)
    if md is None:
        return render(
            request=request,
            template_name=ERROR_TEMPLATE,
            context={
                "title": ERROR_TITLE,
                "error_message": "Title content is not a valid piece of Markdown. Try Again."
            }
        )
    
    # at this point we know markdown is valid
    try:
        util.save_entry(title=title_name, content=title_content)
    except Exception as e:
        logger.error("error saving new title: %s", e, exc_info=True)
        return render(
            request=request,
            template_name=ERROR_TEMPLATE,
            context={
                "title": ERROR_TITLE,
                "error_message": "Unexpected server error while saving content. Try Again"
            }
        )
    
    # getting here means the title was saved ok so we can redirect its author there
    return redirect(to=f"wiki/{title_name}")

def new_entry(request: HttpRequest):
    if request.method == "GET":
        return _get_new_entry_form(request=request)
    elif request.method == "POST":
        return _post_new_entry_form(request=request)
    else:
        return render(
            request=request,
            template_name=ERROR_TEMPLATE,
            context={
                "title": ERROR_TITLE,
                "error_message": f"Request error: {request.method} method is not supported"
            }
        )