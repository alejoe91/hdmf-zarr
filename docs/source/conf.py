# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import sphinx_rtd_theme


# -- Support building doc without install --------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
# sys.path.insert(0, os.path.abspath('.'))

# Get the project root dir, which is the parent parent dir of this
cwd = os.getcwd()
project_root = os.path.dirname(os.path.dirname(cwd))

# Insert the project root dir as the first element in the PYTHONPATH.
# This lets us ensure that the source package is imported, and that its
# version is used.
sys.path.insert(0, os.path.join(project_root, 'src'))
from hdmf_zarr._version import get_versions


# -- Autodoc configuration -----------------------------------------------------
autoclass_content = 'both'
autodoc_docstring_signature = True
autodoc_member_order = 'bysource'


# -- Project information -----------------------------------------------------

project = 'hdmf_zarr'
copyright = '2022, Oliver Ruebel'
author = 'Oliver Ruebel'

# The short X.Y version.
version = '{}'.format(get_versions()['version'])
# The full version, including alpha/beta/rc tags.
release = '{}'.format(get_versions()['version'])

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.extlinks',
    'sphinx.ext.napoleon',
    'sphinx_gallery.gen_gallery',
]

# sphinx gallery setup
sphinx_gallery_conf = {
    # path to your examples scripts
    'examples_dirs': ['../gallery'],
    # path where to save gallery generated examples
    'gallery_dirs': ['tutorials'],
    'backreferences_dir': 'gen_modules/backreferences',
    'min_reported_time': 5,
    'remove_config_comments': True
}

intersphinx_mapping = {
    'python': ('https://docs.python.org/3.10', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'scipy': ('https://docs.scipy.org/doc/scipy/', None),
    'matplotlib': ('https://matplotlib.org/stable/', None),
    'h5py': ('https://docs.h5py.org/en/latest/', None),
    'pandas': ('https://pandas.pydata.org/pandas-docs/stable/', None),
    'hdmf': ('https://hdmf.readthedocs.io/en/stable/', None),
    'pynwb': ('https://pynwb.readthedocs.io/en/stable/', None),
    'zarr': ('https://zarr.readthedocs.io/en/stable/', None)
}

# Use this for mapping to external links
extlinks = {
    'pynwb-docs': ('https://pynwb.readthedocs.io/en/stable/', '%s'),
    'hdmf-docs': ('https://hdmf.readthedocs.io/en/stable/', '%s'),
    'zarr-docs': ('https://zarr.readthedocs.io/en/stable/', '%s')
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
# language = 'Python'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

html_theme_options = {
    'logo_only': False,  # Only show the hdmf-zarr logo without the documentation title
    'display_version': True,
    'prev_next_buttons_location': 'bottom',  # Show previous/next button at the bottom
    'style_external_links': True,  # Add marker to indicate external links
    'vcs_pageview_mode': '',
    # 'style_nav_header_background': '#0281b8',
    # Toc options
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = 'figures/logo_hdmf_zarr.png'

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
# html_favicon = 'figures/logo_hdmf_zarr_iconsize.png'


# The name of an image file (relative to this directory) to place at the top of
# the title page.
latex_logo = 'figures/logo_hdmf_zarr.pdf'


# -- sphinx extension ----------------------------------------------------

#
# see http://www.sphinx-doc.org/en/master/extdev/appapi.html
#

def run_apidoc(_):
    from sphinx.ext.apidoc import main as apidoc_main
    import os
    import sys
    out_dir = os.path.dirname(__file__)
    src_dir = os.path.join(out_dir, '../../src')
    sys.path.append(src_dir)
    apidoc_main(['-f', '-e', '--no-toc', '-o', out_dir, src_dir])


from abc import abstractproperty

def skip(app, what, name, obj, skip, options):
    if isinstance(obj, abstractproperty) or getattr(obj, '__isabstractmethod__', False):
        return False
    elif name == "__getitem__":
        return False
    return skip


def setup(app):
    app.connect('builder-inited', run_apidoc)
    app.add_css_file("theme_overrides.css")
    app.connect("autodoc-skip-member", skip)
