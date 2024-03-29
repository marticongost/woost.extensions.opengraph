"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail import schema
from woost.models import Item


class OpenGraphType(Item):

    members_order = [
        "title",
        "code",
        "category"
    ]

    title = schema.String(
        required = True,
        unique = True,
        translated = True,
        spellcheck = True,
        descriptive = True
    )

    code = schema.String(
        required = True,
        unique = True,
        indexed = True
    )

    category = schema.Reference(
        type = "woost.extensions.opengraph"
                ".opengraphcategory.OpenGraphCategory",
        required = True,
        bidirectional = True
    )

