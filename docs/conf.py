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
autodoc_member_order = "bysource"
myst_heading_anchors = 3
html_theme = "breeze"
html_title = "LRFutils"
html_static_path = ["_static"]
html_logo = "_static/logo.png"
html_favicon = "_static/logo.png"
html_context = {"github_user": "VForiel", "github_repo": "LRFutils", "github_version": "main", "doc_path": "docs"}
