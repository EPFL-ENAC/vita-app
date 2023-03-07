# Configuration file for the Sphinx documentation builder.

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys

sys.path.insert(0, os.path.abspath(".."))


# -- Project information

project = "VITA'App"
copyright = "2023 EPFL (École Polytechnique Fédérale de Lausanne)"
author = "Son Pham-Ba"

# -- General configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.extlinks",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]


templates_path = ["_templates"]

# -- Options for HTML output

html_theme = "sphinx_book_theme"

# -- Options for EPUB output
epub_show_urls = "footnote"


# -- Automatically run apidoc to generate rst from code
# https://github.com/readthedocs/readthedocs.org/issues/1139
def run_apidoc(_):
    from sphinx.ext.apidoc import main

    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    cur_dir = os.path.abspath(os.path.dirname(__file__))
    module = os.path.join(cur_dir, "..")
    output = os.path.join(cur_dir, "source")
    main(["-e", "-f", "-o", output, module])


def setup(app):
    app.connect("builder-inited", run_apidoc)
