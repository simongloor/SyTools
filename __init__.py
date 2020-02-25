bl_info = {
        "name": "SyTools",
        "category": "3D View",
        "author": "Pillars of SY | Simon Gloor",
        "version": (1, 1, 0),
        "blender": (2, 80, 0),
        "description": "Tools to improve the Workflow for creating Game Assets",
        "category": "Pillars of SY"
        }

if "bpy" in locals():
    import imp
    imp.reload(SyMenu)
    imp.reload(SyPanel)
    imp.reload(SyCommands)
    # imp.reload(SyNormals)
    print("Reloaded SyTools")
else:
    from . import (SyMenu,
    SyPanel,
    SyCommands)
    # , SyNormals
    print("Imported Sytools")


import bpy
from bpy.props import *

#************************************************************************************
# Register

classes = (
    SyCommands.SY_OT_SySetCursorPivot,
    SyCommands.SY_OT_SyUpdateLinks,
    SyCommands.SY_OT_SyCreateCamEqui,
    SyCommands.SY_OT_SyCutHole,
    SyCommands.SY_OT_SyCreateCam,
    SyCommands.SY_OT_SyOriginToSelection,
    SyCommands.SY_OT_SyCreateSkyboxCam,
    SyCommands.SY_OT_SyExtractMasked,
    SyCommands.SY_OT_SyTurnSubedge,
    SyCommands.SY_OT_SyCreateCube,
    SyCommands.SY_OT_SyMoveSelectionToZero,
    SyCommands.SY_OT_SyFixRotation,
    SyCommands.SY_OT_SyDissolveEdge,
    SyCommands.SY_OT_SyEdgeIntersection,
    SyCommands.SY_OT_Weight2VertexCol,
    SyCommands.SY_OT_SySeamBorder,
    SyMenu.SY_MT_SyMenu,
    # SyNormals.SY_PT_vertex_normals_ui,
    # SyNormals.SY_OT_tree_vertex_normals,
    # SyNormals.SY_OT_foliage_vertex_normals,
    # SyNormals.SY_OT_select_vertex,
    # SyNormals.SY_OT_invert_selection,
    # SyNormals.SY_OT_copy_normal,
    # SyNormals.SY_OT_paste_normal,
    # SyNormals.SY_OT_clear_normal,
    # SyNormals.SY_OT_invert_normal,
    # SyNormals.SY_OT_transfer_normal,
    # SyNormals.SY_OT_save_normals,
    # # SyNormals.vertex_normal_list,
    # SyNormals.SY_OT_update_normal_list,
    # SyNormals.SY_OT_draw_normals,
    SyPanel.SY_PT_sy_panel_ui,
    )

register, unregister = bpy.utils.register_classes_factory(classes)

# def register():
    # bpy.utils import register_class
    # for cls in classes:
    #     register_class(cls)
    # SyNormals.init_properties()

# def unregister():
    # bpy.utils import unregister_class
    # for cls in classes:
    #     unregister_class(cls)
    # SyNormals.clear_properties()

def draw_item(self, context):
    layout = self.layout
    #layout.menu(SyPanel.bl_idname)
    #layout.menu(SyNormals.bl_idname)

# if __name__ == "__main__":
#     register()
