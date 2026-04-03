project = "wdatabricks"
copyright = "2024, William Steve Rodriguez Villamizar"
author = "William Steve Rodriguez Villamizar"
release = "1.0.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosummary",
    "sphinx.ext.extlinks",
    "sphinx.ext.graphviz",
    "sphinx.ext.mathjax",
]

extlinks = {
    "issue": ("https://github.com/wisrovi/wdatabricks/issues/%s", "Issue #%s"),
    "pr": ("https://github.com/wisrovi/wdatabricks/pulls/%s", "PR #%s"),
}

author = "William Steve Rodriguez Villamizar"
github_doc_root = "https://github.com/wisrovi/wdatabricks/tree/main/docs/"
github_root_url = "https://github.com/wisrovi/wdatabricks"
linkedin_url = "https://www.linkedin.com/in/william-steve-rodriguez-villamizar"

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "furo"
html_static_path = ["_static"]
html_title = "wdatabricks Documentation"

html_theme_options = {
    "source_repository": "https://github.com/wisrovi/wdatabricks",
    "source_repository_branch": "main",
    "footer_icons": [
        {
            "text": "wdatabricks v1.0.0",
            "url": "https://pypi.org/project/wdatabricks/",
            "class": "pypi",
        },
        {
            "text": "LinkedIn",
            "url": "https://www.linkedin.com/in/william-steve-rodriguez-villamizar",
            "class": "linkedin",
        },
    ],
    "navigation_depth": 3,
    "breadcrumb_parent_page_title": "Documentation",
}

autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": "__weakref__",
}

napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_type_aliases = {}

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "databricks": ("https://docs.databricks.com", None),
}
