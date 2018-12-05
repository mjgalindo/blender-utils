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
def render_geometry(ply_file, output_file, color):
    # create a new world
    # print(dir(bpy.context.scene.world))
    bpy.context.scene.world.horizon_color = np.array([158, 158, 158])/255
    scn = bpy.context.scene

    bpy.ops.import_mesh.ply(filepath=ply_file)
    bpy.ops.material.new()
    mat = bpy.data.materials["Material"]
    mat.diffuse_color = np.array(color)/255
    bpy.context.scene.objects[0].active_material = mat
    camera_pos = [0, 0, 1.5]
    light_pos = [0, 0, 2.5]

    # Add a camera fish eye.
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.ops.object.camera_add(view_align=True, location=camera_pos)
    bpy.context.object.rotation_euler[0] = 0
    bpy.context.object.rotation_euler[1] = 0
    bpy.context.object.rotation_euler[2] = 0
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = 1
    bpy.context.scene.camera = bpy.context.object

    # Add a lamp.
    bpy.ops.object.lamp_add(type='POINT', view_align=False, location=light_pos)
    bpy.context.object.data.cycles.cast_shadow = True

    # Set the rendering parameter
    bpy.context.scene.render.resolution_x = 1024 / 2
    bpy.context.scene.render.resolution_y = 1024 / 2
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
