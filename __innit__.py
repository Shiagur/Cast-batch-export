bl_info = {
    "name" : "Simple Cast Batch Export Script",
    "author" : "Shiagur",
    "description" : "",
    "blender" : (4, 5, 4),
    "version" : (1, 0, 0),
    "location" : "View3d > Tools",
    "warning" : "",
    "category" : "Generic"
}   

print("\n\n\n -------------- NEW EXECUTION --------------")

import bpy # type: ignore
from bpy.props import (EnumProperty,PointerProperty,BoolProperty,FloatProperty,StringProperty) # type: ignore
from bpy_extras.io_utils import (ExportHelper) # type: ignore

class MY_PG_SceneProperties(bpy.types.PropertyGroup):
    export_selected: BoolProperty(name = "Export Selected", description="", default=True,)# type: ignore
    include_models: BoolProperty(name = "Include Models", description="", default=False,)# type: ignore
    include_animations: BoolProperty(name = "Include Animations", description="", default=True,)# type: ignore
    include_notetracks: BoolProperty(name = "Include Notetracks", description="", default=True,)# type: ignore
    looped: BoolProperty(name = "Looped", description="", default=False,)# type: ignore
    scale: FloatProperty(name = "Scale", default = 1.0)# type: ignore
    up_enum: EnumProperty(
        name="Up:",
        description="",
        items = (
            ("z", "Z Up", "Z Up"),
            ("y", "Y Up", "Y Up")
        )
    )# type: ignore

class ExportOp (bpy.types.Operator, ExportHelper):
    """Export"""
    bl_idname= "pose.castexportop"
    bl_label= "Export"
    # bl_options = {"REGISTER", "UNDO"}
    filename_ext = ""
    default = ""
    filter_glob: StringProperty(default="",options={'HIDDEN'},maxlen=512) # type: ignore
    
    def execute(self, context):
        pg=bpy.context.scene.shia_cast_properties
        exppath = self.filepath.removesuffix(bpy.path.basename(self.filepath))

        if not bpy.context.selected_objects: 
            self.report({'ERROR'}, 'No Object selected. Could not export animations.')
            return {'CANCELLED'}
        if not bpy.context.object.type == 'ARMATURE': 
            self.report({'ERROR'}, 'No Aramature selected. Could not export animations.')
            return {'CANCELLED'}        
        if len(bpy.data.actions) == 0:
            self.report({'ERROR'}, 'No Actions to export found.')
            return {'CANCELLED'}

        for exp_action in bpy.data.actions:

            bpy.context.object.animation_data.action = exp_action
            cast_export=bpy.ops.export_scene.cast(
                filepath=str(f"{exppath}{exp_action.name}.cast"), 
                check_existing=False, 
                export_selected=pg.export_selected, 
                incl_model=pg.include_models, 
                incl_animation=pg.include_animations, 
                incl_notetracks=pg.include_notetracks, 
                is_looped=pg.looped, 
                scale=pg.scale, 
                up_axis=pg.up_enum
            )
            print(f"Finished {exp_action.name}: {cast_export}")


        # bpy.ops.ed.undo_push(message="TTTEEEEESSSSTTTT")
        # print(self.test_prop)

        return {"FINISHED"}

class CAST_PT_MainPanel(bpy.types.Panel):
    bl_label = "Cast Batch Export"
    bl_idname = "CAST_PT_MainPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Cast'
    
    def draw(self, context):
        pg=bpy.context.scene.shia_cast_properties
        layout = self.layout
        col = layout.column()
        col.label(text = f"Export settings:")
        col.prop(pg, "export_selected")
        col.prop(pg, "include_models")
        col.prop(pg, "include_animations")
        col.prop(pg, "include_notetracks")
        col.prop(pg, "looped")
        col.prop(pg, "scale")
        col.prop(pg, "up_enum")
        button = col.operator("pose.castexportop", icon= "EXPORT") 


myClasses = [MY_PG_SceneProperties,CAST_PT_MainPanel,ExportOp]
def register():
    for cls in myClasses:
        bpy.utils.register_class(cls)
    bpy.types.Scene.shia_cast_properties = PointerProperty(type=MY_PG_SceneProperties)

def unregister():
    del bpy.types.Scene.my_properties
    for cls in myClasses:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    
    register()



    # if bpy.app.version >= (4,4,0):
