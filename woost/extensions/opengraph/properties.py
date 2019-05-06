"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from woost.models import Configuration


def get_global_properties():

    properties = {}
    config = Configuration.instance

    site_name = config.get_setting("site_name")
    if site_name:
        properties["og:site_name"] = site_name

    logo = (
        config.get_setting("x_opengraph_default_image")
        or config.get_setting("logo")
    )
    if logo:
        properties["og:image"] = logo.get_image_uri("facebook", host = "!")

    email = config.get_setting("email")
    if email:
        properties["og:email"] = email

    fb_admins = config.get_setting("x_opengraph_fb_admins")
    if fb_admins:
        properties["fb:admins"] = fb_admins

    fb_apps = config.get_setting("x_opengraph_fb_apps")
    if fb_apps:
        properties["fb:app_id"] = fb_apps

    return properties


def get_properties(publishable):
    properties = get_global_properties()
    properties.update(publishable.x_opengraph_get_properties())
    return properties

