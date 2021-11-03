from mathutils import Matrix
import bpy
from bpy.types import (Panel,
                       Operator,
                       AddonPreferences,
                       PropertyGroup,
                       )
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )

from batoms.butils import get_selected_batoms
from batoms import Batoms

class Cell_PT_prepare(Panel):
    bl_label       = "Cell"
    bl_space_type  = "VIEW_3D"
    bl_region_type = "UI"
    # bl_options     = {'DEFAULT_CLOSED'}
    bl_category = "Cell"
    bl_idname = "BATOMS_PT_Cell"

  
    def draw(self, context):
        layout = self.layout
        clpanel = context.scene.clpanel

        box = layout.box()
        row = box.row()
        row.prop(clpanel, "pbc")

        box = layout.box()
        col = box.column(align=True)
        col = box.column()
        col.prop(clpanel, "cell")

        box = layout.box()
        col = box.column(align=True)
        col = box.column()
        col.prop(clpanel, "transform", index = 0)
        #
        box = layout.box()
        col = box.column()
        col.prop(clpanel, "boundary")



class CellProperties(bpy.types.PropertyGroup):
    @property
    def selected_batoms(self):
        return get_selected_batoms()
    def Callback_modify_transform(self, context):
        clpanel = bpy.context.scene.clpanel
        transform = clpanel.transform
        modify_transform(self.selected_batoms, transform)
    def Callback_modify_cell(self, context):
        clpanel = bpy.context.scene.clpanel
        cell = [clpanel.cell_a, clpanel.cell_b, clpanel.cell_c]
        modify_batoms_attr(self.selected_batoms, 'cell', cell)
    def Callback_modify_pbc(self, context):
        clpanel = bpy.context.scene.clpanel
        pbc = clpanel.pbc
        modify_batoms_attr(self.selected_batoms, 'pbc', pbc)
    def Callback_modify_boundary(self, context):
        clpanel = bpy.context.scene.clpanel
        modify_batoms_attr(self.selected_batoms, 'boundary', clpanel.boundary)

    pbc: BoolProperty(
        name = "pbc", default=True,
        description = "pbc", update = Callback_modify_pbc)
    cell: FloatVectorProperty(
        name="Cell", default=(1, 1, 1),
        subtype = "XYZ",
        description = "Cell in a, b, c axis", update = Callback_modify_cell)
    
    transform: FloatVectorProperty(
        name="Transform",
        size=9,
        subtype = "MATRIX",
        # default=[b for a in Matrix.Identity(3) for b in a],
        description = "Transform matrix", update = Callback_modify_transform)
    boundary: FloatVectorProperty(
        name="boundary", default=(0.00, 0.0, 0.0),
        subtype = "XYZ",
        description = "boundary  in a, b, c axis", update = Callback_modify_boundary)
    
def modify_batoms_attr(batoms_name_list, key, value):
    batoms_list = []
    for name in batoms_name_list:
        batoms = Batoms(label = name)
        setattr(batoms, key, value)
        batoms_list.append(batoms)
    for batoms in batoms_list:
        batoms.select = True
        
def modify_transform(batoms_name_list, transform):
    for name in batoms_name_list:
        batoms = Batoms(label = name)
        batoms.repeat(transform)