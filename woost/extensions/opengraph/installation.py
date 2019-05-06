"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from woost.models import ExtensionAssets, rendering
from .opengraphcategory import OpenGraphCategory
from .opengraphtype import OpenGraphType


def install():
    """Creates the assets required by the opengraph extension."""

    assets = ExtensionAssets("opengraph")

    # 'facebook' image renderer
    assets.require(
        rendering.ImageFactory,
        "image_factory",
        title = assets.TRANSLATIONS,
        identifier = "facebook",
        effects = [
            rendering.Fill(
                width = "200",
                height = "200"
            ),
            rendering.Align(
                width = "200",
                height = "200",
                background = "fff"
            )
        ]
    )

    # OpenGraph categories
    for category_id, type_ids in (
        ("activities", (
            "activity",
            "sport"
        )),
        ("businesses", (
            "bar",
            "company",
            "cafe",
            "hotel",
            "restaurant"
        )),
        ("groups", (
            "cause",
            "sports_league",
            "sports_team"
        )),
        ("organizations", (
            "band",
            "government",
            "non_profit",
            "school",
            "university"
        )),
        ("people", (
            "actor",
            "athlete",
            "author",
            "director",
            "musician",
            "politician",
            "profile",
            "public_figure"
        )),
        ("places", (
            "city",
            "country",
            "landmark",
            "state_province"
        )),
        ("products_and_entertainment", (
            "album",
            "book",
            "drink",
            "food",
            "game",
            "movie",
            "product",
            "song",
            "tv_show"
        )),
        ("websites", (
            "article",
            "blog",
            "website"
        ))
    ):
        og_category = assets.require(
            OpenGraphCategory,
            f"categories.{category_id}",
            title = assets.TRANSLATIONS,
            code = category_id,
            types = [
                assets.require(
                    OpenGraphType,
                    f"types.{type_id}",
                    title = assets.TRANSLATIONS,
                    code = type_id,
                )
                for type_id in type_ids
            ]
        )

