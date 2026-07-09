import datetime
import os
import textwrap

# Configuration for the Sphinx documentation builder.
# All configuration specific to your project should be done in this file.
#
# If you're new to Sphinx and don't want any advanced or custom features,
# just go through the items marked 'TODO'.
#
# A complete list of built-in Sphinx configuration values:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
#
# The Sphinx Stack uses the Canonical Sphinx theme to keep all documentation consistent
# and on brand:
# https://github.com/canonical/canonical-sphinx

#######################
# Project information #
#######################

# Project name
# TODO: Update with the official name of your project or product (e.g., "Ubuntu Server")
project = "Robotics"

# Author name; used in the default copyright statement in the page footer
author = "Canonical Ltd."

# The year in the copyright statement
copyright = f"{datetime.date.today().year} CC-BY-SA, {author}"

# Sidebar documentation title
# To disable the title, set it to an empty string.
html_title = project + " documentation"

# Documentation website URL
ogp_site_url = os.environ.get(
    "READTHEDOCS_CANONICAL_URL", "https://canonical-robotics.readthedocs-hosted.com/"
)

# Preview name of the documentation website
# TODO: To use a different name for the project in previews, update the next line.
ogp_site_name = project

# Preview image URL
# TODO: To customise the preview image, update the next line.
ogp_image = "https://assets.ubuntu.com/v1/cc828679-docs_illustration.svg"

# Product favicon; shown in bookmarks, browser tabs, etc.
# TODO: To customise the favicon, uncomment and update the next line.
# html_favicon = "_static/favicon.png"

# Dictionary of values to pass into the Sphinx context for all pages:
# https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_context
html_context = {
    # Product page URL; can be different from product docs URL
    # TODO: Change to your product website URL, dropping the 'https://' prefix (e.g.,
    #       'ubuntu.com/lxd'). If there's no such website, remove the {{ product_page }}
    #       link from the _templates/header.html file.
    "product_page": "ubuntu.com/robotics",
    # Product tag image; the orange part of your logo, shown in the page header
    # TODO: To add a tag image, uncomment and update as needed.
    # 'product_tag': '_static/tag.png',
    # Your Discourse instance URL
    # TODO: Change to your Discourse instance URL or leave empty.
    "discourse": "https://discourse.ubuntu.com",
    # Your Mattermost channel URL
    # TODO: Change to your Mattermost channel URL or leave empty.
    "mattermost": "https://chat.canonical.com/canonical/channels/documentation",
    # Your Matrix channel URL
    # TODO: Change to your Matrix channel URL or leave empty.
    "matrix": "https://matrix.to/#/#documentation:ubuntu.com",
    # Your documentation GitHub repository URL If set, links for viewing the
    # documentation source files and creating GitHub issues are added at the bottom of
    # each page.
    # TODO: Change to your documentation GitHub repository URL or leave empty.
    "github_url": "https://github.com/canonical/robotics_documentation/",
    # Docs branch in the repo; used in links for viewing the source files
    "repo_default_branch": "main",
    # Docs location in the repo; used in links for viewing the source files
    "repo_folder": "/docs/",
    # TODO: To enable or disable the Previous / Next buttons at the bottom of pages
    # Valid options: none, prev, next, both
    "sequential_nav": "both",
    # TODO: To enable listing contributors on individual pages, set to True
    "display_contributors": False,
    # Required for feedback button
    "github_issues": "enabled",
    # Passes the top-level 'author' value to the theme
    "author": author,
    # Documentation license information
    "license": {
        # TODO: Specify your project's license.
        # For the name, we recommend using the standard shorthand identifier from
        # https://spdx.org/licenses
        "name": "CC-BY-SA",
        # TODO: Link directly to your project's license statement.
        "url": "",
    },
}

# TODO: To enable the edit button on pages, uncomment and change the link to a
# public repository on GitHub or Launchpad. Any of the following link domains
# are accepted:
# - https://github.com/example-org/example"
# - https://launchpad.net/example
# - https://git.launchpad.net/example
#
# html_theme_options = {
# 'source_edit_link': 'https://github.com/canonical/sphinx-stack',
# }

# Project slug
# TODO: If your documentation is hosted on https://documentation.ubuntu.com/,
#       uncomment and set to the RTD slug.
# slug = ''

#######################
# Sitemap configuration: https://sphinx-sitemap.readthedocs.io/
#######################

# Use RTD canonical URL to ensure duplicate pages have a specific canonical URL
html_baseurl = os.environ.get("READTHEDOCS_CANONICAL_URL", "/")

# sphinx-sitemap uses html_baseurl to generate the full URL for each page:
sitemap_url_scheme = "{link}"

# Include `lastmod` dates in the sitemap:
sitemap_show_lastmod = True

# TODO: Exclude pages that aren't user-facing from the sitemap (e.g., module pages
# generated by autodoc).
# Pages excluded from the sitemap:
sitemap_excludes = [
    "404/",
    "genindex/",
    "search/",
]

################################
# Template and asset locations #
################################

html_static_path = ["_static"]
templates_path = ["_templates"]

#############
# Redirects #
#############

# To set up redirects: https://documatt.gitlab.io/sphinx-reredirects/usage.html
# For example: 'explanation/old-name.html': '../how-to/prettify.html',

# To set up redirects in the Read the Docs project dashboard:
# https://docs.readthedocs.io/en/stable/guides/redirects.html

# Known divergence from upstream sphinx-stack template:
# keep using the existing in-repo redirects mapping with sphinx-reredirects
# (inline ``redirects`` dict) rather than sphinx-rerediraffe + redirects.txt.
# Preserve this during future template updates unless intentionally migrating.

redirects = {
    # The migration from Discourse to ReadTheDoc stripped the 'docs/' prefix
    "docs/tutorials/": "../../tutorials/",
    "docs/tutorials/snapcraft/": "../../../tutorials/snapcraft/",
    "docs/tutorials/packaging-ros-application-as-snap/": "../../../tutorials/packaging-ros-application-as-snap/",
    "docs/tutorials/packaging-complex-robotics-software-with-snaps/": "../../../tutorials/packaging-complex-robotics-software-with-snaps/",
    "docs/tutorials/distribute-ros-apps-with-snap-store/": "../../../tutorials/distribute-ros-apps-with-snap-store/",
    "docs/tutorials/building-ros-snaps-with-content-sharing/": "../../../tutorials/building-ros-snaps-with-content-sharing/",
    "docs/tutorials/create-ubuntu-core-image-for-turtlebot3/": "../../../tutorials/create-ubuntu-core-image-for-turtlebot3/",
    "docs/tutorials/ubuntu-pro/ros-esm-intro/": "../../../../tutorials/ubuntu-pro/ros-esm-intro/",
    "docs/how-to-guides/": "../../how-to-guides/",
    "docs/how-to-guides/packaging/build-and-publish-snap-with-github-actions/": "../../../../how-to-guides/packaging/build-and-publish-snap-with-github-actions/",
    "docs/how-to-guides/packaging/migrate_from_docker_to_snap": "../../../../how-to-guides/packaging/migrate_from_docker_to_snap",
    "docs/how-to-guides/packaging/ros-2-shared-memory-in-snaps": "../../../../how-to-guides/packaging/ros-2-shared-memory-in-snaps",
    "docs/how-to-guides/packaging/ros-distributions-with-no-extensions/": "../../../../how-to-guides/packaging/ros-distributions-with-no-extensions/",
    "docs/how-to-guides/packaging/config-a-snap-pull-from-a-server.html": "../../../../how-to-guides/packaging/config-a-snap-pull-from-a-server.html",
    "docs/how-to-guides/packaging/config-a-snap-using-content-snap": "../../../../how-to-guides/packaging/config-a-snap-using-content-snap/",
    "docs/how-to-guides/packaging/config-a-snap-make-config-overwritable": "../../../../how-to-guides/packaging/config-a-snap-make-config-overwritable/",
    "docs/references/snapcraft/": "../../../references/snapcraft/",
    "docs/references/plugins/": "../../../references/plugins/",
    "docs/references/extensions/": "../../../references/extensions/",
    "docs/references/faq/": "../../../references/faq/",
    "docs/explanations/": "../../explanations/",
    "docs/explanations/ubuntu-core/": "../../../explanations/ubuntu-core/",
    "docs/explanations/security/securing-ros-robotic-platforms/": "../../../../explanations/security/securing-ros-robotic-platforms/",
    "docs/explanations/snaps/ros-architectures-with-snaps/": "../../../../explanations/snaps/ros-architectures-with-snaps/",
    "docs/explanations/snaps/identify-functionalities-and-apps-of-robotics-snap/": "../../../../explanations/snaps/identify-functionalities-and-apps-of-robotics-snap/",
    "docs/explanations/snaps/snap-configurations-and-hooks/": "../../../../explanations/snaps/snap-configurations-and-hooks/",
    "docs/explanations/snaps/snap-data-and-file-storage/": "../../../../explanations/snaps/snap-data-and-file-storage/",
    "docs/explanations/snaps/snap-environment-variables/": "../../../../explanations/snaps/snap-environment-variables/",
    "docs/explanations/snaps/application-orchestration/": "../../../../explanations/snaps/application-orchestration/",
    "docs/explanations/snaps/vcstool-and-rosinstall-file/": "../../../../explanations/snaps/vcstool-and-rosinstall-file/",
    "docs/explanations/snaps/debug-the-build-of-a-snap/": "../../../../explanations/snaps/debug-the-build-of-a-snap/",
    "docs/explanations/snaps/debug-a-snap-application/": "../../../../explanations/snaps/debug-a-snap-application/",
    "docs/explanations/iot-app-store/": "https://ubuntu.com/internet-of-things/appstore/docs/",
    "docs/explanations/dedicated-snap-store/": "https://ubuntu.com/internet-of-things/appstore/docs/",
    # The snaps/core tutorials were moved to a subfolder
    "tutorials/snapcraft/": "../../tutorials/snaps-core/",
    "tutorials/packaging-ros-application-as-snap/": "../../tutorials/snaps-core/packaging-ros-application-as-snap/",
    "tutorials/packaging-complex-robotics-software-with-snaps/": "../../tutorials/snaps-core/packaging-complex-robotics-software-with-snaps/",
    "tutorials/distribute-ros-apps-with-snap-store/": "../../tutorials/snaps-core/distribute-ros-apps-with-snap-store/",
    "tutorials/building-ros-snaps-with-content-sharing/": "../../tutorials/snaps-core/building-ros-snaps-with-content-sharing/",
    "tutorials/create-ubuntu-core-image-for-turtlebot3/": "../../tutorials/snaps-core/create-ubuntu-core-image-for-turtlebot3/",
    # These intermediate pages were removed
    "tutorials/ubuntu-pro/": "../../tutorials/ubuntu-pro/ros-esm-intro/",
    "explanations/iot-app-store/": "https://ubuntu.com/internet-of-things/appstore/docs/",
    "explanations/dedicated-snap-store/": "https://ubuntu.com/internet-of-things/appstore/docs/",
    # The snapcraft references were moved to a subfolder
    "references/plugins/": "../../references/snapcraft/plugins/",
    "references/extensions/": "../../references/snapcraft/extensions/",
    # The unique ESM tutorial was broken down into how-tos & explanations
    "tutorials/ubuntu-pro/ros-esm-intro/": "../../../explanations/security/what-is-ros-esm/",
    "explanations/security/securing-ros-robotic-platforms/": "../../../how-to-guides/security/hardening-your-robot/",
    "explanations/security/hardening-your-robot/": "../../../how-to-guides/security/hardening-your-robot/",
}


############################
# sphinx-llm configuration #
############################

# This description is included in llms.txt to provide some initial context for your
# product docs.
# TODO: Add a description in the form "This is the documentation for <product name>,
# <first sentence of home page>".
llms_txt_description = textwrap.dedent(
    """\
    This is the documentation for Ubuntu Robotics, covering the Ubuntu Robotics
    stack, packaging, deployment, operations, and reference material for
    maintainers and users.
    """
)

# The base URL for references built by sphinx-markdown-builder.
if os.environ.get("READTHEDOCS"):
    markdown_http_base = html_baseurl

###########################
# Link checker exceptions #
###########################

# A regex list of URLs that are ignored by 'make linkcheck'
linkcheck_ignore = [
    "http://127.0.0.1:8000",
    r"https://developer\.hashicorp\.com/terraform.*",
    "https://linux.die.net/man/1/curl",
]

# A regex list of URLs where anchors are ignored by 'make linkcheck'
linkcheck_anchors_ignore_for_url = [
    r"https://github\.com/.*",
    # Ignore the get-in-touch anchor
    r"https://ubuntu\.com/robotics$",
    r"https://ubuntu\.com/robotics/ros-esm$",
    r"https://ubuntu\.com/core/features/secure-boot$",
    r"https://www.ros.org/.*",
]

# How long the link checker will wait for a response for each request
# TODO: Decrease to improve run time or increase if links frequently time out.
# linkcheck_timeout = 30

# Give linkcheck multiple tries on failure
linkcheck_retries = 3
linkcheck_workers = 1

########################
# Configuration extras #
########################

# Custom MyST syntax extensions; see
# https://myst-parser.readthedocs.io/en/latest/syntax/optional.html
# NOTE: By default, the following MyST extensions are enabled:
#   - substitution
#   - deflist
#   - linkify
# myst_enable_extensions = set()

# Custom Sphinx extensions; see
# https://www.sphinx-doc.org/en/master/usage/extensions/index.html
extensions = [
    "canonical_sphinx",
    "notfound.extension",
    "sphinx_design",
    "sphinx_reredirects",
    "sphinx_tabs.tabs",
    "sphinxcontrib.jquery",
    "sphinxext.opengraph",
    "sphinx_config_options",
    "sphinx_contributor_listing",
    "sphinx_filtered_toctree",
    "sphinx_llm.txt",
    "sphinx_related_links",
    "sphinx_roles",
    "sphinx_terminal",
    "sphinx_ubuntu_images",
    "sphinx_youtube_links",
    "sphinxcontrib.cairosvgconverter",
    "sphinx_last_updated_by_git",
    "sphinx.ext.intersphinx",
    "sphinx_sitemap",
    "sphinxcontrib.mermaid",
]

# Excludes files or directories from processing
exclude_patterns = [
    "doc-cheat-sheet*",
    "content",
    ".venv*",
]

# Adds custom CSS files, located remotely or in 'html_static_path'.
html_css_files = [
    "cookie-banner.css",
]

# Adds custom JavaScript files, located remotely or in 'html_static_path'.
html_js_files = [
    "bundle.js",
]

# Appends extra markup to the end of every document written in reST
rst_epilog = """
.. include:: /reuse/links.txt
"""

# Feedback button at the top; enabled by default
# TODO: Disable the button if your project is unsuitable for public feedback.
# disable_feedback_button = True

# Your manpage URL
# TODO: To enable manpage links, uncomment and replace {codename} with required
#       release, preferably an LTS release (e.g. noble). Do *not* substitute
#       {section} or {page}; these will be replaced by sphinx at build time
#
# NOTE: If set, adding ':manpage:' to an .rst file
#       adds a link to the corresponding man section at the bottom of the page.
# manpages_url = 'https://manpages.ubuntu.com/manpages/{codename}/en/' + \
#     'man{section}/{page}.{section}.html'

# Specifies a reST snippet to be prepended to each .rst file
# This defines a :center: role that centers table cell content.
# This defines a :h2: role that styles content for use with PDF generation.
rst_prolog = """
.. role:: center
   :class: align-center
.. role:: h2
    :class: hclass2
.. role:: woke-ignore
    :class: woke-ignore
.. role:: vale-ignore
    :class: vale-ignore

"""

# Workaround for https://github.com/canonical/canonical-sphinx/issues/34
if "discourse_prefix" not in html_context and "discourse" in html_context:
    html_context["discourse_prefix"] = html_context["discourse"] + "/t/"


myst_heading_anchors = 2

myst_substitutions = {"COS_ROB": "COS for robotics", "COS": "COS Lite"}

# Configuration for Intersphinx projects
#
# intersphinx_mapping = {
#     "snap": ("https://snapcraft.io/docs/", None),
# }
