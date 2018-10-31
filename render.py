import bpy
import numpy as np
from mathutils import *
from math import *
import sys
import click

@click.command()
@click.argument('scene_file')
@click.argument('output_file')
def render_scene(scene_file, output_file):
    bpy.ops.wm.open_mainfile(filepath=scene_file)
    if '/box/' in scene_file:
        bpy.context.scene.objects['right_wall'].hide_render = True
        bpy.context.scene.objects['ceiling'].hide_render = True
        bpy.context.scene.objects['back_wall'].hide_render = True

    camera_pos = np.array((2, -1.5, 2)) + (np.array(bpy.context.scene.objects["hidden_geometry"].location) if "hidden_geometry" in bpy.context.scene.objects else 0)
    camera_rot = [1, 0, 0.75]
    # Add a camera fish eye.
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.ops.object.camera_add(view_align=True, location=camera_pos)
    bpy.context.object.rotation_euler[0] = camera_rot[0]
    bpy.context.object.rotation_euler[1] = camera_rot[1]
    bpy.context.object.rotation_euler[2] = camera_rot[2]
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = 1
    bpy.context.scene.camera = bpy.context.object

    #Add a lamp.
    bpy.ops.object.lamp_add(type='POINT', view_align=False, location=camera_pos)
    bpy.context.object.data.cycles.cast_shadow = True

    #Set the rendering parameter
    bpy.context.scene.render.resolution_x = 250
    bpy.context.scene.render.resolution_y = 250
    bpy.context.scene.render.resolution_percentage = 100
    bpy.context.scene.render.pixel_aspect_x = 1
    bpy.context.scene.render.pixel_aspect_y = 1
    bpy.context.scene.render.use_file_extension = True
    bpy.context.scene.render.image_settings.color_mode ='RGBA'
    bpy.context.scene.render.image_settings.file_format='PNG' 
    bpy.context.scene.render.filepath = output_file
    bpy.context.scene.render.image_settings.compression = 90

    ##sampling;=path tracing 
    bpy.context.scene.cycles.progressive = 'PATH'
    bpy.context.scene.cycles.samples = 64
    bpy.context.scene.cycles.max_bounces = 2
    bpy.context.scene.cycles.min_bounces = 1
    bpy.context.scene.cycles.transparent_max_bounces = 1
    bpy.context.scene.cycles.transparent_min_bounces = 1
    bpy.context.scene.cycles.use_progressive_refine = True
    bpy.context.scene.render.tile_x = 64
    bpy.context.scene.render.tile_y = 64

    #Render results
    bpy.ops.render.render(write_still=True)

if __name__ == '__main__':
    sys.argv = sys.argv[sys.argv.index('--'):]
    render_scene()