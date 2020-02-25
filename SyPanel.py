# Copyright | Pillars of SY (Simon Gloor) | 2018 | All Rights Reserved

# ***********************************************************************************************************************

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

    def __init__(self):
        pass

    @classmethod
    def poll(self, context):
        try:
            ob = context.active_object
            mode = context.mode
            return (ob.type == 'MESH')
        except AttributeError:
            return 0

    def draw(self, context):

        layout = self.layout

        # standard normal commands
        box = self.layout.box()
        box.label(text='Standard Tools')

        col = box.column(align=True)
        row = col.row(align=True)
        row.operator('object.shade_smooth', text = 'Smooth')
        row.operator('object.shade_flat', text = 'Flat')
        row = col.row(align=True)
        row.operator('mesh.normals_make_consistent', text = 'Recalculate')
        row.operator('mesh.flip_normals', text = 'Flip Direction')
