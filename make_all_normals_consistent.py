import bpy
import sys

scene_file = sys.argv[sys.argv.index('--')+1]

bpy.ops.wm.open_mainfile(filepath=scene_file)

mesh_objects = [o for o in bpy.data.objects if o.type == 'MESH']
for obj in mesh_objects:
    bpy.ops.object.select_all(action='DESELECT')
    obj.select = True
    bpy.context.scene.objects.active = obj
    # go edit mode
    bpy.ops.object.mode_set(mode='EDIT')
    # select al faces
    bpy.ops.mesh.select_all(action='SELECT')
    # recalculate outside normals 
    bpy.ops.mesh.normals_make_consistent(inside=False)
    # go object mode again
    bpy.ops.object.editmode_toggle()
bpy.ops.wm.save_as_mainfile(filepath=scene_file)
