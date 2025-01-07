# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys

# 添加项目根目录到 sys.path
sys.path.insert(0, os.path.abspath('../'))

project = 'cpu_data_fetch'
copyright = '2025, pj'
author = 'pj'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration


templates_path = ['_templates']
exclude_patterns = []

language = 'zh_CN'

extensions = [
    'sphinx.ext.autodoc',  # 用于生成模块文档
    'sphinx.ext.napoleon',  # 支持 Google 和 NumPy 风格的 docstring
    'sphinx.ext.viewcode',  # 添加源码链接
]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
