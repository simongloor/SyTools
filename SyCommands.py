import sys
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
    bl_description = "Save and reopen the file to delete unused assets."

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
class SY_OT_SyCreateSculptsphere(bpy.types.Operator):
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
        bpy.context.view_layer.objects.active = bpy.data.objects['SkyboxCam.000']
        bpy.ops.object.parent_set(type='OBJECT')


        #SetUp the RenderMarkers
        bpy.context.area.type = 'TIMELINE'

        bpy.context.scene.frame_current = 1
        bpy.ops.marker.add()
        bpy.context.area.type = 'VIEW_3D'
        bpy.context.view_layer.objects.active = bpy.data.objects['SkyboxCam.001']
        bpy.ops.view3d.object_as_camera()
        bpy.context.area.type = 'TIMELINE'
        bpy.ops.marker.camera_bind()

        bpy.context.scene.frame_current = 2
        bpy.ops.marker.add()
        bpy.context.area.type = 'VIEW_3D'
        bpy.context.view_layer.objects.active = bpy.data.objects['SkyboxCam.002']
        bpy.ops.view3d.object_as_camera()
        bpy.context.area.type = 'TIMELINE'
        bpy.ops.marker.camera_bind()

        bpy.context.scene.frame_current = 3
        bpy.ops.marker.add()
        bpy.context.area.type = 'VIEW_3D'
        bpy.context.view_layer.objects.active = bpy.data.objects['SkyboxCam.003']
        bpy.ops.view3d.object_as_camera()
        bpy.context.area.type = 'TIMELINE'
        bpy.ops.marker.camera_bind()

        bpy.context.scene.frame_current = 4
        bpy.ops.marker.add()
        bpy.context.area.type = 'VIEW_3D'
        bpy.context.view_layer.objects.active = bpy.data.objects['SkyboxCam.004']
        bpy.ops.view3d.object_as_camera()
        bpy.context.area.type = 'TIMELINE'
        bpy.ops.marker.camera_bind()

        bpy.context.scene.frame_current = 5
        bpy.ops.marker.add()
        bpy.context.area.type = 'VIEW_3D'
        bpy.context.view_layer.objects.active = bpy.data.objects['SkyboxCam.005']
        bpy.ops.view3d.object_as_camera()
        bpy.context.area.type = 'TIMELINE'
        bpy.ops.marker.camera_bind()

        bpy.context.scene.frame_current = 6
        bpy.ops.marker.add()
        bpy.context.area.type = 'VIEW_3D'
        bpy.context.view_layer.objects.active = bpy.data.objects['SkyboxCam.006']
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
# Move Selection to Zero
class SY_OT_FindNgons(bpy.types.Operator):
    bl_idname = "mesh.sy_find_ngons"
    bl_label = "Find Ngons (Sy)"
    bl_description = "Shortcut for select_face_by_sides(number=4, type='GREATER')"

    def execute(self, context):
        #Deselect all
        bpy.ops.mesh.select_all(action='DESELECT')

        #Select ngons
        bpy.ops.mesh.select_face_by_sides(number=4, type='GREATER')

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
        context.scene.cursor.location = obj.matrix_world @ point
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


#************************************************************************************
# Add Seams on Border

# class SY_OT_TransformFromSelection(bpy.types.Operator):
#     bl_idname = "mesh.sy_transform_from_selection"
#     bl_label = "Transform from Selection (Sy)"
#     bl_description = "Create and set a Transform Orientation based on the current selection."
#
#     def execute(self, context):
#
#         #Delete existing
#         # for slot in bpy.context.scene.transform_orientation_slots:
#         #     print(slot.type)
#         #     if slot.type != 'DEFAULT':
#         #     #if slot.custom_orientation is None:
#         #         print("Not a custom slot")
#         #         continue
#         #     if slot.custom_orientation.name == "SY":
#         #         print("Found SY")
#         #         bpy.ops.transform.select_orientation(orientation='SY')
#         #         bpy.ops.transform.delete_orientation()
#         #         break
#         # bpy.ops.transform.select_orientation(orientation='SY')
#         # bpy.ops.transform.delete_orientation()
#
#         #Create new
#         bpy.ops.transform.create_orientation(use=True)
#         bpy.context.scene.transform_orientation_slots[0].custom_orientation.name = "SY"
#
#         return {'FINISHED'}


#************************************************************************************
# Create Bounds

class SY_OT_SyCreateBounds_FromObjects(bpy.types.Operator):
    bl_idname = "object.sy_create_bounds_from_objects"
    bl_label = "Create Bounding Boxes from Objects (Sy)"
    bl_description = "Create a BoundingBox for each selected Object"

    def execute(self, context):

        selected = bpy.context.selected_objects

        for obj in selected:
            #ensure origin is centered on bounding box center
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
            #create a cube for the bounding box
            bpy.ops.mesh.primitive_cube_add()
            #our new cube is now the active object, so we can keep track of it in a variable:
            bound_box = bpy.context.active_object

            #copy transforms
            bound_box.dimensions = obj.dimensions
            bound_box.location = obj.location
            bound_box.rotation_euler = obj.rotation_euler

            #rename
            bound_box.name = "UBX_" + bound_box.name + "_.000"

            #display as collision
            bpy.context.object.display_type = 'WIRE'
            bpy.context.object.show_in_front = True

        #select old
        bpy.ops.object.select_all(action='DESELECT')
        for obj in selected:
            obj.select_set(state=True)

        return {'FINISHED'}

#------------------------------------------------------------------------------------

class SY_OT_SyCreateBounds_FromVertices(bpy.types.Operator):
    bl_idname = "object.sy_create_bounds_from_vertices"
    bl_label = "Create Bounding Boxes from Vertices (Sy)"
    bl_description = "Create a BoundingBox along that envelopes the selected vertices"

    def execute(self, context):
        #Save active object
        obj = context.active_object

        #Get the active space
        active_space = bpy.context.scene.transform_orientation_slots[0]

        # #Get selected vertices (locally)
        bm = bmesh.from_edit_mesh(obj.data)
        verts = [v for v in bm.verts if v.select]

        #Find extent
        Max_X = -sys.float_info.max
        Min_X = sys.float_info.max
        Max_Y = -sys.float_info.max
        Min_Y = sys.float_info.max
        Max_Z = -sys.float_info.max
        Min_Z = sys.float_info.max
        for vert in verts:
            #Get coordinate
            if active_space.type == 'GLOBAL':
                co_final = obj.matrix_world @ vert.co
            elif active_space.type == 'LOCAL':
                co_final = vert.co
            elif active_space.custom_orientation:
                co_final = obj.matrix_world @ vert.co
                co_final = active_space.custom_orientation.matrix.inverted() @ co_final

            #Get bounding box
            if co_final[0] > Max_X:
                Max_X = co_final[0]
            if co_final[0] < Min_X:
                Min_X = co_final[0]
            if co_final[1] > Max_Y:
                Max_Y = co_final[1]
            if co_final[1] < Min_Y:
                Min_Y = co_final[1]
            if co_final[2] > Max_Z:
                Max_Z = co_final[2]
            if co_final[2] < Min_Z:
                Min_Z = co_final[2]

        #leave the active object
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')

        #create a cube for the bounding box
        bpy.ops.mesh.primitive_cube_add()
        #our new cube is now the active object, so we can keep track of it in a variable:
        bound_box = bpy.context.active_object

        #calculate center
        box_location = mathutils.Vector(((Min_X + Max_X) / 2, (Min_Y + Max_Y) / 2, (Min_Z + Max_Z) / 2))

        #copy transforms
        if active_space.type == 'LOCAL':
            #print("DEBUG: local")
            bound_box.location = obj.matrix_world @ box_location
            bound_box.rotation_euler = obj.rotation_euler

        elif active_space.type == 'GLOBAL':
            #print("DEBUG: global")
            bound_box.location = box_location

        elif active_space.custom_orientation:
            #print("DEBUG: custom")
            bound_box.location = active_space.custom_orientation.matrix @ box_location
            bound_box.rotation_euler = active_space.custom_orientation.matrix.to_euler()

        else:
            #print("DEBUG: transform orientation not recognized")
            print(bpy.context.scene.type)

        bound_box.dimensions = Max_X - Min_X, Max_Y - Min_Y, Max_Z - Min_Z

        #rename
        bound_box.name = "UBX_" + obj.name + "_.000"

        #display as collision
        bpy.context.object.display_type = 'WIRE'
        bpy.context.object.show_in_front = True

        #return to initial state
        bpy.ops.object.select_all(action='DESELECT')
        bound_box.select_set(state=False)
        obj.select_set(state=True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}

#------------------------------------------------------------------------------------

class SY_OT_SyCreateCollision_Complex_FromFloor(bpy.types.Operator):
    bl_idname = "object.sy_create_collision_complex_from_floor"
    bl_label = "Create Complex Collider from Floors (Sy)"
    bl_description = "Create a complex collider based on the selected floors"

    def execute(self, context):

        return {'FINISHED'}

#------------------------------------------------------------------------------------

class SY_OT_SyCreateCollision_Simple_FromFloor(bpy.types.Operator):
    bl_idname = "object.sy_create_collision_simple_from_floor"
    bl_label = "Create Simple Colliders from Floors (Sy)"
    bl_description = "Create simple colliders based on the selected floors"

    def execute(self, context):

        # Enable Pivot
        def get_override(area_type, region_type):
            for area in bpy.context.screen.areas:
                if area.type == area_type:
                    for region in area.regions:
                        if region.type == region_type:
                            override = {'area': area, 'region': region}
                            return override
                            #error message if the area or region wasn't found
                            raise RuntimeError("Wasn't able to find", region_type," in area ", area_type, "Make sure it's open while executing script.")
        bpy.context.scene.tool_settings.transform_pivot_point = 'MEDIAN_POINT'
        override = get_override( 'VIEW_3D', 'WINDOW' )

        original_floors = bpy.context.selected_objects

        # Create unscaled duplicates
        bpy.ops.object.duplicate()
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
        floors_unscaled = bpy.context.selected_objects

        # Create volumes from the floors
        bpy.ops.object.duplicate()
        original_floor_volumes = bpy.context.selected_objects

        # Expand
        for floor in original_floor_volumes:
            bpy.context.view_layer.objects.active = floor
            bpy.ops.object.modifier_add(type='SOLIDIFY')
            bpy.context.object.modifiers["Solidify"].offset = 1
            bpy.context.object.modifiers["Solidify"].thickness = 2.8
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Solidify")

        # Create a bounding box
        bpy.ops.object.duplicate()
        bpy.ops.transform.resize(override, value=(1.2, 1.2, 1), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
        bpy.ops.object.join()
        expanded_floor_volume = bpy.context.active_object

        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
        bpy.ops.mesh.primitive_cube_add()
        bound_box = bpy.context.active_object
        bound_box.dimensions = expanded_floor_volume.dimensions
        bound_box.location = expanded_floor_volume.location
        bound_box.rotation_euler = expanded_floor_volume.rotation_euler
        bound_box.name = "FloorCollider.000"

        #display as wire
        bpy.context.object.display_type = 'WIRE'
        bpy.context.object.show_in_front = True

        # Delete expanded floor volume
        bpy.ops.object.select_all(action='DESELECT')
        expanded_floor_volume.select_set(state=True)
        bpy.ops.object.delete(use_global=False, confirm=False)

        # Create a floor collider
        bpy.ops.object.select_all(action='DESELECT')
        bound_box.select_set(state=True)
        bpy.ops.object.duplicate()
        bpy.ops.transform.translate(override, value=(0, 0, -2.8), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        floor_collider = bpy.context.active_object

        # Cut out each floor
        for floor_volume in original_floor_volumes:

            # Scale up pure volume to ensure a clean cut through
            bpy.ops.object.select_all(action='DESELECT')
            floor_volume.select_set(state=True)
            bpy.context.view_layer.objects.active = floor_volume
            bpy.ops.transform.translate(override, value=(0, 0, -1), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
            bpy.ops.transform.resize(override, value=(1, 1, 2), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

            #display as wire
            bpy.context.object.display_type = 'WIRE'
            bpy.context.object.show_in_front = True

            # Create bool fix volume
            bpy.ops.object.duplicate()
            bpy.ops.object.modifier_add(type='SOLIDIFY')
            bpy.context.object.modifiers["Solidify"].offset = 0.0
            floor_volume_bool_fix = bpy.context.active_object

            # Cut out bool fix volume
            bpy.ops.object.select_all(action='DESELECT')
            bound_box.select_set(state=True)
            bpy.context.view_layer.objects.active = bound_box
            bpy.ops.object.modifier_add(type='BOOLEAN')
            bpy.context.object.modifiers["Boolean"].object = floor_volume_bool_fix
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Boolean")

            # Cut out pure volume
            bpy.ops.object.select_all(action='DESELECT')
            bound_box.select_set(state=True)
            bpy.context.view_layer.objects.active = bound_box
            bpy.ops.object.modifier_add(type='BOOLEAN')
            bpy.context.object.modifiers["Boolean"].object = floor_volume
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Boolean")

            # Clean up
            bpy.ops.object.select_all(action='DESELECT')
            floor_volume_bool_fix.select_set(state=True)
            bpy.context.view_layer.objects.active = floor_volume_bool_fix
            bpy.ops.object.delete(use_global=False, confirm=False)

        # Clean up
        bpy.ops.object.select_all(action='DESELECT')
        for delete_me in original_floor_volumes:
            delete_me.select_set(state=True)
        for delete_me in floors_unscaled:
            delete_me.select_set(state=True)
        bpy.ops.object.delete(use_global=False, confirm=False)

        return {'FINISHED'}

#************************************************************************************
# Split from bound selection

class SY_OT_SySplitBounds(bpy.types.Operator):
    bl_idname = "object.sy_split_bounds"
    bl_label = "Split along Seam (Sy)"
    bl_description = "Splits a mesh along a seam and closes the holes"

    def execute(self, context):

        bpy.ops.mesh.rip('INVOKE_DEFAULT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.edge_face_add()
        bpy.ops.mesh.f2()
        bpy.ops.mesh.separate(type='LOOSE')
        bpy.ops.object.mode_set(mode='OBJECT')

        return {'FINISHED'}


#************************************************************************************
# UV Origin Operations

class SY_OT_SyApplyUVOrigin(bpy.types.Operator):
    bl_idname = "object.sy_apply_uv_origin"
    bl_label = "Apply UV-Origin (Sy)"
    bl_description = "Remaps all first UV channels of the selected Objects.\nIf an origin is selected, it will be applied and saved into the selected objects.\nIf no origin is selected, the saved origin or the world origin is used."

    def execute(self, context):

        #find origin
        origin = None
        selected = bpy.context.selected_objects
        for obj in selected:
            if obj.name[:9] == "UV_Origin":
                print("DEBUG: found origin")
                origin = obj
                break

        #iterate over selected objects
        for obj in selected:

            #skip origin
            if obj.name[:9] == "UV_Origin":
                print("DEBUG: skipping the object as it is an origin")
                continue
            else:
                print("DEBUG: processing object")

            #store or read origin
            origin_property_name = "UVOrigin"
            if origin != None:
                print("DEBUG: saving origin to object")
                obj[origin_property_name] = origin

            elif obj.get(origin_property_name) is not None:
                print("DEBUG: reading origin from object")
                origin = obj[origin_property_name]

            #get origin transformation
            mat_origin = mathutils.Matrix()
            if origin != None:
                mat_origin = origin.matrix_world.inverted()
            rot_origin = mat_origin.to_quaternion()

            #iterate over polys
            for face in obj.data.polygons:

                #gather object transform
                mat_obj = obj.matrix_world
                rot_obj = mat_obj.to_quaternion()

                #gather normal data
                nor_obj_space = face.normal
                nor_world_space = rot_obj @ nor_obj_space
                tan_world_space = mathutils.Vector.cross(nor_world_space, (0.0, 0.0, 1.0))

                nor_origin_space = rot_origin @ nor_world_space
                tan_origin_space = rot_origin @ tan_world_space

                #flip tangent?
                flip_tangent = False
                tan_oriented_origin_space = tan_origin_space #(abs(tan_origin_space[0]), abs(tan_origin_space[1]), abs(tan_origin_space[2]))
                if abs(tan_origin_space[0]) > abs(tan_origin_space[1]):
                    #flows right
                    if(tan_origin_space[0] < 0.0):
                        flip_tangent = True
                else:
                    #flows up
                    if(tan_origin_space[1] < 0.0):
                        flip_tangent = True

                #flip if required
                if flip_tangent:
                    tan_oriented_origin_space = (-tan_origin_space[0], -tan_origin_space[1], tan_origin_space[2])

                #evaluate normal
                poly_is_vertical = abs(nor_origin_space[2]) < 0.8

                #iterate over vertices
                for vert_idx, loop_idx in zip(face.vertices, face.loop_indices):
                    #uv_coords = obj.data.uv_layers.active.data[loop_idx].uv
                    #print("face idx: %i, vert idx: %i, uvs: %f, %f" % (face.index, vert_idx, uv_coords.x, uv_coords.y))

                    #Gather location data
                    vert = obj.data.vertices[vert_idx]
                    vert_world_space = obj.matrix_world @ vert.co

                    #Calculate new coords
                    vert_origin_space = mat_origin @ vert_world_space
                    vert_x_tangent_space = mathutils.Vector.dot(vert_origin_space, tan_oriented_origin_space)

                    #is_vertical = vert_final.
                    if poly_is_vertical:
                        uv_coords = (vert_x_tangent_space, vert_origin_space[2])
                    else:
                        uv_coords = (vert_origin_space[0], vert_origin_space[1])

                    #Apply
                    if obj.data.uv_layers.active == None:
                        obj.data.uv_layers.new(name = "Texture")
                    obj.data.uv_layers[0].data[loop_idx].uv = uv_coords

        return {'FINISHED'}

#------------------------------------------------------------------------------------

class SY_OT_SyAddUVOrigin(bpy.types.Operator):
    bl_idname = "object.sy_add_uv_origin"
    bl_label = "Add UV-Origin (Sy)"
    bl_description = "Creates a UV-Origin.\nPlace and rotate it to define the origin of the UV."

    def execute(self, context):

        #bpy.ops.object.empty_add(type='CONE', align='WORLD', location=(bpy.context.scene.cursor.location), rotation=(1.5708, 0, 0))
        bpy.ops.object.empty_add(type='SPHERE', location=bpy.context.scene.cursor.location)
        bpy.context.active_object.name = "UV_Origin.000"

        return {'FINISHED'}

#------------------------------------------------------------------------------------

class SY_OT_SyPreviewUV(bpy.types.Operator):
    bl_idname = "object.sy_preview_uv"
    bl_label = "Preview UV (Sy)"
    bl_description = "Switches between the applied materials and a preview material.\nThe materials will be stored in the custom properties."

    def execute(self, context):
        #Attributes
        mat_name = "UV_Preview"
        mat_preview = None

        #Find Material
        for mat in bpy.data.materials:
            if mat.name == mat_name:
                mat_preview = mat
                break

        #Create Material
        if mat_preview == None:
            #create texture
            color_grid = None
            texture_name = "ColorGrid"
            bpy.ops.image.new(name=texture_name, width=1024, height=1024, generated_type="COLOR_GRID")
            for img in bpy.data.images:
                if img.name == texture_name:
                    color_grid = img

            #create material
            mat_preview = bpy.data.materials.new(name = mat_name)
            mat_preview.use_nodes = True
            bsdf = mat_preview.node_tree.nodes["Principled BSDF"]
            image_node = mat_preview.node_tree.nodes.new('ShaderNodeTexImage')
            image_node.image = color_grid
            mat_preview.node_tree.links.new(bsdf.inputs['Base Color'], image_node.outputs['Color'])

        #Iterate over material slots of objects
        enabled_preview = False
        selected = bpy.context.selected_objects
        for obj in selected:

            for i in range(len(obj.material_slots)):
                slot_name = "MatPrev_%02d" % (i,)

                #toggle?
                applied_material_is_preview = obj.material_slots[i].material == mat_preview
                has_restorable_material = obj.get(slot_name) is not None

                enable_preview = not applied_material_is_preview
                restore_material = applied_material_is_preview and has_restorable_material

                #reapply original material?
                if restore_material:
                    obj.material_slots[i].material = obj[slot_name]
                    del obj[slot_name]

                #apply preview material?
                if enable_preview:
                    obj[slot_name] = obj.material_slots[i].material
                    obj.material_slots[i].material = mat_preview
                    enabled_preview = True

        if enabled_preview:
            bpy.context.space_data.shading.type = 'MATERIAL'

        return {'FINISHED'}

#------------------------------------------------------------------------------------

class SY_OT_EnableMaterialNodes(bpy.types.Operator):
    bl_idname = "object.sy_enable_material_nodes"
    bl_label = "Enable Material Nodes (Sy)"
    bl_description = "Makes all materials of the selected objects use nodes."

    def execute(self, context):
        #Iterate over material slots of objects
        selected = bpy.context.selected_objects
        for obj in selected:

            for mat_slot in obj.material_slots:
                mat_slot.material.use_nodes = True

        return {'FINISHED'}

#------------------------------------------------------------------------------------

class SY_OT_FixZeroAlphas(bpy.types.Operator):
    bl_idname = "object.sy_fix_zero_alphas"
    bl_label = "Fix Zero Alphas (Sy)"
    bl_description = "Sets alphas that are 0 to 1 on all materials of the selected objects."

    def execute(self, context):
        #Iterate over material slots of objects
        selected = bpy.context.selected_objects
        for obj in selected:

            for mat_slot in obj.material_slots:
                bsdf = mat_slot.material.node_tree.nodes["Principled BSDF"]
                if bsdf is None:
                    continue
                if bsdf.inputs['Alpha'].default_value == 0.0:
                    bsdf.inputs['Alpha'].default_value = 1.0

        return {'FINISHED'}

#------------------------------------------------------------------------------------

class SY_OT_ReduceMaterials(bpy.types.Operator):
    bl_idname = "object.sy_reduce_materials"
    bl_label = "Reduce Materials (Sy)"

    def execute(self, context):

        ModeAtStart = bpy.context.object.mode
        bpy.ops.object.mode_set(mode='OBJECT')
        SelectedAtStart = bpy.context.view_layer.objects.active

        #Iterate through Objects
        ObjectsToSetUp = bpy.context.selected_objects
        if len(ObjectsToSetUp) > 0:
            for iObject in ObjectsToSetUp:
                if iObject.type == 'MESH':

                    #Set Object Active
                    bpy.context.view_layer.objects.active = iObject

                    #Go through Materials
                    IsDone = False;
                    CurrentMaterialID = 0
                    while not IsDone:
                        #Mode
                        bpy.ops.object.mode_set(mode='EDIT')
                        bpy.ops.mesh.select_mode(type="FACE")

                        #Deselect Mesh
                        bpy.ops.mesh.select_all(action='DESELECT')

                        #Select Current Material
                        bpy.context.object.active_material_index = CurrentMaterialID

                        #Select Assigned
                        bpy.ops.object.material_slot_select()

                        #Mode
                        bpy.ops.object.mode_set(mode='OBJECT')

                        #Get selected
                        FoundSelectedMesh = False
                        for p in iObject.data.polygons:
                            if p.select == True:
                                FoundSelectedMesh = True
                                break

                        #Found?
                        if FoundSelectedMesh == True:
                            #Iterate
                            CurrentMaterialID += 1
                        else:
                            bpy.ops.object.material_slot_remove()

                        #Next Slot exists?
                        if CurrentMaterialID >= len(iObject.data.materials):
                            IsDone = True


        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.view_layer.objects.active = SelectedAtStart
        bpy.ops.object.mode_set(mode = ModeAtStart)

        return {'FINISHED'}

#------------------------------------------------------------------------------------

class SY_OT_SySplitOnSeams(bpy.types.Operator):
    bl_idname = "object.sy_clean_all_connections"
    bl_label = "Cleans all Face Connections (Sy)"
    bl_description = "Splits all selected objects into already disconnected faces and faces disconnected by seams."

    def execute(self, context):

        ModeAtStart = bpy.context.object.mode
        bpy.ops.object.mode_set(mode='OBJECT')
        SelectedAtStart = bpy.context.view_layer.objects.active

        #Iterate through Objects
        ObjectsToSetUp = bpy.context.selected_objects
        if len(ObjectsToSetUp) > 0:
            for iObject in ObjectsToSetUp:
                if iObject.type == 'MESH':

                    #Set Object Active
                    bpy.context.view_layer.objects.active = iObject

                    #Mode
                    bpy.ops.object.mode_set(mode='EDIT')

                    #Clean all
                    IsDone = False;
                    while not IsDone:
                        #Hide selected faces
                        bpy.ops.mesh.hide(unselected=False)

                        #Still Polys visible?
                        Mesh = bmesh.from_edit_mesh(iObject.data)
                        UnhiddenPolys = [f for f in Mesh.faces if f.hide == False]
                        if len(UnhiddenPolys) == 0:
                            IsDone = True;
                        else:
                            #Select random face
                            UnhiddenPolys[0].select = True;

                            #Run CleanConnections
                            bpy.ops.object.sy_clean_connections()

                            #Hide Faces
                            bpy.ops.mesh.hide(unselected=False)

                    #Unhide all
                    bpy.ops.mesh.reveal()


                    #Mode
                    bpy.ops.object.mode_set(mode='OBJECT')

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.view_layer.objects.active = SelectedAtStart
        bpy.ops.object.mode_set(mode = ModeAtStart)

        return {'FINISHED'}

#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
