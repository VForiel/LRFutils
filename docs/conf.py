"""Sphinx configuration of the LRFutils documentation."""

import sys
from importlib.metadata import version as package_version
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

project = "LRFutils"
copyright = "2022-2026, Vincent Foriel"
author = "Vincent Foriel"
release = package_version("LRFutils")
extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]
source_suffix = {".md": "markdown"}
exclude_patterns = ["_build"]
templates_path = ["_templates"]
autodoc_member_order = "bysource"
autodoc_typehints = "description"
napoleon_use_rtype = False
myst_heading_anchors = 3
myst_enable_extensions = ["colon_fence", "deflist"]

SPONSOR_URL = "https://github.com/sponsors/VForiel"

html_theme = "breeze"
html_title = "LRFutils"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_logo = "_static/logo.png"
html_favicon = "_static/logo.png"
html_context = {
    "github_user": "VForiel",
    "github_repo": "LRFutils",
    "github_version": "main",
    "doc_path": "docs",
    "sponsor_url": SPONSOR_URL,
}
html_theme_options = {
    "emojis_header_nav": True,
    "emojis_sidebar_nav": True,
    "emojis_sidebar_toc": True,
    "external_links": [
        {"url": SPONSOR_URL, "name": "Sponsor LRFutils", "icon": "heart"},
        {"url": "https://github.com/VForiel/LRFutils", "name": "GitHub"},
        {"url": "https://pypi.org/project/LRFutils/", "name": "PyPI"},
    ],
    "sidebar_secondary": "sidebar-toc.html, sponsor.html, repo-stats.html, edit-this-page.html",
}
