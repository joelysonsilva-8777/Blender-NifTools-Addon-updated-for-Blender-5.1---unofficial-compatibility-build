"""Aurakingdom helper operators."""

import os
from pathlib import Path

import bpy
from bpy.types import Operator

from io_scene_niftools.utils.decorators import register_classes, unregister_classes


def _abs_path(path_value):
    return Path(bpy.path.abspath(path_value)).resolve()


def _find_case_insensitive(folder, stem, suffix):
    folder = Path(folder)
    if not folder.is_dir():
        return None
    exact = folder / f"{stem}{suffix}"
    if exact.exists():
        return exact
    target = f"{stem}{suffix}".lower()
    for path in folder.iterdir():
        if path.is_file() and path.name.lower() == target:
            return path
    return None


def _set_status(context, message):
    context.scene.niftools_aurakingdom.status = message


def _refresh_model_cache(props):
    props.model_items.clear()
    props.model_count = 0
    props.model_dir_cache = ""

    if not props.model_dir:
        props.model_file = ""
        return False, "Select a model folder."

    model_dir = _abs_path(props.model_dir)
    if not model_dir.is_dir():
        props.model_file = ""
        return False, f"Model folder not found: {model_dir}"

    current_model = props.model_file
    try:
        model_names = sorted(
            (
                entry.name
                for entry in os.scandir(model_dir)
                if entry.is_file() and entry.name.lower().endswith(".nif")
            ),
            key=str.lower,
        )
    except OSError as exc:
        props.model_file = ""
        return False, f"Could not read model folder: {exc}"

    for model_name in model_names:
        item = props.model_items.add()
        item.name = model_name
        item.file_name = model_name

    props.model_count = len(model_names)
    props.model_dir_cache = str(model_dir)

    if current_model not in model_names:
        props.model_file = model_names[0] if len(model_names) == 1 else ""

    if not model_names:
        return False, "No .nif models found."
    return True, f"Cached {len(model_names)} .nif models."


def _model_cache_current(props):
    if not props.model_dir or not props.model_dir_cache:
        return False
    return props.model_dir_cache == str(_abs_path(props.model_dir))


def _new_images(before_names):
    return [image for image in bpy.data.images if image.name not in before_names]


def _summarize_textures(images):
    found = []
    missing = []
    for image in images:
        image_path = bpy.path.abspath(image.filepath) if image.filepath else ""
        if image_path and os.path.exists(image_path):
            found.append(image.name)
        else:
            missing.append(image.name)
    return found, missing


def _select_armature_for_kf(imported_object_names):
    armatures = [
        obj for obj in bpy.data.objects
        if obj.type == 'ARMATURE' and obj.name in imported_object_names
    ]
    if not armatures:
        armatures = [obj for obj in bpy.context.selected_objects if obj.type == 'ARMATURE']
    if not armatures:
        armatures = [obj for obj in bpy.data.objects if obj.type == 'ARMATURE']
    if not armatures:
        return None

    armature = armatures[0]
    for obj in bpy.context.selected_objects:
        obj.select_set(False)
    armature.select_set(True)
    bpy.context.view_layer.objects.active = armature
    return armature


def _convert_dds_images_to_png(export_dir):
    export_dir = Path(export_dir)
    export_dir.mkdir(parents=True, exist_ok=True)
    converted = []
    failed = []

    for image in bpy.data.images:
        filepath = Path(bpy.path.abspath(image.filepath)) if image.filepath else Path(image.name)
        image_name = Path(image.name)
        if filepath.suffix.lower() != ".dds" and image_name.suffix.lower() != ".dds":
            continue

        stem = filepath.stem if filepath.suffix else image_name.stem
        png_path = export_dir / f"{stem}.png"
        try:
            image.save_render(str(png_path))
        except Exception:
            failed.append(image.name)
        else:
            converted.append(png_path.name)

    return converted, failed


class AurakingdomRefreshModelsOperator(Operator):
    bl_idname = "niftools.aurakingdom_refresh_models"
    bl_label = "Refresh Models"
    bl_options = {'REGISTER'}

    def execute(self, context):
        props = context.scene.niftools_aurakingdom
        ok, message = _refresh_model_cache(props)
        _set_status(context, message)
        self.report({'INFO'} if ok else {'WARNING'}, message)
        return {'FINISHED'} if ok else {'CANCELLED'}


class AurakingdomImportOperator(Operator):
    bl_idname = "niftools.aurakingdom_import"
    bl_label = "Import"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.niftools_aurakingdom
        if not _model_cache_current(props) and not props.model_file:
            _refresh_model_cache(props)

        model_file = props.model_file.strip()
        if not model_file:
            _set_status(context, "No .nif model selected.")
            self.report({'ERROR'}, "No .nif model selected.")
            return {'CANCELLED'}

        model_dir = _abs_path(props.model_dir)
        nif_path = model_dir / model_file
        if not nif_path.exists():
            _set_status(context, f"Model not found: {nif_path.name}")
            self.report({'ERROR'}, f"Model not found: {nif_path}")
            return {'CANCELLED'}

        before_objects = {obj.name for obj in bpy.data.objects}
        before_images = {image.name for image in bpy.data.images}
        messages = []

        old_texture_dir = bpy.context.preferences.filepaths.texture_directory
        try:
            if props.use_texture_folder and props.texture_dir:
                bpy.context.preferences.filepaths.texture_directory = str(_abs_path(props.texture_dir))

            result = bpy.ops.import_scene.nif(filepath=str(nif_path))
        finally:
            bpy.context.preferences.filepaths.texture_directory = old_texture_dir

        if 'CANCELLED' in result:
            _set_status(context, f"Import cancelled: {nif_path.name}")
            return {'CANCELLED'}

        messages.append(f"Imported {nif_path.name}")

        found_textures, missing_textures = _summarize_textures(_new_images(before_images))
        if missing_textures:
            messages.append(f"Missing textures: {len(missing_textures)}")
            self.report({'WARNING'}, f"Missing textures: {', '.join(missing_textures[:5])}")
        elif found_textures:
            messages.append(f"Textures loaded: {len(found_textures)}")
        else:
            messages.append("No new textures found.")

        if props.import_animation:
            kf_path = _find_case_insensitive(_abs_path(props.animation_dir), nif_path.stem, ".kf") if props.animation_dir else None
            if kf_path:
                imported_names = {obj.name for obj in bpy.data.objects if obj.name not in before_objects}
                armature = _select_armature_for_kf(imported_names)
                if armature:
                    kf_result = bpy.ops.import_scene.kf(
                        filepath=str(kf_path),
                        files=[{"name": kf_path.name}],
                    )
                    if 'CANCELLED' in kf_result:
                        messages.append(f"KF cancelled: {kf_path.name}")
                    else:
                        messages.append(f"Imported {kf_path.name}")
                else:
                    messages.append(f"No armature for {kf_path.name}")
            else:
                messages.append(f"KF not found: {nif_path.stem}.kf")

        status = " | ".join(messages)
        _set_status(context, status)
        self.report({'INFO'}, status)
        return {'FINISHED'}


class AurakingdomExportOperator(Operator):
    bl_idname = "niftools.aurakingdom_export"
    bl_label = "Export"
    bl_options = {'REGISTER'}

    def execute(self, context):
        props = context.scene.niftools_aurakingdom
        export_dir = _abs_path(props.export_dir) if props.export_dir else Path(bpy.path.abspath("//")).resolve()
        export_dir.mkdir(parents=True, exist_ok=True)

        export_name = props.export_name.strip()
        if not export_name and props.model_file:
            export_name = Path(props.model_file).stem
        if not export_name:
            export_name = bpy.context.scene.name or "export"

        nif_path = export_dir / f"{export_name}.nif"
        result = bpy.ops.export_scene.nif(filepath=str(nif_path))
        if 'CANCELLED' in result:
            _set_status(context, f"Export cancelled: {nif_path.name}")
            return {'CANCELLED'}

        messages = [f"Exported {nif_path.name}"]
        if props.convert_dds_to_png:
            converted, failed = _convert_dds_images_to_png(export_dir)
            if converted:
                messages.append(f"PNG textures: {len(converted)}")
            if failed:
                messages.append(f"DDS conversion failed: {len(failed)}")
                self.report({'WARNING'}, f"DDS conversion failed: {', '.join(failed[:5])}")

        status = " | ".join(messages)
        _set_status(context, status)
        self.report({'INFO'}, status)
        return {'FINISHED'}


CLASSES = [
    AurakingdomRefreshModelsOperator,
    AurakingdomImportOperator,
    AurakingdomExportOperator,
]


def register():
    register_classes(CLASSES, __name__)


def unregister():
    unregister_classes(CLASSES, __name__)
