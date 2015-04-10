__author__ = 'fkint'
from flask import render_template


from .. import internal_site
from ....login import login_required
from ....utilities import pages


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
    return render_template("internal/pages/page.html",pagename=path,description=description, content_elements=content_elements)