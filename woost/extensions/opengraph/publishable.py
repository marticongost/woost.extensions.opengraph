"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail import schema
from cocktail.translations import translations
from cocktail.html.datadisplay import display_factory
from cocktail.html.grouping import GroupByMember
from woost.models import Publishable, Document, News, File
from woost.extensions.opengraph.opengraphtype import OpenGraphType
from woost.extensions.opengraph.utils import (
    export_content,
    get_publishable_website
)

translations.load_bundle("woost.extensions.opengraph.publishable")

File.default_x_opengraph_enabled = False
File.default_x_opengraph_type = None

Publishable.members_order += [
    "x_opengraph_enabled",
    "x_opengraph_type"
]


class GroupByOpenGraphCategory(GroupByMember):
    member = OpenGraphType.category


Publishable.add_member(
    schema.Boolean("x_opengraph_enabled",
        required = True,
        default = True,
        listed_by_default = False,
        member_group = "meta.x_opengraph"
    )
)

Publishable.add_member(
    schema.Reference("x_opengraph_type",
        type = OpenGraphType,
        required = Publishable["x_opengraph_enabled"],
        related_end = schema.Collection(
            block_delete = True
        ),
        default = schema.DynamicDefault(
            lambda: OpenGraphType.get_instance(code = "article")
        ),
        indexed = True,
        listed_by_default = False,
        member_group = "meta.x_opengraph"
    )
)

def _get_publishable_properties(self):

    properties = {
        "og:title": translations(self),
        "og:type": self.x_opengraph_type.code,
        "og:url": self.get_uri(host = "!")
    }

    description = self.x_opengraph_get_description()
    if description:
        properties["og:description"] = description

    image = self.x_opengraph_get_image()
    if image:
        if isinstance(image, Publishable):
            if image.is_accessible():
                image = image.get_image_uri("facebook", host = "!")
            else:
                image = None

        if image:
            properties["og:image"] = image

    video = self.x_opengraph_get_video()
    if video:
        if isinstance(video, Publishable):
            video = video.get_uri(host = "!")
        properties["og:video"] = video

    return properties

Publishable.x_opengraph_get_properties = _get_publishable_properties

def _get_publishable_description(self):
    website = get_publishable_website(self)
    if website:
        return website.description

Publishable.x_opengraph_get_description = _get_publishable_description

def _get_document_description(self):
    if self.description:
        return export_content(self.description)

    return Publishable.x_opengraph_get_description(self)

Document.x_opengraph_get_description = _get_document_description

def _get_news_description(self):

    if self.summary:
        return export_content(self.summary)

    return Document.x_opengraph_get_description(self)

News.x_opengraph_get_description = _get_news_description

def _get_publishable_open_graph_image(self):
    return self.get_representative_image()

Publishable.x_opengraph_get_image = _get_publishable_open_graph_image

def _get_publishable_open_graph_video(self):
    return None

Publishable.x_opengraph_get_video = _get_publishable_open_graph_video

