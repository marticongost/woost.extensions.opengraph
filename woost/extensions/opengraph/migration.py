"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.persistence import migration_step, datastore
from woost.models import extensions_manager
from woost.models.migration import (
    rebuild_indexes_after_conversion_to_python3,
    create_admin
)


@migration_step(before=rebuild_indexes_after_conversion_to_python3)
def preserve_woost2_info(e):

    from woost.models import Configuration, Website, Publishable
    from .opengraphtype import OpenGraphType

    broken = datastore.root.get("woost2_broken_objects")
    ext_map = \
        broken and broken.get("woost.extensions.opengraph.OpenGraphExtension")
    ext = ext_map and ext_map.popitem()[1]

    if ext:

        # Must run before rebuild_indexes_after_conversion_to_python3, since
        # the index rebuilding can trigger the default value production for
        # Publication.x_opengraph_type, which in turn will attempt to obtain
        # a type by code.
        OpenGraphType.code.rebuild_index()

        def rename_attrib(obj, name, new_name=None):
            old_key = "_open_graph_" + name
            try:
                value = getattr(obj, old_key)
            except AttributeError:
                pass
            else:
                delattr(obj, old_key)
                new_key = "_x_opengraph_" + (new_name or name)
                setattr(obj, new_key, value)

        # Disable installation for the extension
        extensions_manager.set_installed("opengrah", True)

        for config in Configuration.select():
            rename_attrib(config, "default_image")
            if ext:
                config._x_opengraph_fb_admins = ext["_facebook_administrators"]
                config._x_opengraph_fb_apps = ext["_facebook_applications"]

        for website in Website.select():
            rename_attrib(website, "default_image")

        for pub in Publishable.select():
            rename_attrib(pub, "enabled")
            rename_attrib(pub, "type")


@migration_step(before=create_admin)
def fix_opengraph_type_references(e):

    from woost.models import Publishable
    from .opengraphtype import OpenGraphType

    for og_type in OpenGraphType.select():
        try:
            del og_type._Publishable_open_graph_type
        except AttributeError:
            pass

    for pub in Publishable.select():
        try:
            og_type = pub._x_opengraph_type
        except AttributeError:
            pass
        else:
            del pub._x_opengraph_type
            pub.x_opengraph_type = og_type

