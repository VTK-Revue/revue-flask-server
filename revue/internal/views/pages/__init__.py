__author__ = 'fkint'
from flask import render_template, request, redirect, url_for

from revue.internal.views import internal_site
from revue.utilities.login import login_required
from revue.utilities import pages
from forms import EditTextElementForm, CreatePageForm, EditPageForm
from revue.utilities.pages import save_page, create_page
from revue.models.pages import Page

@internal_site.route("/page/<int:id>", methods=['GET', 'POST'])
@login_required
def show_page_by_id(id):
    page = pages.get_page_by_id(id)
    return show_page(page)


@internal_site.route("/page/<path:path>", methods=['GET', 'POST'])
@login_required
def show_page_by_path(path):
    page = pages.get_page_by_path(path)
    return show_page(page)


@internal_site.route('/page', methods=['GET', 'POST'])
@login_required
def show_create_page():
    action = str(request.args.get("action", ""))
    if action == "create":
        form = CreatePageForm(request.form)
        if request.method == "POST":
            page = Page()
            form.populate_obj(page)
            create_page(page)
            return redirect(url_for('.show_page_by_id', id=page.id))
        return render_template("internal/pages/create_page.html", form=form)
    return redirect('/')


def show_page(page):
    if page is None:
        return render_template("404.html"), 404
    action = str(request.args.get('action', ''))
    if action == 'edit':
        form = EditPageForm(request.form, obj=page)
        if request.method == "POST":
            form.populate_obj(page)
            save_page(page)
        return render_edit_page(page, form)
    return render_page(page)


def render_page(page):
    content_elements = pages.get_content_elements(page)
    return render_template("internal/pages/page.html", page=page,
                           content_elements=content_elements)


def render_edit_page(page, form):
    return render_template("internal/pages/edit_page.html", form=form, page=page)


@internal_site.route("/content/<int:id>", methods=["GET", "POST"])
@login_required
def show_content(id):
    content_element = pages.get_content_element_by_id(id)
    action = str(request.args.get("action", ""))
    if action == "edit":
        return show_edit_content(content_element)
    return render_template("internal/pages/content_element_page.html", element=content_element)


def show_edit_text_element(text_element):
    form = EditTextElementForm(request.form, obj=text_element)
    return render_template("internal/pages/content/edit_text_element.html", element=text_element, form=form)


def save_text_element_content(text_element):
    # TODO: save text element content
    print("TODO: save text element content")


def save_content(content_element):
    # TODO: save updated content
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
