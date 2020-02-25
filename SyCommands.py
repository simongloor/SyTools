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


#************************************************************************************
# CreateCamEqui
class SY_OT_SySetCursorPivot(bpy.types.Operator):
    bl_idname = "object.sy_set_cursor_pivot"
    bl_label = "Cursor Pivot (Sy)"

    def execute(self, context):

        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.context.space_data.pivot_point = 'CURSOR'

        return {'FINISHED'}

#************************************************************************************
# CreateCamEqui
class SY_OT_SyUpdateLinks(bpy.types.Operator):
    bl_idname = "object.sy_update_links"
    bl_label = "Refresh File (Sy)"

    def execute(self, context):

        path = bpy.data.filepath

        if path:
            bpy.ops.wm.save_mainfile()
            self.report({'INFO'}, "Saved & Reloaded")
            bpy.ops.wm.open_mainfile("EXEC_DEFAULT", filepath=path)
        else:
            bpy.ops.wm.save_as_mainfile("INVOKE_AREA")

        return {'FINISHED'}

#************************************************************************************
# CreateCamEqui
class SY_OT_SyCreateCamEqui(bpy.types.Operator):
    bl_idname = "object.sy_create_cam_equi"
    bl_label = "Create Camera Equirectangular (Sy)"

    def execute(self, context):

        #Calculate Spawnpoint
        SpawnLoc = bpy.context.region_data.view_location
        OffsetVec = Vector((0, 0, bpy.context.region_data.view_distance))
        OffsetRot = bpy.context.region_data.view_rotation
        TargetLocation = SpawnLoc + (OffsetRot * OffsetVec)

        #Create Cam
        bpy.ops.object.camera_add(view_align=True, enter_editmode=False, location=TargetLocation)
        bpy.context.object.rotation_euler[0] = 1.5708

        #SetUp Cam- and Rendersettings
        bpy.context.object.data.type = 'PANO'
        bpy.context.object.data.cycles.panorama_type = 'EQUIRECTANGULAR'
        bpy.context.scene.render.resolution_x = 2048
        bpy.context.scene.render.resolution_y = 1024
        bpy.ops.view3d.object_as_camera()


        return {'FINISHED'}


#************************************************************************************
# CutHole
class SY_OT_SyCutHole(bpy.types.Operator):
    bl_idname = "mesh.sy_cut_hole"
    bl_label = "Cut Hole (Sy)"

    def execute(self, context):

        #Hide Mask
        bpy.ops.paint.hide_show(action = 'HIDE', area='MASKED')

        #Select Hidden
        bpy.ops.sculpt.sculptmode_toggle()
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.reveal()

        #Smooth Selection
        bpy.ops.mesh.select_more()
        bpy.ops.mesh.select_less()

        #Delete Vertices
        bpy.ops.mesh.delete(type='VERT')

        #Get Boundary
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.region_to_loop()

        #Bridge
        bpy.ops.mesh.bridge_edge_loops()

        #Go back to Sculpting and enable DynTopo
        bpy.ops.sculpt.sculptmode_toggle()
        bpy.ops.sculpt.dynamic_topology_toggle()

        return {'FINISHED'}


#************************************************************************************
# FaceToPoint
class SY_OT_SyCreateCam(bpy.types.Operator):
    bl_idname = "mesh.sy_face_to_point"
    bl_label = "Face to Point (Sy)"

    def execute(self, context):

        bpy.ops.mesh.extrude_region_move()
        bpy.ops.mesh.merge(type='CENTER')

        return {'FINISHED'}


#************************************************************************************
# CreateCam
class SY_OT_SyCreateCam(bpy.types.Operator):
    bl_idname = "object.sy_create_cam"
    bl_label = "Create Camera (Sy)"

    def execute(self, context):

        SpawnLoc = bpy.context.region_data.view_location
        OffsetVec = Vector((0, 0, bpy.context.region_data.view_distance))
        OffsetRot = bpy.context.region_data.view_rotation
        TargetLocation = SpawnLoc + (OffsetRot * OffsetVec)

        bpy.ops.object.camera_add(view_align=True, enter_editmode=False, location=TargetLocation)
        bpy.ops.view3d.object_as_camera()

        return {'FINISHED'}


#************************************************************************************
# CreateSculptSphere
class SY_OT_SyOriginToSelection(bpy.types.Operator):
    bl_idname = "object.sy_create_sculptsphere"
    bl_label = "Create SculptSphere (Sy)"

    def execute(self, context):

        bpy.ops.mesh.primitive_uv_sphere_add(size=1, view_align=False, enter_editmode=False, location=(0, 0, 0))
        bpy.ops.sculpt.sculptmode_toggle()
        bpy.ops.sculpt.dynamic_topology_toggle()
        bpy.context.scene.tool_settings.sculpt.detail_size = 10
        bpy.context.scene.tool_settings.sculpt.detail_refine_method = 'SUBDIVIDE_COLLAPSE'

        return {'FINISHED'}


#************************************************************************************
# OriginToSelection
class SY_OT_SyOriginToSelection(bpy.types.Operator):
    bl_idname = "object.sy_origin_to_selection"
    bl_label = "Set Origin to Selection (Sy)"

    def execute(self, context):

        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.ops.object.editmode_toggle()

        return {'FINISHED'}


#************************************************************************************
# Create SkyboxCam
class SY_OT_SyCreateSkyboxCam(bpy.types.Operator):
    bl_idname = "mesh.sy_create_skybox_cam"
    bl_label = "Create SkyboxCam (Sy)"

    def execute(self, context):

        #Set general Settings
        bpy.context.scene.render.engine = 'CYCLES'
        bpy.context.scene.render.resolution_x = 2048
        bpy.context.scene.render.resolution_y = 2048
        bpy.context.scene.frame_end = 6

        #Create Empty CamHolder
        bpy.ops.object.empty_add(type='PLAIN_AXES')
        bpy.context.object.name = 'SkyboxCam.000'

        #Create the first Cam
        bpy.ops.object.camera_add(view_align=False, rotation=(1.5708, 0, 0))
        bpy.context.object.data.lens_unit = 'FOV'
        bpy.context.object.data.angle = 1.5708
        bpy.context.object.data.clip_start = 0.001
        bpy.context.object.name = 'SkyboxCam.001'


        #Create the additional Cams
        bpy.ops.object.duplicate_move()
        bpy.ops.transform.rotate(value=-1.5708, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL')

        bpy.ops.object.duplicate_move()
        bpy.ops.transform.rotate(value=-1.5708, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL')

        bpy.ops.object.duplicate_move()
        bpy.ops.transform.rotate(value=-1.5708, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL')

        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects['SkyboxCam.001'].select = True
        bpy.ops.object.duplicate_move()
        bpy.ops.transform.rotate(value=1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL')

        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects['SkyboxCam.001'].select = True
        bpy.ops.object.duplicate_move()
        bpy.ops.transform.rotate(value=-1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL')


        #Attach the Cams to a EmptyObject
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects['SkyboxCam.001'].select = True
        bpy.data.objects['SkyboxCam.002'].select = True
        bpy.data.objects['SkyboxCam.003'].select = True
        bpy.data.objects['SkyboxCam.004'].select = True
        bpy.data.objects['SkyboxCam.005'].select = True
        bpy.data.objects['SkyboxCam.006'].select = True
        bpy.data.objects['SkyboxCam.000'].select = True
        bpy.context.scene.objects.active = bpy.data.objects['SkyboxCam.000']
        bpy.ops.object.parent_set(type='OBJECT')


        #SetUp the RenderMarkers
        bpy.context.area.type = 'TIMELINE'

        bpy.context.scene.frame_current = 1
        bpy.ops.marker.add()
        bpy.context.area.type = 'VIEW_3D'
        bpy.context.scene.objects.active = bpy.data.objects['SkyboxCam.001']
        bpy.ops.view3d.object_as_camera()
        bpy.context.area.type = 'TIMELINE'
        bpy.ops.marker.camera_bind()

        bpy.context.scene.frame_current = 2
        bpy.ops.marker.add()
        bpy.context.area.type = 'VIEW_3D'
        bpy.context.scene.objects.active = bpy.data.objects['SkyboxCam.002']
        bpy.ops.view3d.object_as_camera()
        bpy.context.area.type = 'TIMELINE'
        bpy.ops.marker.camera_bind()

        bpy.context.scene.frame_current = 3
        bpy.ops.marker.add()
        bpy.context.area.type = 'VIEW_3D'
        bpy.context.scene.objects.active = bpy.data.objects['SkyboxCam.003']
        bpy.ops.view3d.object_as_camera()
        bpy.context.area.type = 'TIMELINE'
        bpy.ops.marker.camera_bind()

        bpy.context.scene.frame_current = 4
        bpy.ops.marker.add()
        bpy.context.area.type = 'VIEW_3D'
        bpy.context.scene.objects.active = bpy.data.objects['SkyboxCam.004']
        bpy.ops.view3d.object_as_camera()
        bpy.context.area.type = 'TIMELINE'
        bpy.ops.marker.camera_bind()

        bpy.context.scene.frame_current = 5
        bpy.ops.marker.add()
        bpy.context.area.type = 'VIEW_3D'
        bpy.context.scene.objects.active = bpy.data.objects['SkyboxCam.005']
        bpy.ops.view3d.object_as_camera()
        bpy.context.area.type = 'TIMELINE'
        bpy.ops.marker.camera_bind()

        bpy.context.scene.frame_current = 6
        bpy.ops.marker.add()
        bpy.context.area.type = 'VIEW_3D'
        bpy.context.scene.objects.active = bpy.data.objects['SkyboxCam.006']
        bpy.ops.view3d.object_as_camera()
        bpy.context.area.type = 'TIMELINE'
        bpy.ops.marker.camera_bind()

        bpy.context.scene.frame_current = 1
        bpy.context.area.type = 'VIEW_3D'


        return {'FINISHED'}


#************************************************************************************
# Extract Masked
class SY_OT_SyExtractMasked(bpy.types.Operator):
    bl_idname = "object.sy_extract_masked"
    bl_label = "Extract Masked (Sy)"

    def execute(self, context):

        #Duplicate Mesh
        bpy.ops.sculpt.sculptmode_toggle()
        bpy.ops.object.duplicate_move()

        #Hide Mask
        bpy.ops.sculpt.sculptmode_toggle()
        bpy.ops.paint.hide_show(action = 'HIDE', area='MASKED')

        #Delete Shown
        bpy.ops.sculpt.sculptmode_toggle()
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='TOGGLE')
        bpy.ops.mesh.delete(type='FACE')

        #Unhide and Deselect All
        bpy.ops.mesh.reveal()
        bpy.ops.mesh.select_all(action='TOGGLE')
        bpy.ops.object.editmode_toggle()

        #Add Modifier
        bpy.ops.object.modifier_add(type='SOLIDIFY')
        bpy.context.object.modifiers["Solidify"].thickness = -0.02

        #Go back to Sculpting
        bpy.ops.sculpt.sculptmode_toggle()


        return {'FINISHED'}


#************************************************************************************
# Turn Subedge
class SY_OT_SyTurnSubedge(bpy.types.Operator):
    bl_idname = "mesh.sy_turn_subedge"
    bl_label = "Turn Subedge (Sy)"

    def execute(self, context):

        #ToTris
        bpy.ops.mesh.quads_convert_to_tris(use_beauty=True)

        #Flip
        bpy.ops.mesh.edge_rotate()

        #ToQuad
        bpy.ops.mesh.edge_face_add()

        return {'FINISHED'}

#************************************************************************************
# Add Cube upon Grid
class SY_OT_SyCreateCube(bpy.types.Operator):
    bl_idname = "mesh.sy_create_cube"
    bl_label = "Create Cube (Sy)"

    def execute(self, context):

        #Move Cursor to Zero
        bpy.ops.view3d.snap_cursor_to_center()

        #Create Cube
        bpy.ops.mesh.primitive_cube_add(enter_editmode=True)

        #Move Cube Up
        bpy.ops.transform.translate(value=(0, 0, 1))

        return {'FINISHED'}

#************************************************************************************
# Move Selection to Zero
class SY_OT_SyMoveSelectionToZero(bpy.types.Operator):
    bl_idname = "object.sy_move_selection_to_zero"
    bl_label = "Move Selection to Origin (Sy)"

    def execute(self, context):

        #Move Cursor to Selection
        bpy.ops.view3d.snap_cursor_to_selected()

        #Move to ObjectMode
        bpy.ops.object.mode_set(mode='OBJECT')

        #Set Origin
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

        #Move to Zero
        bpy.context.object.location[0] = 0
        bpy.context.object.location[1] = 0
        bpy.context.object.location[2] = 0

        #return to the EditMode
        bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}



#************************************************************************************
# Fix the Rotation to match Unity
class SY_OT_SyFixRotation(bpy.types.Operator):
    bl_idname = "object.sy_fix_rotation"
    bl_label = "Fix Rotation for Unity (Sy)"

    def execute(self, context):

        #Save old PivotOption
        OldPivotOption = bpy.context.space_data.pivot_point

        #Set new PivotOption
        bpy.context.space_data.pivot_point = 'INDIVIDUAL_ORIGINS'

        #Rotate Selection -90
        bpy.ops.transform.rotate(value=-1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL')

        #Apply Rotation
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

        #Rotate Selection -90
        bpy.ops.transform.rotate(value=1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL')

        #Restore old PivotOption
        bpy.context.space_data.pivot_point = OldPivotOption

        return {'FINISHED'}


#************************************************************************************
# Dissolve Edge completely
class SY_OT_SyDissolveEdge(bpy.types.Operator):
    bl_idname = "mesh.sy_dissolve_edge"
    bl_label = "Dissolve Edge (Sy)"

    def execute(self, context):
        bpy.ops.mesh.dissolve_edges(use_verts=False, use_face_split=False)
        bpy.ops.mesh.dissolve_verts(use_face_split=False)

        return {'FINISHED'}


#************************************************************************************
# Connect on Intersection

class SY_OT_SyEdgeIntersection(bpy.types.Operator):
    "Finds the mid-point of the shortest distance between two edges"

    bl_idname = "view3d.sy_edge_intersection"
    bl_label = "Edge Intersection (Sy)"

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj != None and obj.type == 'MESH'

    def execute(self, context):
        from mathutils.geometry import intersect_line_line

        obj = context.active_object

        if (obj.type != "MESH"):
            operator.report({'ERROR'}, "Object must be a mesh")
            return None

        edges = []
        mesh = obj.data
        verts = mesh.vertices

        is_editmode = (obj.mode == 'EDIT')
        if is_editmode:
            bpy.ops.object.mode_set(mode='OBJECT')

        for e in mesh.edges:
            if e.select:
                edges.append(e)

                if len(edges) > 2:
                    break

        if is_editmode:
            bpy.ops.object.mode_set(mode='EDIT')

        if len(edges) != 2:
            operator.report({'ERROR'},
                            "Operator requires exactly 2 edges to be selected")
            return

        line = intersect_line_line(verts[edges[0].vertices[0]].co,
                                   verts[edges[0].vertices[1]].co,
                                   verts[edges[1].vertices[0]].co,
                                   verts[edges[1].vertices[1]].co)

        if line is None:
            operator.report({'ERROR'}, "Selected edges do not intersect")
            return

        point = line[0].lerp(line[1], 0.5)
        context.scene.cursor_location = obj.matrix_world * point
        bpy.ops.mesh.merge(type='CURSOR', uvs=False)
        return {'FINISHED'}

#************************************************************************************
# Convert WeightPaint to VertexPaint

class SY_OT_Weight2VertexCol(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.sy_weight_to_vertexcol"
    bl_label = "Weight to VertexCol (Sy)"
    bl_space_type = "VIEW_3D"
    bl_options = {'REGISTER', 'UNDO'}

    method=bpy.props.BoolProperty(name="Color", description="Choose the coloring method", default=False)

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        transferWeight2VertexCol(context, self.method)
        context.active_object.data.update()
        return {'FINISHED'}


def transferWeight2VertexCol(context, method):

    bpy.ops.paint.vertex_paint_toggle()
    bpy.data.brushes["Draw"].color = (0, 0, 0)
    bpy.ops.paint.vertex_color_set()
    bpy.ops.paint.weight_paint_toggle()

    me=context.active_object
    verts=me.data.vertices

    col=Color()
    col.h=0
    col.s=1
    col.v=1

    #vcolgrp=bpy.context.active_object.data.vertex_colors.keys()

    try:
        assert bpy.context.active_object.vertex_groups
        assert bpy.context.active_object.data.vertex_colors

    except AssertionError:
        bpy.ops.error.message('INVOKE_DEFAULT',
                type = "Error",
                message = 'you need at least one vertex group and one color group')
        return

    vgrp=bpy.context.active_object.vertex_groups.keys()

    vcolgrp=bpy.context.active_object.data.vertex_colors


    #Check to see if we have at least one vertex group and one vertex color group
    if len(vgrp) > 0 and len(vcolgrp) > 0:
        print ("enough parameters")

        #Colored
        if method:
            for poly in me.data.polygons:
                for loop in poly.loop_indices:
                    vertindex=me.data.loops[loop].vertex_index

                    #Check to see if the vertex has any geoup association
                    try:
                        weight=me.vertex_groups.active.weight(vertindex)
                    except:
                       continue

                    #col=Color ((r, g, b ))
                    col.h=0.66*weight
                    col.s=1
                    col.v=1
                    me.data.vertex_colors.active.data[loop].color = (col.b, col.g, col.r)


        if not method:
            for poly in me.data.polygons:
                for loop in poly.loop_indices:
                    vertindex=me.data.loops[loop].vertex_index
                    #weight=me.vertex_groups['Group'].weight(vertindex)

                    #Check to see if the vertex has any geoup association
                    try:
                        weight=me.vertex_groups.active.weight(vertindex)
                    except:
                        continue

                    col.r=weight
                    col.g=col.r
                    col.b=col.r
                    me.data.vertex_colors.active.data[loop].color = (col.b, col.g, col.r)


#************************************************************************************
# Add Seams on Border
class SY_OT_SySeamBorder(bpy.types.Operator):
    bl_idname = "mesh.sy_seam_border"
    bl_label = "Seam Border (Sy)"

    def execute(self, context):

        # save selection
        bpy.ops.object.vertex_group_add()
        bpy.ops.object.vertex_group_assign()

        # set seams
        bpy.ops.mesh.region_to_loop()
        bpy.ops.mesh.mark_seam(clear=False)
        bpy.context.tool_settings.mesh_select_mode = [False, False, True]

        # load selection
        bpy.ops.object.vertex_group_select()
        bpy.ops.object.vertex_group_remove()

        return {'FINISHED'}
