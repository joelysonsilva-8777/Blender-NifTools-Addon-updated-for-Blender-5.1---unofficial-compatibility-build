"""Aurakingdom helper sidebar."""

from bpy.types import Panel

from io_scene_niftools.utils.decorators import register_classes, unregister_classes


class AurakingdomHelperPanel(Panel):
    bl_label = "Niftools Aurakingdom Helper"
    bl_idname = "NIFTOOLS_PT_aurakingdom_helper"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Niftools Aurakingdom Helper"

    def draw(self, context):
        props = context.scene.niftools_aurakingdom
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        col = layout.column(align=True)
        col.prop(props, "model_dir")
        col.operator("niftools.aurakingdom_refresh_models", icon='FILE_REFRESH')
        col.prop_search(props, "model_file", props, "model_items", text="Model")
        col.label(text=f"{props.model_count} models cached")
        col.prop(props, "texture_dir")
        col.prop(props, "animation_dir")
        col.prop(props, "use_texture_folder")
        col.prop(props, "import_animation")
        col.operator("niftools.aurakingdom_import", icon='IMPORT')

        layout.separator()

        col = layout.column(align=True)
        col.prop(props, "export_dir")
        col.prop(props, "export_name")
        col.prop(props, "convert_dds_to_png")
        col.operator("niftools.aurakingdom_export", icon='EXPORT')

        layout.separator()

        for line in props.status.split(" | "):
            layout.label(text=line)


CLASSES = [
    AurakingdomHelperPanel,
]


def register():
    register_classes(CLASSES, __name__)


def unregister():
    unregister_classes(CLASSES, __name__)
