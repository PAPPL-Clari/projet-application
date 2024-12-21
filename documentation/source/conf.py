# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
sys.path.insert(0, os.path.abspath('../../code'))

project = 'Projet Application - Centrale Alumni'
copyright = '2024, Larissa ALBUQUERQUE, Clara MATTOS MEDEIROS'
author = 'Larissa ALBUQUERQUE, Clara MATTOS MEDEIROS'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    ]

templates_path = ['_templates']
exclude_patterns = []
autodoc_default_options = {
    'exclude-members': 'datetime'  # Substitua por qualquer nome de função ou módulo que você não queira documentar
}

language = 'fr'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']


autodoc_default_options = {
    'members': True,
    'undoc-members': True,  
    'special-members': '__init__',  
    'imported-members': True 
}

