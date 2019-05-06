"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from woost.admin.sections import Settings
from woost.admin.sections.contentsection import ContentSection


class OpenGraphSettings(Settings):

    members = [
        "x_opengraph_fb_admins",
        "x_opengraph_fb_apps",
        "x_opengraph_default_image"
    ]


@when(ContentSection.declared)
def fill(e):
    e.source.append(OpenGraphSettings("opengraph"))

