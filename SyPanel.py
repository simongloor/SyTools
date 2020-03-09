import bmesh
import bpy
import mathutils
import bgl
from bpy.types import Panel
from rna_prop_ui import PropertyPanel
from sys import float_info as fi


##########################################################
# draw UI ButtonS
class SY_PT_sy_panel_ui(bpy.types.Panel):
    bl_idname = "SyPanel"
    bl_label = 'SyTools'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "SY | flow"

    def __init__(self):
        pass

    @classmethod
    def poll(self, context):
        try:
            ob = context.active_object
            mode = context.mode
            return 1#(ob.type == 'MESH')
        except AttributeError:
            return 0

    def draw(self, context):

        layout = self.layout

        #Surface
        box = self.layout.box()
        box.label(text='Surface')

        col = box.column(align=True)
        row = col.row(align=True)
        row.operator('object.shade_smooth', text = 'Smooth')
        row.operator('object.shade_flat', text = 'Flat')
        row = col.row(align=True)
        row.operator('mesh.normals_make_consistent', text = 'Recalculate')
        row.operator('mesh.flip_normals', text = 'Flip Direction')

        #Collision
        box = self.layout.box()
        box.label(text='Collision')

        col = box.column(align=True)
        row = col.row(align=True)
        row.operator('object.sy_create_bounds_from_objects', text = 'Bounds from Objects')
        row = col.row(align=True)
        row.operator('object.sy_create_bounds_from_vertices', text = 'Bounds from Vertices')
        row = col.row(align=True)
        row.operator('object.sy_split_bounds', text = 'Split Bounds')

        #UV
        box = self.layout.box()
        box.label(text='UV')
        box = box.box()
        box.label(text='UV from Origin')

        col = box.column(align=True)
        row = col.row(align=True)
        row.operator('object.sy_add_uv_origin', text = 'Add Origin')
        row = col.row(align=True)
        row.operator('object.sy_apply_uv_origin', text = 'Apply')

#************************************************************************************

# # init properties
# def init_properties():
#
#     # bpy.types.WindowManager.SpecificUVOrigin = bpy.props.PointerProperty(name="Specific UV-Origin", type=bpy.types.Object)
#
# # clear properties
# def clear_properties():
#     props = ['RunAutoImport', 'RenameFile', 'RunMoveToCenter', 'RunUnparent', 'RunRename', 'RunClean', 'RunModifiers', 'TargetDecimateCount', 'RunRewrapT', 'RunRewrapL', 'RunIslands', 'RunPackT', 'RunPackL', 'PackSize', 'PackRotate', 'OldRewrapT', 'OldRewrapL', 'OldIsland', 'RunExportFBX', 'ExportAnim', 'CurveLength']
#     for p in props:
#         if bpy.context.window_manager.get(p) != None:
#             del bpy.context.window_manager[p]
#         try:
#             x = getattr(bpy.types.WindowManager, p)
#             del x
#         except:
#             pass
