from typing import TYPE_CHECKING
from flask import render_template
# from flask import redirect
# from jembe import page_url

if TYPE_CHECKING:
    from flask import Flask


def init_views(app: "Flask"):
    """Flask regular routes unrelated to Jembe pages"""

    @app.route("/")
    def index():
        """Servers intex.html"""
        return render_template("index.html")
        # # redirectd to projects page
        # return redirect(page_url("/projects"))
