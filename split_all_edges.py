import bpy
import bmesh
import sys 

context = bpy.context
scene = context.scene

scene_file = sys.argv[sys.argv.index('--')+1]

bpy.ops.wm.open_mainfile(filepath=scene_file)
bm = bmesh.new()
meshes = set(o.data for o in bpy.data.objects if o.type == 'MESH')
for me in meshes:
    if len(me.polygons) < 1: continue
    if not getattr(me.polygons[0], "use_smooth"):
        bm.from_mesh(me)
        bmesh.ops.split_edges(bm, edges=bm.edges)
        bm.to_mesh(me)
        bm.clear() 


bpy.ops.wm.save_as_mainfile(filepath=scene_file[:-6]+'_split.blend')
