# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Voyagers Restoration Codex'
copyright = '2025, Hawk Eye / Omniversal Media, LLC'
author = 'Hawk Eye / Omniversal Media, LLC'
release = '2025'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['myst_parser', 'sphinx.ext.autodoc']

html_baseurl = "https://sphinxguardian.com/"

myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "dollarmath",
    "html_admonition",
    "html_image",
]

myst_heading_anchors = 2
myst_all_links_external = True
myst_links_external_new_tab = True

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}
templates_path = ['_templates']
# Exclude the large collection of individual fragments used during the
# conversion of Voyagers Volume II.  Without this exclusion Sphinx will
# treat each fragment as an orphan page, which can slow down the build
# and clutter the output.  We refer to the volume via a single
# chaptered document instead.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '**/.ipynb_checkpoints/*',
                    'voyagers_2/*']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'

html_theme_options = {
    "light_logo": "logo-light.png",
    "dark_logo": "logo-dark.png"
}

html_static_path = ['_static']
