"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.translations import translations
from woost.admin.sections import Settings
from woost.admin.sections.contentsection import ContentSection

translations.load_bundle("woost.extensions.opengraph.admin.sections")


class OpenGraphSettings(Settings):

    icon_uri = "woost.extensions.opengraph.admin.ui://images/opengraph.svg"

    members = [
        "x_opengraph_fb_admins",
        "x_opengraph_fb_apps",
        "x_opengraph_default_image"
    ]


@when(ContentSection.declared)
def fill(e):
    e.source.append(OpenGraphSettings("opengraph"))

