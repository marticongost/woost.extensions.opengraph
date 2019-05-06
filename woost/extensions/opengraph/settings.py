"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail import schema
from cocktail.translations import translations
from woost.models import add_setting, File

translations.load_bundle("woost.extensions.opengraph.settings")

add_setting(
    schema.String(
        "x_opengraph_fb_admins"
    )
)

add_setting(
    schema.String(
        "x_opengraph_fb_apps"
    )
)

add_setting(
    schema.Reference(
        "x_opengraph_default_image",
        type = File,
        relation_constraints = {"resource_type": "image"}
    )
)

