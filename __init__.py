bl_info = {
        "name": "SyTools",
        "category": "3D View",
        "author": "Pillars of SY | Simon Gloor",
        "description": "Tools to improve the Workflow for creating Game Assets",
        "category": "Sy"
        }

if "bpy" in locals():
    import imp
    imp.reload(SyMenu)
    imp.reload(SyPanel)
    imp.reload(SyCommands)
    imp.reload(SyNormals)
    print("Reloaded SyTools")
else:
    from . import SyMenu, SyPanel, SyCommands, SyNormals
    print("Imported Sytools")


import bpy
from bpy.props import *

#************************************************************************************
# Register

def register():
    bpy.utils.register_module(__name__)
    SyNormals.init_properties()
    
def unregister():
    bpy.utils.unregister_module(__name__)
    SyNormals.clear_properties()

def draw_item(self, context):
    layout = self.layout
    #layout.menu(SyPanel.bl_idname)
    #layout.menu(SyNormals.bl_idname)
                
if __name__ == "__main__":
    register()

