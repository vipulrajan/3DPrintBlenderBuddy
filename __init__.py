from pickle import TRUE
import bpy
import sys
import os

bl_info = {
    'name': 'My Example Addon',
    'blender': (2, 93, 0),
    'category': 'Object',
    'location': "View3D > Tools > MyPlugin",
    'version': (1, 0, 0),
    'author': 'Vipul Rajan',
    'description': 'An example addon',
}

modulesNames = [ 'Exceptions', 'BevelShapeCreator', 'GCodeReader']

modulesFullNames = {}
for currentModuleName in modulesNames:
    modulesFullNames[currentModuleName] = ('{}.{}'.format(__name__, currentModuleName))
 
for currentModuleFullName in modulesFullNames.values():
    import importlib
    if currentModuleFullName in sys.modules:
        importlib.reload(sys.modules[currentModuleFullName])
    else:
        globals()[currentModuleFullName] = importlib.import_module(currentModuleFullName)
        setattr(globals()[currentModuleFullName], 'modulesNames', modulesFullNames)


class GCodeLoaderOperator(bpy.types.Operator):
    
    bl_idname = 'opr.gcode_loader'
    bl_label = 'Load GCode'
    
    def execute(self, context):

        fileName = getattr(bpy.context.scene.Buddy_Props, 'FilePath')
        filters = {}

        for prop in propsFilter:
            filters[prop] = getattr(bpy.context.scene.Buddy_Props, prop)

        sys.modules[modulesFullNames['GCodeReader']].builder(fileName, params={'widthOffset':-0.06}, filters=filters)
        return {'FINISHED'}

class FilterUpdaterOperator(bpy.types.Operator):
    
    bl_idname = 'opr.filter_updater'
    bl_label = 'Update Filters'
    
    def execute(self, context):

        filters = {}
        for prop in propsFilter:
            filters[prop] = getattr(bpy.context.scene.Buddy_Props, prop)

        sys.modules[modulesFullNames['GCodeReader']].toggleVisibility(filters=filters)
        return {'FINISHED'}

class PanelParent(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "3D-Print Buddy"
    bl_options = {"DEFAULT_CLOSED"}

class Options(PanelParent ):
    bl_idname = 'VIEW3D_PT_panel_options'
    bl_label = 'Options'

    def draw(self, context):
        col = self.layout.column()
        for propName in propsMain:
            row = col.row()
            row.prop(context.scene.Buddy_Props, propName)

        row = col.row()
        col.operator('opr.gcode_loader', text='Load GCode')

class Filters(PanelParent):
    bl_parent_id = "VIEW3D_PT_panel_options"
    bl_idname = 'VIEW3D_PT_panel_fiters'
    bl_label = "Filters"

    def draw(self, context):
        col = self.layout.column()
        for propName in propsFilter:
            row = col.row()
            row.prop(context.scene.Buddy_Props, propName)
        
        row = col.row()
        col.operator('opr.filter_updater', text='Update Filters')
        
        

class Buddy_Props(bpy.types.PropertyGroup):
    ObjectName: bpy.props.StringProperty(name='Object Name', description='What to name the imported object collection', default='OBJECT')
    BevelName: bpy.props.StringProperty(name='Bevel Name', description='What to name the created bevel profiles', default='bevel')
    FilePath: bpy.props.StringProperty(name='File Path', description="Path of GCode file", subtype="FILE_PATH")
        
    Gap_fill: bpy.props.BoolProperty(name='Gap fill', default=True)
    External_perimeter: bpy.props.BoolProperty(name='External perimeter', default=True)
    Perimeter: bpy.props.BoolProperty(name='Perimeter', default=True)
    Top_solid_infill: bpy.props.BoolProperty(name='Top solid infill', default=True)
    Bridge_infill: bpy.props.BoolProperty(name='Bridge infill', default=True)
    Internal_infill: bpy.props.BoolProperty(name='Internal infill', default=True)
    Custom: bpy.props.BoolProperty(name='Custom', default=True)
    Solid_infill: bpy.props.BoolProperty(name='Solid infill', default=True)
    Skirt_Brim: bpy.props.BoolProperty(name='Skirt/Brim', default=True)
    

CLASSES = [
    Buddy_Props, Options, Filters, GCodeLoaderOperator, FilterUpdaterOperator
]

propsMain = [
    'ObjectName', 'BevelName', 'FilePath'
    ]

propsFilter = ['Gap_fill', 'External_perimeter', 'Perimeter', 'Top_solid_infill', 'Bridge_infill', 'Internal_infill', 'Custom', 'Solid_infill', 'Skirt_Brim']



def register():
    print('registered') # just for debug
    for klass in CLASSES:
        bpy.utils.register_class(klass)

    bpy.types.Scene.Buddy_Props = bpy.props.PointerProperty(type=Buddy_Props)

    

def unregister():
    print('unregistered') # just for debug
    for klass in CLASSES:
        bpy.utils.unregister_class(klass)


    del bpy.types.Scene.Buddy_Props

    

if __name__ == '__main__':
    register()