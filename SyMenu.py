# Copyright | Pillars of SY (Simon Gloor) | 2018 | All Rights Reserved

# ***********************************************************************************************************************

import bpy
import mathutils
from mathutils import Vector
from math import radians

from mathutils import Color
import random
from bpy.props import *
import bmesh


class SY_MT_SyMenu(bpy.types.Menu):
    bl_label = "SyTools"
    bl_idname = "view3D.sy_menu"

    def draw(self, context):
        layout = self.layout

        #All Modes

        #File
        layout.separator()
        layout.label(text="File")
        layout.separator()
        layout.operator("object.sy_update_links")

        #ObjectMode
        if bpy.context.mode == 'OBJECT':
            layout.separator()
            layout.label(text="ObjectMode", icon = 'OBJECT_DATAMODE')

            #Create
            layout.separator()
            layout.label(text="Create")
            layout.separator()
            layout.operator("mesh.sy_create_cube")
            layout.operator("object.sy_create_sculptsphere")
            layout.operator("object.sy_create_cam")
            layout.operator("object.sy_create_cam_equi")
            layout.operator("mesh.sy_create_skybox_cam")

            #Snap
            layout.separator()
            layout.label(text="Snap n Pivot")
            layout.separator()
            layout.operator("object.sy_set_cursor_pivot")

            #Clean
            layout.separator()
            layout.label(text="Clean")
            layout.separator()
            layout.operator("object.sy_fix_rotation")

        #EditMode
        if bpy.context.mode == 'EDIT_MESH':
            layout.separator()
            layout.label(text="EditMode", icon = 'EDITMODE_HLT')

            layout.separator()
            layout.label(text="Create")
            layout.separator()
            layout.operator("object.sy_create_sculptsphere")

            #Select
            layout.separator()
            layout.label(text="Select")
            layout.separator()
            layout.operator("mesh.region_to_loop")
            layout.operator("mesh.sy_find_ngons")

            #Edit
            layout.separator()
            layout.label(text="Edit")
            layout.separator()
            layout.operator("mesh.bridge_edge_loops")
            layout.operator("mesh.vertices_smooth")
            layout.operator("mesh.sy_face_to_point")
            layout.operator("mesh.sy_turn_subedge")
            layout.operator("view3d.sy_edge_intersection")

            #Unwrap
            layout.separator()
            layout.label(text="Unwrap")
            layout.separator()
            layout.operator("mesh.sy_seam_border")

            #Snap
            layout.separator()
            layout.label(text="Snap n Pivot")
            layout.separator()
            layout.operator("object.sy_set_cursor_pivot")

            #Clean
            layout.separator()
            layout.label(text="Clean")
            layout.separator()
            layout.operator("mesh.remove_doubles")
            layout.operator("object.sy_move_selection_to_zero")
            layout.operator("object.sy_origin_to_selection")


        #SculptMode
        if bpy.context.mode == 'SCULPT':
            layout.separator()
            layout.label(text="SculptMode", icon = 'SCULPTMODE_HLT')

            #Create
            layout.separator()
            layout.label(text="Create")
            layout.separator()
            layout.operator("object.sy_create_sculptsphere")
            layout.operator("mesh.sy_create_cube")
            layout.operator("object.sy_extract_masked")
            layout.operator("mesh.sy_cut_hole")

        #PoseMode
        if bpy.context.mode == 'POSE':
            layout.separator()
            layout.label(text="PoseMode", icon = 'POSE_HLT')

            #Pose
            layout.separator()
            layout.label(text="Pose")
            layout.separator()
            layout.operator("pose.transforms_clear")

        #WeightPaint
        if bpy.context.mode == 'PAINT_WEIGHT':
            layout.separator()
            layout.label(text="WeightMode", icon = 'WPAINT_HLT')

            #Pose
            layout.separator()
            layout.label(text="Convert")
            layout.separator()
            layout.operator("object.sy_weight_to_vertexcol")
