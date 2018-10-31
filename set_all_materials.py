import bpy
import bmesh
import sys 

context = bpy.context
scene = context.scene

scene_file = sys.argv[sys.argv.index('--')+1]
bpy.ops.wm.open_mainfile(filepath=scene_file)
print(len(bpy.data.materials))
for mat in bpy.data.materials:
    mat.diffuse_color = [1, 1,1]
    mat.diffuse_intensity = 1
    mat.specular_color =  [0,0,0]
    mat.specular_intensity = 0

bpy.ops.wm.save_as_mainfile(filepath=scene_file[:-6]+'_mats.blend')
