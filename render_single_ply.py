import bpy
import numpy as np
from mathutils import *
from math import *
import sys
import click
from tempfile import TemporaryDirectory

# Delete all default objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()


@click.command()
@click.argument('ply_file')
@click.argument('output_file')
@click.option('--color', nargs=3, default=[95, 200, 221], type=int)
@click.option('--bg', nargs=3, default=[158, 158, 158], type=int)
@click.option('--campos', nargs=3, default=[0, 0, 1.5], type=float)
@click.option('--lightpos', nargs=3, default=[0, 0, 1.5], type=float)
@click.option('--camrot', nargs=3, default=[0, 0, 0], type=float)
@click.option('--ortho_scale', default=1.6, type=float)
def render_geometry(ply_file, output_file, color, bg, campos, lightpos, camrot, ortho_scale):
    # create a new world
    # print(dir(bpy.context.scene.world))
    bpy.context.scene.world.horizon_color = np.array(bg)/255

    bpy.ops.import_mesh.ply(filepath=ply_file)
    bpy.ops.material.new()
    mat = bpy.data.materials["Material"]
    mat.diffuse_color = np.array(color)/255
    bpy.context.scene.objects[0].active_material = mat

    # Add a camera fish eye.
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.ops.object.camera_add(view_align=True, location=campos)
    bpy.data.cameras[0].type = 'ORTHO'
    bpy.data.cameras[0].ortho_scale = ortho_scale
    bpy.context.object.rotation_euler = camrot
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = 1
    bpy.context.scene.camera = bpy.context.object

    # Add a lamp.
    bpy.ops.object.lamp_add(type='POINT', view_align=False, location=lightpos)
    bpy.context.object.data.cycles.cast_shadow = False

    # Set the rendering parameter
    bpy.context.scene.render.resolution_x = 1024
    bpy.context.scene.render.resolution_y = 1024
    bpy.context.scene.render.resolution_percentage = 50
    bpy.context.scene.render.pixel_aspect_x = 1
    bpy.context.scene.render.pixel_aspect_y = 1
    bpy.context.scene.render.use_file_extension = True
    bpy.context.scene.render.image_settings.color_mode = 'RGBA'
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.render.filepath = output_file
    bpy.context.scene.render.image_settings.compression = 90

    # sampling;=path tracing
    bpy.context.scene.cycles.progressive = 'PATH'
    bpy.context.scene.cycles.samples = 64
    bpy.context.scene.cycles.max_bounces = 2
    bpy.context.scene.cycles.min_bounces = 1
    bpy.context.scene.cycles.transparent_max_bounces = 1
    bpy.context.scene.cycles.transparent_min_bounces = 1
    bpy.context.scene.cycles.use_progressive_refine = True
    bpy.context.scene.render.tile_x = 64
    bpy.context.scene.render.tile_y = 64

    # Render results
    bpy.ops.render.render(write_still=True)


if __name__ == '__main__':
    sys.argv = sys.argv[sys.argv.index('--'):]
    render_geometry()
