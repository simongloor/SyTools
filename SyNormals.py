# (c) adsn 2012, Recalc Vertex Normals
# > edited by Pillars of Sy
# > edited by Raumgleiter AG
# 
# This addon manipulates vertex normals and stores them into an object
# property.
# 

#
# ***** BEGIN GPL LICENSE BLOCK *****
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ***** END GPL LICENCE BLOCK *****

  
import bmesh  
import bpy
import mathutils
import bgl
from bpy.types import Panel
from rna_prop_ui import PropertyPanel
from sys import float_info as fi

##########################################################
# draw UI ButtonS
class vertex_normals_ui(bpy.types.Panel):
    bl_idname = "SyNormals"
    bl_label = 'SyTools | Vertex Normals'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    
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


        # special editing
        box = self.layout.box()
        box.label(text='Extended Tools')

        # draw normals
        row = box.row(align=True)
        if context.window_manager.drawnormal:
            if context.window_manager.drawnormal == True:
                row.operator('object.draw_normals', text = 'Hide')
            elif context.window_manager.drawnormal == False:
                row.operator('object.draw_normals', text = 'Show')
        else:
            row.operator('object.draw_normals', text = 'Show')
        row.prop(context.scene.tool_settings, "normal_size", text="Size")


        # manage data
        col = box.column(align=True)
        col.label(text='Data')

        # save normals
        row = col.row(align=True)
        row.prop(context.window_manager, 'autosave', text = ' Autosave', toggle=True)
        row.operator('object.save_normals', text = 'Save')

        # update normals
        row = col.row(align=True)
        row.prop(context.window_manager, 'autoreload', text = ' Autoreload', toggle=True)
        row.operator('object.update_normal_list', text = 'Reload Normals')

        # clear
        row = col.row(align=True)
        row.operator('object.clear_normal', text = 'Clear')
        
        # copy and paste
        row = col.row(align=True)
        row.operator('object.copy_normal', text = 'Copy')
        row.operator('object.paste_normal', text = 'Paste')
        

        # manipulate normals simple
        col = box.column(align=True)
        col.label(text='Edit Manually')

        # selection tools
        row = col.row(align=True)
        row.operator('object.invert_selection', text = 'Inv Sel')
        row.operator('object.select_vertex', text = 'Cycle Sel')
        
        # simple manipulations
        row = col.row()
        row.column().prop(context.window_manager, 'customnormal2', expand = True, text='')
        row.prop(context.window_manager, 'customnormal1', text='')
        

        # manipulate normals complex
        col = box.column(align=True)
        col.label(text='Quick Tools')

        row = col.row(align=True)
        row.operator('object.invert_normal', text = 'Invert')
        row.operator('object.transfer_normal', text = 'Transfer')

        row = col.row(align=True)
        row.operator('object.tree_vertex_normals', text = 'Tree')
        row.operator('object.foliage_vertex_normals', text = 'Foliage')


        # autoreload saved normals when autoreload is activated
        if context.window_manager.autoreload == True:
            if context.active_object.mode != context.window_manager.reloadchange:
                if context.active_object.mode != 'EDIT':
                    context.window_manager.reload = not context.window_manager.reload
                    
            context.window_manager.reloadchange = context.active_object.mode
        
        if context.window_manager.autosave == True:
            if context.active_object.mode != context.window_manager.savechange:
                if context.active_object.mode != 'OBJECT':
                    context.window_manager.save = not context.window_manager.save

            context.window_manager.savechange = context.active_object.mode

##########################################################
# toggle vertices selection

##########################################################
# tree vertex normals
# process only selected vertices
# skip unselected to preserve normals on non transparent geometry

class tree_vertex_normals(bpy.types.Operator):
    bl_idname = 'object.tree_vertex_normals'
    bl_label = 'Vertex Normal Tree'
    bl_description = 'Align selected verts pointing away from 3d cursor'
        
    def execute(self, context):

        obj = context.active_object
        vert_index = len(bpy.context.active_object.data.vertices)
        vec1 = context.scene.cursor_location

        bpy.ops.object.mode_set(mode='OBJECT')

        if 'vertex_normal_list' not in context.active_object:
            context.active_object['vertex_normal_list'] = []
        if 'vertex_normal_list' in context.active_object:
            for i in range(vert_index):
                if context.active_object.data.vertices[i].select == True:
                    vec2 = obj.data.vertices[i].co
                    newvec = vec2 - vec1 + obj.location
                    newnormal = newvec.normalized()
    
                    obj.data.vertices[i].normal = newnormal
                
                # update vertex normal list
                if context.window_manager.autosave == True:
                    if len(context.object.vertex_normal_list) <= i:
                        item = context.object.vertex_normal_list.add()
                        item.normal = obj.data.vertices[i].normal
                    else:
                        context.object.vertex_normal_list[i]['normal'] = obj.data.vertices[i].normal
        
        bpy.ops.object.mode_set(mode='EDIT')
        context.area.tag_redraw()
        return {'FINISHED'}


##########################################################
# foliage vertex normals
# align selected verts to global z axis
# and unselected to 3d cursor

class foliage_vertex_normals(bpy.types.Operator):
    bl_idname = 'object.foliage_vertex_normals'
    bl_label = 'Vertex Normal Foliage'
    bl_description = 'Selected verts to Z axis, unselected away from 3d cursor'

    def execute(self, context):
        obj = context.active_object
        vert_index = len(bpy.context.active_object.data.vertices)
        vec1 = context.scene.cursor_location

        bpy.ops.object.mode_set(mode='OBJECT')
        
        if 'vertex_normal_list' not in context.active_object:
            context.active_object['vertex_normal_list'] = []
        if 'vertex_normal_list' in context.active_object:
            for i in range(vert_index):
                
                # selected verts will align on z-axis
                if context.active_object.data.vertices[i].select == True:
                    obj.data.vertices[i].normal = (0.0, 0.0, 1.0)
                
                # unselected verts will align on 3d cursor
                elif context.active_object.data.vertices[i].select == False:
                    vec2 = obj.data.vertices[i].co
                    newvec = vec2 - vec1 + obj.location
                    newnormal = newvec.normalized()
    
                    obj.data.vertices[i].normal = newnormal
                
                # update vertex normal list
                if context.window_manager.autosave == True:
                    if len(context.object.vertex_normal_list) <= i:
                        item = context.object.vertex_normal_list.add()
                        item.normal = obj.data.vertices[i].normal
                    else:
                        context.object.vertex_normal_list[i]['normal'] = obj.data.vertices[i].normal
        bpy.ops.object.mode_set(mode='EDIT')
        context.area.tag_redraw()
        return {'FINISHED'}



##########################################################
# custom vertex normal vector
## custom 1
def update_custom_normal1(self, context):

    obj = context.active_object
    if 'vertex_normal_list' not in context.active_object:
        context.active_object['vertex_normal_list'] = []
    if 'vertex_normal_list' in context.active_object:
        vert_index = len(context.active_object.data.vertices)
        for i in range(vert_index):
            # selected verts align on custom normal
            if context.active_object.data.vertices[i].select == True:
                obj.data.vertices[i].normal = context.window_manager.customnormal1
            
            # unselected verts are skipped 
            elif context.active_object.data.vertices[i].select == False:
                pass
            
            # update vertex normal list
            if context.window_manager.autosave == True:
                if len(context.object.vertex_normal_list) <= i:
                    item = context.object.vertex_normal_list.add()
                    item.normal = obj.data.vertices[i].normal
                else:
                    context.object.vertex_normal_list[i]['normal'] = obj.data.vertices[i].normal

## custom 2
def update_custom_normal2(self, context):

    obj = context.active_object
    if 'vertex_normal_list' not in context.active_object:
        context.active_object['vertex_normal_list'] = []
    if 'vertex_normal_list' in context.active_object:
        vert_index = len(context.active_object.data.vertices)
        for i in range(vert_index):
            # selected verts align on custom normal
            if context.active_object.data.vertices[i].select == True:
                obj.data.vertices[i].normal = context.window_manager.customnormal2
            
            # unselected verts are skipped 
            elif context.active_object.data.vertices[i].select == False:
                pass
            # update vertex normal list
            if context.window_manager.autosave == True:
                if len(context.object.vertex_normal_list) <= i:
                    item = context.object.vertex_normal_list.add()
                    item.normal = obj.data.vertices[i].normal
                else:
                    context.object.vertex_normal_list[i]['normal'] = obj.data.vertices[i].normal


##########################################################
# select next vertex
class select_vertex(bpy.types.Operator):
    bl_idname = 'object.select_vertex'
    bl_label = 'Select Vertex'
    bl_description = 'Toggles through vertices'

    def execute(self, context):
        obj = context.active_object
        vert_index = len(context.active_object.data.vertices)
        
        if 'select_vertex' not in context.active_object:
            context.active_object['select_vertex'] = 0
    
        if 'select_vertex' in context.active_object:
            
            for h in range(vert_index):
                if context.active_object.data.vertices[h].select == True:
                    obj['select_vertex'] = h
 
            if obj['select_vertex'] < vert_index-1:
                obj['select_vertex'] += 1
            else:
                obj['select_vertex'] = 0

            # select next vertex
            for i in range(vert_index):
                
                if i == obj['select_vertex']:
                    context.active_object.data.vertices[i].select = True
                else:
                    context.active_object.data.vertices[i].select = False

            return {'FINISHED'}  
##########################################################
# invert vertex selection
class invert_selection(bpy.types.Operator):
    bl_idname = 'object.invert_selection'
    bl_label = 'Invert Selection'
    bl_description = 'Inverts Selected Vertices'

    def execute(self, context):
        obj = context.active_object
        vert_index = len(context.active_object.data.vertices)
        # invert selection
        for i in range(vert_index):
            
            if context.active_object.data.vertices[i].select == True:
                context.active_object.data.vertices[i].select = False
            else:
                context.active_object.data.vertices[i].select = True

        return {'FINISHED'}
##########################################################
# reload function called after leaving edit mode (autoreload)
def reload(self, context):
    vertices = context.active_object.data.vertices
    obj = context.active_object
    
    for i in range(len(obj.vertex_normal_list)):
        vertices[i].normal = obj.vertex_normal_list[i]['normal']
    
    context.area.tag_redraw()

##########################################################
# save function called after leaving object mode (autosave)
def save(self, context):
    obj = context.active_object
    vert_index = len(bpy.context.active_object.data.vertices)
        
    if 'vertex_normal_list' not in context.active_object:
        context.active_object['vertex_normal_list'] = []
        
    if 'vertex_normal_list' in context.active_object:
        for i in range(vert_index):
           
            # update vertex normal list
            if len(context.object.vertex_normal_list) <= i:
                item = context.object.vertex_normal_list.add()
                item.normal = obj.data.vertices[i].normal
            # add items to list if too short
            else:
                context.object.vertex_normal_list[i]['normal'] = obj.data.vertices[i].normal

##########################################################
# copy normal
class copy_normal(bpy.types.Operator):
    bl_idname = 'object.copy_normal'
    bl_label = 'Copy Normal'
    bl_description = 'Copies normal from selected Vertex'

    def execute(self, context):
        context.window_manager.save = not context.window_manager.save
        bpy.ops.object.mode_set(mode='OBJECT')
        context.window_manager.reload = not context.window_manager.reload
        
        obj = context.active_object
        vert_index = len(context.active_object.data.vertices)

        check = 0
        # inverse selection
        for h in range(vert_index):
            if context.active_object.data.vertices[h].select == True:
                check += 1
        if check == 1:
            for i in range(vert_index):
                if context.active_object.data.vertices[i].select == True:
                    context.window_manager.copynormal = context.active_object.data.vertices[i].normal
                
#                if context.window_manager.autosave == True:
#                    if len(context.object.vertex_normal_list) <= i:
#                        item = context.object.vertex_normal_list.add()
#                        item.normal = obj.data.vertices[i].normal
#                    else:
#                        context.object.vertex_normal_list[i]['normal'] = obj.data.vertices[i].normal
        else:
            self.report({'INFO'}, 'please select a single vertex')
        
        bpy.ops.object.mode_set(mode='EDIT')
        return {'FINISHED'}

##########################################################
# paste normal
class paste_normal(bpy.types.Operator):
    bl_idname = 'object.paste_normal'
    bl_label = 'Paste Normal'
    bl_description = 'Paste normal to selected Vertex'

    def execute(self, context):
        context.window_manager.save = not context.window_manager.save
        bpy.ops.object.mode_set(mode='OBJECT')
        context.window_manager.reload = not context.window_manager.reload
        
        obj = context.active_object
        vert_index = len(context.active_object.data.vertices)
        
        check = 0
        # inverse selection
        if 'select_vertex' not in context.active_object:
            context.active_object['select_vertex'] = 0
    
        if 'select_vertex' in context.active_object:
            for h in range(vert_index):
                if context.active_object.data.vertices[h].select == True:
                    check += 1
            if check >= 1:
                for i in range(vert_index):
                    if context.active_object.data.vertices[i].select == True:
                        context.active_object.data.vertices[i].normal = context.window_manager.copynormal
                        
#                    if context.window_manager.autosave == True:
#                        if len(context.object.vertex_normal_list) <= i:
#                            item = context.object.vertex_normal_list.add()
#                            item.normal = obj.data.vertices[i].normal
#                        else:
#                            context.object.vertex_normal_list[i]['normal'] = obj.data.vertices[i].normal
            else:
                self.report({'INFO'}, 'please select at least one vertex')
        
        context.window_manager.save = not context.window_manager.save
        bpy.ops.object.mode_set(mode='EDIT')
        context.area.tag_redraw()
        return {'FINISHED'}

##########################################################
# clear normals
class clear_normal(bpy.types.Operator):
    bl_idname = 'object.clear_normal'
    bl_label = 'Clear Normal'
    bl_description = 'Reset the Normals'

    def execute(self, context):
        
        context.window_manager.autoreload = False
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()

        return {'FINISHED'}

##########################################################
# invert normals
class invert_normal(bpy.types.Operator):
    bl_idname = 'object.invert_normal'
    bl_label = 'Invert Normal'
    bl_description = 'Invert selected Normals'

    def execute(self, context):

        obj = context.active_object
        if 'vertex_normal_list' not in context.active_object:
            context.active_object['vertex_normal_list'] = []
        if 'vertex_normal_list' in context.active_object:
            vert_index = len(context.active_object.data.vertices)
            for i in range(vert_index):
                # selected verts align on custom normal
                if context.active_object.data.vertices[i].select == True:
                    obj.data.vertices[i].normal = -obj.data.vertices[i].normal
                
                # unselected verts are skipped 
                elif context.active_object.data.vertices[i].select == False:
                    pass
                # update vertex normal list
                if context.window_manager.autosave == True:
                    if len(context.object.vertex_normal_list) <= i:
                        item = context.object.vertex_normal_list.add()
                        item.normal = obj.data.vertices[i].normal
                    else:
                        context.object.vertex_normal_list[i]['normal'] = obj.data.vertices[i].normal

        return {'FINISHED'}

##########################################################
# transfer normals

def nearestVertexNormal(sourceverts, vert, MAXDIST):
    '''
    Acquire Vector normal of nearest-location sourcevert to vert.
    sourceverts = BMVertSeq, source object verts 
    vert = Vector, comparison vert coordinate 
    MAXDIST = float, max distance to consider nearest 
    '''
    nearest = None
    nearestdist = fi.max
    if MAXDIST == 0.0:
        MAXDIST = fi.max
    
    for svert in sourceverts:
        dist = (vert.co - svert.co).magnitude
        if dist < nearestdist and dist < MAXDIST:
            nearest = svert
            nearestdist = dist
    if nearest:
        return nearest.normal
    else:
        return

def gatherSourceVerts(bmsrc, src, scene, BOUNDS):
    '''
    Adjust source BMesh for providing desired source normals.
    bmsrc = BMesh, should be empty
    src = Object, source to acquire verts from
    scene = Scene, generally context.scene; required for src.to_mesh
    BOUNDS = str, whether to include, ignore, or only use boundary edges
    '''
    bmsrc.from_mesh(src.to_mesh(scene, True, 'PREVIEW'))
    bmsrc.transform(src.matrix_world)
    
    if BOUNDS != 'INCLUDE':
        invalidverts = []
        boundaryvert = False
        for edge in bmsrc.edges:
            if BOUNDS == 'IGNORE':
                # Boundary verts are invalid
                if len(edge.link_faces) < 2:
                    for vert in edge.verts:
                        invalidverts.append(vert)
            else:
                # Internal verts are invalid
                if len(edge.link_faces) > 1:
                    for vert in edge.verts:
                        for edge in vert.link_edges:
                            if len(edge.link_faces) < 2:
                                boundaryvert = True
                                break
                        if boundaryvert:
                            boundaryvert = False
                            continue
                        else:
                            invalidverts.append(vert)
        for vert in invalidverts:
            if vert.is_valid:
                bmsrc.verts.remove(vert)

def joinBoundaryVertexNormals(self, context, destobjs,
                              INFL=0.0, MAXDIST=0.01):
    '''
    Average smoothing over boundary verts, usually same-location.
    destobjs = list, generally context.selected_objects
    INFL = float, influence strength
    MAXDIST = float, distance to influence... probably not necessary
    '''
    bms = {}
    bmsrc = bmesh.new()
    scene = context.scene
    
    for obj in destobjs:
        # These type != 'MESH' checks could be alleviated by removing
        #  non-mesh objects in execute(), but, may wish to
        #  support non-mesh objects one day
        if obj.type != 'MESH':
            continue
        bms[obj.name] = bmesh.new()
        bm = bms[obj.name]
        bm.from_mesh(obj.to_mesh(scene, False, 'PREVIEW'))
        bm.transform(obj.matrix_world)
        destverts = bm.verts
        
        for otherobj in destobjs:
            if otherobj.type != 'MESH' or obj == otherobj:
                continue
            gatherSourceVerts(bmsrc, otherobj, scene, 'ONLY')
            sourceverts = bmsrc.verts
            
            for vert in destverts:
                near = nearestVertexNormal(sourceverts, vert, MAXDIST)
                if near:
                    offset = near * INFL
                    vert.normal = (vert.normal + offset) * 0.5
                    vert.normal.normalize()
            bmsrc.clear()
    
    for name in bms:
        # Everything's been modified by everything else's original state,
        #  time to apply the modified data to the original objects
        bm = bms[name]
        for obj in destobjs:
            if obj.name == name:
                bm.transform(obj.matrix_world.inverted())
                bm.to_mesh(obj.data)
                bm.free()
    bmsrc.free()

def transferVertexNormals(self, context, src, destobjs,
                          INFL=1.0, MAXDIST=0.00, BOUNDS='IGNORE'):
    '''
    Transfer smoothing from one object to other selected objects.
    src = source object to transfer from 
    destobjs = list of objects to influence 
    INFL = influence strength 
    MAXDIST = max distance to influence 
    BOUNDS = ignore/include/only use boundary edges
    '''
    bm = bmesh.new()
    bmsrc = bmesh.new()
    scene = context.scene
    gatherSourceVerts(bmsrc, src, scene, BOUNDS)
    sourceverts = bmsrc.verts
    
    for obj in destobjs:
        if obj.type != 'MESH' or obj == src:
            continue
        bm.from_mesh(obj.to_mesh(scene, False, 'PREVIEW'))
        bm.transform(obj.matrix_world)
        destverts = bm.verts
        
        for vert in destverts:
            near = nearestVertexNormal(sourceverts, vert, MAXDIST)
            if near:
                offset = near
                if INFL < 0.0:
                    offset = offset * -1
                vert.normal = vert.normal.lerp(offset,abs(INFL))
                vert.normal.normalize()
        
        bm.transform(obj.matrix_world.inverted())
        bm.to_mesh(obj.data)
        bm.clear()
    
    bm.free()

class transfer_normal(bpy.types.Operator):
    ''' 
    Transfers nearest worldspace vertex normals from active object to selected.
    When 'Boundary Edges' is set to Only, each object checks all other objects.
    Example uses: baking, mollifying lowpoly foliage, hiding sub-object seams.
    '''
    bl_idname = "object.transfer_normal"
    bl_label = "Transfer Vertex Normals"
    bl_description = "Transfer shading from active object to selected objects."
    bl_options = {'REGISTER', 'UNDO'}
    
    influence = bpy.props.FloatProperty(
            name='Influence',
            description='TransferD strength, negative inverts',
            subtype='FACTOR',
            min=-1.0,
            max=1.0,
            default=1.0
            )
    maxdist = bpy.props.FloatProperty(
            name='Distance',
            description='Transfer distance, 0 for infinite',
            subtype='DISTANCE',
            unit='LENGTH',
            min=0.0,
            max=fi.max,
            soft_max=20.0,
            default=0.00
            )
    bounds = bpy.props.EnumProperty(
            name='Boundary Edges',
            description="Management for single-face edges.",
            items=[('IGNORE', 'Ignore', 'Discard source boundary edges.'),
                   ('INCLUDE', 'Include', 'Include source boundary edges.'),
                   ('ONLY', 'Only', 'Operate only on boundary edges.')],
            default='IGNORE'
            )
    
    def execute(self,context):
        src = context.active_object
        destobjs = context.selected_objects
        
        if context.mode != 'OBJECT':
            self.report({'ERROR'},'Must be performed in object mode')
            return{'CANCELLED'}
        if not src or not isinstance(src.data, bpy.types.Mesh):
            self.report({'ERROR'},'No active object with mesh data')
            return{'CANCELLED'}
        if len(destobjs) < 2:
            self.report({'ERROR'},'Requires two or more objects')
            return{'CANCELLED'}
        
        if self.influence != 0.0:
            if self.bounds != 'ONLY':
                transferVertexNormals(
                    self, context, src, destobjs,
                    INFL=self.influence,
                    MAXDIST=self.maxdist,
                    BOUNDS=self.bounds)
            else:
                joinBoundaryVertexNormals(
                    self, context, destobjs,
                    INFL=self.influence,
                    MAXDIST=self.maxdist)
        return {'FINISHED'}

##########################################################
##########################################################
# save all vertexnormals
class save_normals(bpy.types.Operator):

    bl_idname = 'object.save_normals'
    bl_label = 'Save Normals'
    bl_description = 'Save Vertex Normals'
        
    def execute(self, context):
        obj = context.active_object
        vert_index = len(bpy.context.active_object.data.vertices)


        #bpy.ops.object.mode_set(mode='OBJECT')        
        if 'vertex_normal_list' not in context.active_object:
            context.active_object['vertex_normal_list'] = []
            
        if 'vertex_normal_list' in context.active_object:
            for i in range(vert_index):
               
                # update vertex normal list
                if len(context.object.vertex_normal_list) <= i:
                    item = context.object.vertex_normal_list.add()
                    item.normal = obj.data.vertices[i].normal
                # add items to list if too short
                else:
                    context.object.vertex_normal_list[i]['normal'] = obj.data.vertices[i].normal
            return {'FINISHED'}

##########################################################
# create vertex normal list for saving them normals
class vertex_normal_list(bpy.types.PropertyGroup):
    normal = bpy.props.FloatVectorProperty(default=(0.0, 0.0, 0.0))

# update list
class update_normal_list(bpy.types.Operator):
    bl_idname = "object.update_normal_list" 
    bl_label = "Update Vertex Normals"
    bl_description = 'Update vertex normals after EDITMODE'
    
    def execute(self, context):
        vertices = context.active_object.data.vertices
        obj = context.active_object
       
        bpy.ops.object.mode_set(mode='OBJECT')
        
        for i in range(len(obj.vertex_normal_list)):
            vertices[i].normal = obj.vertex_normal_list[i]['normal']
        
        context.area.tag_redraw()
        
        return{'FINISHED'}         

##########################################################
##########################################################
# draw Normals in OBJECTMODE
def draw_line(self, context, vertexloc, vertexnorm, colour, thick):
    obj = context.active_object
    
    #get obj rotation
    rot = obj.rotation_euler.to_matrix().inverted()
    scale = obj.scale
    vertex = vertexloc * rot
    normal = vertexnorm * rot

    x1 = vertex[0] * scale[0] + obj.location[0]
    y1 = vertex[1] * scale[1] + obj.location[1]
    z1 = vertex[2] * scale[2] + obj.location[2]
    
    x2 = normal[0]*context.scene.tool_settings.normal_size* scale[0] + x1
    y2 = normal[1]*context.scene.tool_settings.normal_size* scale[1] + y1
    z2 = normal[2]*context.scene.tool_settings.normal_size* scale[2] + z1
    
    bgl.glEnable(bgl.GL_BLEND)
    bgl.glLineWidth(thick)
    # set color
    bgl.glColor4f(*colour)
    
    # draw line
    bgl.glBegin(bgl.GL_LINE_STRIP)
    bgl.glVertex3f(x1,y1,z1)
    bgl.glVertex3f(x2,y2,z2)
    bgl.glEnd()
    bgl.glDisable(bgl.GL_BLEND)
    
def InitGLOverlay(self, context):

    obj = context.active_object
    
    if context.active_object != None and obj.type == 'MESH':
        vertex = context.active_object.data.vertices
        vert_index = len(vertex)
        for i in range(vert_index):
            # selected verts will align on z-axis
            if vertex[i].select == True:
                #draw_line(self, context, vertex[i].co, vertex[i].normal, (0.5,1.0,1.0,0.1),3)
                draw_line(self, context, vertex[i].co, vertex[i].normal, (0.5,1.0,1.0,1.0),1)
            # unselected verts will align on 3d cursor
            elif vertex[i].select == False:
                #draw_line(self, context, vertex[i].co, vertex[i].normal, (0.0,0.0,0.0,0.6),3)
                draw_line(self, context, vertex[i].co, vertex[i].normal, (0.0,0.6,0.8,0.6),1)

# draw normals in object mode operator
class draw_normals(bpy.types.Operator):
    bl_idname = 'object.draw_normals'
    bl_label = 'draw_normals'
    bl_description = 'Draw normals in OBJECTMODE'
    _handle = None
    
    def modal(self, context, event):
        if not context.window_manager.drawnormal:
            context.area.tag_redraw()
            # deprecated since 2.66
            # context.region.callback_remove(self._handle)
            # use instead
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            
            return {'CANCELLED'}
        return {'PASS_THROUGH'}
    
    def cancel(self, context):
        if context.window_manager.drawnormal:
            # deprecated since 2.66
            # context.region.callback_remove(self._handle)
            # use instead
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            
            context.window_manager.drawnormal = False
        return {'CANCELLED'}
    
    def invoke(self, context, event):
        if context.area.type == 'VIEW_3D':
            if context.window_manager.drawnormal == False:
                context.window_manager.drawnormal = True
                context.window_manager.modal_handler_add(self)
                # deprecated since 2.66
                #self._handle = context.region.callback_add(InitGLOverlay, (self, context), 'POST_VIEW')
                # use instead
                self._handle = bpy.types.SpaceView3D.draw_handler_add(InitGLOverlay, (self, context),'WINDOW', 'POST_VIEW')
                context.area.tag_redraw()
                return {'RUNNING_MODAL'}
            else:
                context.window_manager.drawnormal = False
                return {'CANCELLED'}
        else:
            self.report({'WARNING'}, "View3D not found, can't run operator")
            return {'CANCELLED'}

##########################################################
# init properties
def init_properties():
    bpy.types.WindowManager.reloadchange = bpy.props.StringProperty(default='OBJECT')
    
    bpy.types.WindowManager.autoreload = bpy.props.BoolProperty(default=False)
    
    bpy.types.WindowManager.reload = bpy.props.BoolProperty(default=False, update=reload)
    
    bpy.types.WindowManager.savechange = bpy.props.StringProperty(default='EDIT')

    bpy.types.WindowManager.autosave = bpy.props.BoolProperty(default=False)
    
    bpy.types.WindowManager.save = bpy.props.BoolProperty(default=False, update=save)
    
    bpy.types.Object.vertex_normal_list = bpy.props.CollectionProperty(
        type=vertex_normal_list)
        
    bpy.types.Object.select_vertex = bpy.props.IntProperty(
        default=0)
    
    bpy.types.WindowManager.drawnormal = bpy.props.BoolProperty(
        default=False)
    
    bpy.types.WindowManager.copynormal = bpy.props.FloatVectorProperty(
        default=(0.0, 0.0, 0.0))
    
    bpy.types.WindowManager.customnormal1 = bpy.props.FloatVectorProperty(
        default=(0.0, 0.0, 1.0),
        subtype = 'DIRECTION',
        update=update_custom_normal1)

    bpy.types.WindowManager.customnormal2 = bpy.props.FloatVectorProperty(
        default=(0.0, 0.0, 1.0),
        subtype = 'TRANSLATION',
        update=update_custom_normal2)

# clear properties
def clear_properties():
    props = ['drawnormal', 'customnormal1', 'customnormal2', 'autosave', 'savechange', 'save', 'copynormal', 'autoreload', 'reloadchange', 'reload']
    for p in props:
        if bpy.context.window_manager.get(p) != None:
            del bpy.context.window_manager[p]
        try:
            x = getattr(bpy.types.WindowManager, p)
            del x
        except:
            pass
    