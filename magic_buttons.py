bl_info = {
    "name": "Magic Buttons",
    "description": "A few usefull tools for the level 1 noob, and the legendary magic render button that will make all renders perferct.",
    "author": "X-27",
    "blender": (2, 7, 3),
    "location": "Properties  > Scene",
    "category": "Render",
}

import bpy


class RLoverride(bpy.types.Operator):
    """Set render layer material override"""
    bl_idname = "magic.render_button"
    bl_label = "Magic Material"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        create_material(None)
        bpy.context.scene.render.layers["RenderLayer"].material_override = bpy.data.materials["magic"]
        bpy.ops.render.view_show('INVOKE_SCREEN')
        bpy.ops.render.render()
        return {'FINISHED'}


#      O====||========================>

def create_material(settings):
    scn = bpy.context.scene
    mat = bpy.data.materials.new('magic')
    if scn.render.engine == 'CYCLES':
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        
        nodes.remove(nodes['Diffuse BSDF'])
        
        emission = nodes.new('ShaderNodeEmission')
        #emission.name = 'Emission'
        
        colorMix = nodes.new('ShaderNodeMixRGB')
        colorMix.blend_type = 'MULTIPLY'
        colorMix.inputs[0].default_value = 1
        colorMix.inputs[2].default_value = (0.0175381, 0.148583, 0.636863, 1)
        
        magicTex = nodes.new('ShaderNodeTexMagic')
        magicTex.turbulence_depth = 0
        #magicTex.name = 'Magic Texture'
        
        multiply = nodes.new('ShaderNodeMath')
        multiply.operation = 'MULTIPLY'
        multiply.inputs[1].default_value = 5
        multiply.name = 'Multiply'
        
        
        max = nodes.new('ShaderNodeMath')
        max.operation = 'MAXIMUM'
        max.inputs[0].default_value = 0.1
        max.name = 'Maximum'
        
        objInfo = nodes.new('ShaderNodeObjectInfo')
        #objInfo.name = 'Object Info'
        
        
        
        # node links
        
        # Object Info > Maximum
        mat.node_tree.links.new(objInfo.outputs['Random'], max.inputs[1])
        
        # Maximum > Multiply
        mat.node_tree.links.new(max.outputs['Value'], multiply.inputs[0])
        
        # Multiply > Magic Texture
        mat.node_tree.links.new(multiply.outputs['Value'], magicTex.inputs['Scale'])
         
        # Magic Texture > Mix
        mat.node_tree.links.new(magicTex.outputs['Color'], colorMix.inputs[1])
        
        # Mix > Emission
        mat.node_tree.links.new(colorMix.outputs['Color'], emission.inputs['Color'])
        
        # Emission > Material Output
        mat.node_tree.links.new(emission.outputs['Emission'], nodes['Material Output'].inputs['Surface'])
        pass








class MagicPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Magic Buttons"
    bl_idname = "Magic Render"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    def draw(self, context):
        layout = self.layout

# Trash - ignore if it doesn't work

# Totally awesome magic render button
        row = layout.row()
        row.label(text="Invoke the power of the Magic Render Button")

        row = layout.row()
        
        row.operator("magic.render_button", text="Magic Render", icon='OUTLINER_OB_CAMERA')
 

# buttons for noob   - WHoops and nevermind
        row = layout.row()
        row.label(text="Other helpfull Noob tools")

        row = layout.row()
        row.operator("ed.undo", text="Whoops!", icon='LOOP_BACK')

        row.operator("ed.redo", text="Nevermind", icon='LOOP_FORWARDS')

# Bring forth the smooth monkey
        row = layout.row()
        row.label(text="Basic Noob Tools")

        row = layout.row()
        
        row.operator("mesh.primitive_monkey_add", text="bring forth a monkey", icon='MONKEY')
        row.operator("object.shade_smooth", text="Make Smooth", icon='OUTLINER_OB_SURFACE')
        row = layout.row()
        
        row.operator("object.subdivision_set", text="Invoke the Magic of sub-serf", icon='MOD_SUBSURF')

# Randomly delete stuff
        row = layout.row()
        row.label(text="If you only have a few mistakes")

        row = layout.row()
        
        row.operator("object.select_random", text="random selection", icon='QUESTION')

        row.operator("object.delete", text="remove selected", icon='MOD_EXPLODE')



# Nuke the Blend!!!
        row = layout.row()
        row.label(text="If you really messed up something")

        row = layout.row()
        
        row.operator("wm.read_homefile", text="Permanently Annihilate my Disaster", icon='RADIO')







def register():
    bpy.utils.register_class(MagicPanel)
    bpy.utils.register_class(RLoverride)


def unregister():
    bpy.utils.unregister_class(MagicPanel)
    bpy.utils.unregister_class(RLoverride)


if __name__ == "__main__":
    register()


#    awesome picture ↓↓↓↓↓↓↓↓


#               ___________
#              /           \_________
#              |___________|=========  ~   ~   ~   ~   ~   ~ 
#         ______/         \_______
#        /____ ________________ __\
#       |  o \  O   O   O   O/ o  |
#        \___/_O__O___O___O__\____/
# """""""""""""""""""""""""""""""""""""""""""""""
