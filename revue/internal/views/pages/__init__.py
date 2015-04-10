__author__ = 'fkint'
from flask import render_template, request


from revue.internal.views import internal_site
from revue.utilities.login import login_required
from revue.utilities import pages
from forms import EditTextElementForm


@internal_site.route("/page/<path:path>")
@login_required
def show_page(path):
    page = pages.get_page(path)
    description = "This page is not available. There might not exist a page with this url or you might " \
                  "not have the needed access permissions."
    content_elements = []
    if page is not None:
        description = page.description
        content_elements = pages.get_content_elements(page)
        print(content_elements)
        print([str(ce.content) for ce in content_elements])
    return render_template("internal/pages/page.html",pagename=path,description=description, content_elements=content_elements)


@internal_site.route("/content/<int:id>", methods=["GET", "POST"])
@login_required
def show_content(id):
    #content_element = pages.get_content_element(ContentElement.query.filter_by(id=id).first())
    #content_element = pages.
    content_element = pages.get_content_element_by_id(id)
    action = str(request.args.get("action", ""))
    if action == "edit":
        return show_edit_content(content_element)
    return render_template("internal/pages/content_element_page.html", element=content_element)


def show_edit_text_element(text_element):
    form = EditTextElementForm(request.form,obj=text_element)
    return render_template("internal/pages/content/edit_text_element.html", element=text_element,form=form)


def save_text_element_content(text_element):
    #TODO: save text element content
    print("TODO: save text element content")


def save_content(content_element):
    #TODO: save updated content
    if content_element.type == "text":
        save_text_element_content(content_element)
    else:
        print("TODO: save updated content for " + content_element.type)


def show_edit_content(content_element):
    if request.method == "POST":
        save_content(content_element)
    if content_element.type == "text":
        return show_edit_text_element(content_element)

    return render_template("internal/pages/content/edit_content_element.html", element=content_element)