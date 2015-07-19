__author__ = 'fkint'
from flask import render_template, request, redirect, url_for

from revue import db

from revue.internal.views import internal_site
from revue.utilities.login import login_required
from revue.utilities.session import get_current_user_id
from revue.utilities import pages
from forms import EditTextElementForm, CreatePageForm, EditPageForm, CreateTextElementForm
from revue.utilities.pages import save_page, create_page
from revue.models.pages import Page, TextElement, PageContentElement, ContentElement

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
        return render_template("internal/pages/edit_page.html", form=form, page=page)
    elif action == 'add-content':
        return show_add_content(page)
    return render_page(page)


def render_page(page):
    content_elements = pages.get_content_elements(page)
    return render_template("internal/pages/page.html", page=page,
                           content_elements=content_elements)


def show_add_content(page):
    content_type = str(request.args.get('content_type', ''))
    if content_type == "text":
        form = CreateTextElementForm(request.form)
        if request.method == "POST":
            text_element = TextElement(form.content.data)
            form.populate_obj(text_element)
            text_element.author_id = get_current_user_id()
            db.session.add(text_element)
            db.session.commit()
            db.session.add(PageContentElement(text_element.id, page.id, 0))
            db.session.commit()
            return redirect(url_for('.show_page_by_id', id=page.id))
        return render_template("internal/pages/content/create_text_element.html", form=form)
    return render_template("404.html"), 404


@internal_site.route("/content/<int:id>", methods=["GET", "POST"])
@login_required
def show_content(id):
    content_element = pages.get_content_element_by_id(id)
    action = str(request.args.get("action", ""))
    if action == "edit":
        return show_edit_content(content_element)
    return render_template("internal/pages/content_element_page.html", element=content_element)


def show_edit_content(content_element):
    if content_element.type == "text":
        form = EditTextElementForm(request.form, obj=content_element)
        if request.method == "POST":
            form.populate_obj(content_element)
            db.session.commit()
        return render_template("internal/pages/content/edit_text_element.html", element=content_element, form=form, referring_page_id=request.args.get('referring_page_id', '#'))
    return render_template("internal/pages/content/edit_content_element.html", element=content_element)
