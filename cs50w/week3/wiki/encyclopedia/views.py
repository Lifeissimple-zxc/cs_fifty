from django.http import HttpRequest
from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request: HttpRequest, title: str):
    raw_title = title
    # assumption: most titles are capitalised, all upper is a fall back scenario
    title = title.capitalize()
    if (markdown := util.get_entry(title=title)) is None:
        print("capitalised search did not work")
        title = title.upper()
        markdown = util.get_entry(title=title)
    if markdown is None:
        return render(
            request=request,
            template_name="encyclopedia/error.html",
            context={
                "title": raw_title,
                "error_message": f"{raw_title} was not found"
            }
        )

    # convert markdown to html
    markdown = util.markdown_to_html(title=raw_title, markdown=markdown)
    # render info
    print("title pre rendering", title)
    return render(
        request=request,
        template_name="encyclopedia/title.html",
        context={
            "title": title.upper(),
            "markdown": markdown
        }
    )

