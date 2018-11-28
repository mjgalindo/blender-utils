import bpy
import numpy as np
from mathutils import *
from math import *
import sys
import click
import re

@click.command()
@click.argument('scene_file')
@click.option('--center', default=[0,0,0], nargs=3, type=float)
@click.option('--radius', default=1.0, type=float)
def get_gt(scene_file, center, radius):
    bpy.ops.wm.open_mainfile(filepath=scene_file)

    # Join the whole scene as a single mesh
    bpy.context.scene.objects.active = bpy.data.objects[0]
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.join()

    # Get into edit mode
    bpy.ops.object.mode_set(mode='EDIT')
    # Bisect by the 6 planes twice deleting the outside (backfacing geometry isn't bisected)
    for ax in range(3):
        axis = np.zeros((3,))
        axis[ax] = 1.0
        for sign in [-1,1]:
            plane_normal = axis * sign
            plane_point = center + plane_normal * radius
            print(radius, plane_point, plane_normal)
            for _ in range(2):
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.bisect(plane_co=plane_point, plane_no=plane_normal, clear_outer=True, threshold=1e-6)

    # Export what's left
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.export_mesh.ply(filepath=scene_file[:scene_file.rfind('.')]+'.ply')


if __name__ == '__main__':
    sys.argv = sys.argv[sys.argv.index('--'):]
    get_gt()