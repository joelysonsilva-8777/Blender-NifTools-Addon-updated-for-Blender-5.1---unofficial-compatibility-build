"""Aurakingdom workflow helper properties."""

import bpy
from bpy.types import PropertyGroup

from io_scene_niftools.utils.decorators import register_classes, unregister_classes


def _mark_model_cache_dirty(self, context):
    try:
        self.model_items.clear()
    except AttributeError:
        pass
    self.model_count = 0
    self.model_dir_cache = ""
    self.model_file = ""
    self.status = "Model list needs refresh."


class AurakingdomModelItem(PropertyGroup):
    file_name: bpy.props.StringProperty(
        name="File",
        options={'HIDDEN', 'SKIP_SAVE'},
    )


class AurakingdomHelper(PropertyGroup):
    model_dir: bpy.props.StringProperty(
        name="Models",
        subtype='DIR_PATH',
        description="Folder containing .nif model files",
        update=_mark_model_cache_dirty,
    )
    texture_dir: bpy.props.StringProperty(
        name="Textures",
        subtype='DIR_PATH',
        description="Folder containing texture files",
    )
    animation_dir: bpy.props.StringProperty(
        name="Animations",
        subtype='DIR_PATH',
        description="Folder containing .kf animation files",
    )
    export_dir: bpy.props.StringProperty(
        name="Export",
        subtype='DIR_PATH',
        description="Folder where helper exports are written",
    )
    model_file: bpy.props.StringProperty(
        name="Model",
        description="Model file to import from the model folder",
    )
    model_items: bpy.props.CollectionProperty(
        type=AurakingdomModelItem,
        options={'HIDDEN', 'SKIP_SAVE'},
    )
    model_count: bpy.props.IntProperty(
        name="Models",
        default=0,
        options={'HIDDEN', 'SKIP_SAVE'},
    )
    model_dir_cache: bpy.props.StringProperty(
        name="Cached Model Folder",
        options={'HIDDEN', 'SKIP_SAVE'},
    )
    export_name: bpy.props.StringProperty(
        name="Name",
        description="Export file name without extension",
    )
    import_animation: bpy.props.BoolProperty(
        name="Import KF",
        description="Import a matching .kf animation from the animation folder",
        default=True,
    )
    use_texture_folder: bpy.props.BoolProperty(
        name="Use Textures",
        description="Use the selected texture folder while importing",
        default=True,
    )
    convert_dds_to_png: bpy.props.BoolProperty(
        name="DDS to PNG",
        description="Convert loaded .dds textures to .png in the export folder",
        default=True,
    )
    status: bpy.props.StringProperty(
        name="Status",
        default="Ready",
    )


CLASSES = [
    AurakingdomModelItem,
    AurakingdomHelper,
]


def register():
    register_classes(CLASSES, __name__)
    bpy.types.Scene.niftools_aurakingdom = bpy.props.PointerProperty(type=AurakingdomHelper)


def unregister():
    if hasattr(bpy.types.Scene, "niftools_aurakingdom"):
        del bpy.types.Scene.niftools_aurakingdom
    unregister_classes(CLASSES, __name__)
