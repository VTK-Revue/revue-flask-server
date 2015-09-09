from flask import render_template, request, redirect, url_for

from revue.internal.views import internal_site
from revue.utilities.login import login_required
from revue.utilities import pages
from .forms import EditTextElementForm, CreatePageForm, EditPageForm, CreateTextElementForm


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


def show_page(page):
    if page is None:
        return render_template("../../templates/internal/404.html"), 404
    action = str(request.args.get('action', ''))
    if action == 'edit':
        form = EditPageForm(request.form, obj=page)
        if request.method == "POST":
            pages.save_page(page, form)
        return render_template("internal/pages/edit_page.html", form=form, page=page)
    elif action == 'add-content':
        return show_add_content(page)
    content_elements = pages.get_content_elements(page)
    return render_template("internal/pages/page.html", page=page,
                           content_elements=content_elements)


@internal_site.route('/page', methods=['GET', 'POST'])
@login_required
def show_create_page():
    action = str(request.args.get("action", ""))
    if action == "create":
        form = CreatePageForm(request.form)
        if request.method == "POST":
            page = pages.create_page(form)
            if page is not None:
                return redirect(url_for('.show_page_by_id', id=page.id))
        return render_template("internal/pages/create_page.html", form=form)
    return redirect('/')


@internal_site.route("/content/<int:id>", methods=["GET", "POST"])
@login_required
def show_content(id):
    content_element = pages.get_content_element_by_id(id)
    action = str(request.args.get("action", ""))
    if action == "edit":
        return show_edit_content(content_element)
    return render_template("internal/pages/content_element_page.html", element=content_element)


def show_add_content(page):
    content_type = str(request.args.get('content_type', ''))
    if content_type == "text":
        form = CreateTextElementForm(request.form)
        if request.method == "POST":
            if pages.create_text_element_for_page(form, page):
                return redirect(url_for('.show_page_by_id', id=page.id))
        return render_template("internal/pages/content/create_text_element.html", form=form)
    return render_template("../../templates/internal/404.html"), 404


def show_edit_content(content_element):
    if content_element.type == "text":
        form = EditTextElementForm(request.form, obj=content_element)
        if request.method == "POST":
            pages.save_content(content_element, form)
        return render_template("internal/pages/content/edit_text_element.html", element=content_element, form=form,
                               referring_page_id=request.args.get('referring_page_id', '#'))
    return render_template("internal/pages/content/edit_content_element.html", element=content_element)
