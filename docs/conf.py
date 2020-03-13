import os
import sys
import re

import sphinx_rtd_theme as theme


# Import package to get version number
sys.path.insert(0, os.path.abspath('..'))
from rsgt import __version__ as rsgt_version

# Project information
project = 'rsgt'
version = re.match(r'[0-9]+\.[0-9]+', rsgt_version).group(0)
release = rsgt_version

# Sphinx configuration
extensions = ['sphinx.ext.autodoc']
autodoc_mock_imports = ['numpy']

html_theme = 'sphinx_rtd_theme'
html_theme_path = [theme.get_html_theme_path()]
html_theme_options = {'sticky_navigation': True}

html_use_index = False
html_show_copyright = False
html_copy_source = False
html_show_sourcelink = False
