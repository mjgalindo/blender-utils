import bpy
import sys 

context = bpy.context
scene = context.scene

scene_file = sys.argv[sys.argv.index('--')+1]

bpy.ops.wm.open_mainfile(filepath=scene_file)
bpy.ops.object.select_all(action='DESELECT')

mesh_objects = [o for o in bpy.data.objects if o.type == 'MESH']
meshes = set(o.data for o in mesh_objects)
for ob in mesh_objects:
    scene.objects.active = ob
    if not getattr(ob.data.polygons[0], "use_smooth"):
        ob.select = True
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.edge_split()
        bpy.ops.object.editmode_toggle()

bpy.ops.wm.save_as_mainfile(filepath=scene_file)
