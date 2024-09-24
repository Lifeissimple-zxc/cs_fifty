import logging

from django.http import HttpRequest
from django.shortcuts import render, redirect
from django import forms

from . import util, cache


logger = logging.getLogger('wiki')
ERROR_TEMPLATE = "encyclopedia/error.html"
ERROR_TITLE = "Error"

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def _render_title_not_found_error(request: HttpRequest, title: str):
    return render(
        request=request,
        template_name=ERROR_TEMPLATE,
        content_type={
            "title": title,
            "error_message": f"Title page for '{title}' was not found" 
        }
    )

def _render_method_not_allowed_error(request: HttpRequest):
    return render(
        request=request,
        template_name=ERROR_TEMPLATE,
        context={
            "title": ERROR_TITLE,
            "error_message": f"Request error: {request.method} method is not supported for {request.path}"
        }
    )

def title(request: HttpRequest, title: str):
    if (markdown := util.fetch_entry(title=title)) is None:
        return _render_title_not_found_error(request=request, title=title)
    markdown = util.string_to_markdown(title=title, markdown=markdown)
    if markdown is None:
        return render(
            request=request,
            template_name=ERROR_TEMPLATE,
            context={
                "title": title,
                "error_message": "Unexpected server error, please try again."
            }
        )
    
    logger.info("title pre rendering: %s", title)
    return render(
        request=request,
        template_name="encyclopedia/title.html",
        context={
            "title": title,
            "markdown": markdown
        }
    )

def random_entry(request: HttpRequest):
    return redirect(to=f"wiki/{cache.entries_cache.get_random_entry()}")

def search_entry(request: HttpRequest):
    if request.method != "POST":
        return _render_method_not_allowed_error(request=request)
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


class NewTitleForm(forms.Form):
    title_name = forms.CharField(
        min_length=1,
        max_length=100,
        required=True,
        strip=True
    )
    title_content = forms.CharField(
        min_length=1,
        required=True,
        strip=True
    )


def _post_new_entry_form(request: HttpRequest):
    data = NewTitleForm(request.POST)
    if not data.is_valid():
        return render(
            request=request,
            template_name=ERROR_TEMPLATE,
            context={
                "title": ERROR_TITLE,
                "error_message": f"Request is missing data: {data.errors.as_text()}"
            }
        )
    
    if cache.entries_cache.has_entry(query=data.title_name):
        return render(
            request=request,
            template_name=ERROR_TEMPLATE,
            context={
                "title": ERROR_TITLE,
                "error_message": f"\"{data.title_name}\" is an already existing title."
            }
        )
    
    # getting here means a new entry is being added
    md = util.string_to_markdown(title=data.title_name, markdown=data.title_content)
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
        util.save_entry(title=data.title_name, content=data.title_content)
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
    return redirect(to=f"wiki/{data.title_name}")

def new_entry(request: HttpRequest):
    if request.method == "GET":
        return _get_new_entry_form(request=request)
    elif request.method == "POST":
        return _post_new_entry_form(request=request)
    else:
        return _render_method_not_allowed_error(request=request)

def _get_update_entry_page(request: HttpRequest, title: str):
    logger.info("update reuqest title: %s", title)
    if (markdown := util.fetch_entry(title=title)) is None:
        return _render_title_not_found_error(request=request, title=title)
    return render(
        request=request,
        template_name="encyclopedia/edit_title.html",
        context={
            "title": title,
            "markdown": markdown
        }
    )

def update_entry(request: HttpRequest, title: str):
    if request.method == "GET":
        logger.info("update path: %s", request.path)
        return _get_update_entry_page(request=request, title=title)
    # elif request.method == "POST":
    #     return
    else:
        return _render_method_not_allowed_error(request=request)