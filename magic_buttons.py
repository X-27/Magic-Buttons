bl_info = {
	"name": "Magic Buttons",
	"description": "A few useful tools for the level 1 noob, and the legendary magic render button that will make all renders perferct.",
	"author": "X-27, David Bates",
	"version": (99999,99),
	"blender": (2, 3, 7),
	"location": "Properties  > Scene",
	"category": "Render",
}

import bpy

#
# --- operator for the "magic button" ---
#
class RLoverride(bpy.types.Operator):
	'''Set render layer material override'''
	bl_idname = "magic.render_button"
	bl_label = "Magic Material"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		create_material()
		bpy.context.scene.render.layers["RenderLayer"].material_override = bpy.data.materials["magic"]
		bpy.ops.render.view_show('INVOKE_SCREEN')
		bpy.ops.render.render()
		return {'FINISHED'}


#
# --- new material, BI or cycles ---
#
def create_material():
	scn = bpy.context.scene
	mat = bpy.data.materials.new('magic')
	
	# cycles material
	if scn.render.engine == 'CYCLES':
		# - nodes -
		mat.use_nodes = True
		nodes = mat.node_tree.nodes
		
		#diffuse
		nodes.remove(nodes['Diffuse BSDF'])
		
		#emission
		emission = nodes.new('ShaderNodeEmission')
		#emission.name = 'Emission'
		
		#Mix node
		colorMix = nodes.new('ShaderNodeMixRGB')
		colorMix.blend_type = 'MULTIPLY'
		colorMix.inputs[0].default_value = 1
		colorMix.inputs[2].default_value = (0.0175381, 0.148583, 0.636863, 1)
		
		#magic texture
		magicTex = nodes.new('ShaderNodeTexMagic')
		magicTex.turbulence_depth = 0
		
		#math
		multiply = nodes.new('ShaderNodeMath')
		multiply.operation = 'MULTIPLY'
		multiply.inputs[1].default_value = 5
		multiply.name = 'Multiply'
		
		#math
		max = nodes.new('ShaderNodeMath')
		max.operation = 'MAXIMUM'
		max.inputs[0].default_value = 0.1
		max.name = 'Maximum'
		
		# Object Info
		objInfo = nodes.new('ShaderNodeObjectInfo')
		
	# - node links -
		
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
		
	# BI material
	if scn.render.engine == 'BLENDER_RENDER':
		# material settings
		mat.diffuse_color = (0.0175381, 0.148583, 0.636863)
		mat.emit = 1
		
		# Create procedural texture 
		magTex = bpy.data.textures.new('Magic', type = 'MAGIC')
		magTex.noise_depth = 0  
		magTex.turbulence = 5
		
		# Add texture slot to material
		mts = mat.texture_slots.add()
		mts.texture = magTex
		# texture settings
		mts.texture_coords = 'GLOBAL'
		mts.scale[0] = 5
		mts.scale[1] = 5
		mts.scale[2] = 5
		mts.use_map_color_diffuse = True
		mts.use_map_emit = True
		#mts.emit_factor = 0.75
		mts.blend_type = 'MULTIPLY'

#
# --- Draw UI in properties window ---
#
class MagicPanel(bpy.types.Panel):
	'''Creates a Panel in the Render properties window'''
	bl_label = 'Magic Buttons'
	bl_idname = 'Magic Render'
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = 'render'

	def draw(self, context):
		layout = self.layout

		# Totally awesome magic render button
		r0 = layout.row()
		r0.label(text="Invoke the power of the Magic Render Button")

		r1 = layout.row()
		r1.operator("magic.render_button", text="Magic Render", icon='OUTLINER_OB_CAMERA')

		# buttons for noob   - Whoops and nevermind
		r2 = layout.row()
		r2.label(text="Other helpfull Noob tools")

		r3 = layout.row()
		r3.operator("ed.undo", text="Whoops!", icon='LOOP_BACK')
		r3.operator("ed.redo", text="Nevermind", icon='LOOP_FORWARDS')

		# Bring forth the smooth monkey
		r4 = layout.row()
		r4.label(text="Basic Noob Tools")

		r5 = layout.row()
		r5.operator("mesh.primitive_monkey_add", text="bring forth a monkey", icon='MONKEY')
		r5.operator("object.shade_smooth", text="Make Smooth", icon='OUTLINER_OB_SURFACE')
		
		r6 = layout.row()
		r6.operator("object.subdivision_set", text="Invoke the Magic of sub-serf", icon='MOD_SUBSURF')

		# Randomly delete stuff
		r7 = layout.row()
		r7.label(text="If you only have a few mistakes")

		r8 = layout.row()
		r8.operator("object.select_random", text="random selection", icon='QUESTION')
		r8.operator("object.delete", text="remove selected", icon='MOD_EXPLODE')

		# Nuke the Blend!!!
		r9 = layout.row()
		r9.label(text="If you really messed up something")

		r10 = layout.row()
		r10.operator("wm.read_homefile", text="Permanently Annihilate my Disaster", icon='RADIO')
# end MagicPanel



#
# --- reg and unreg it all ---
#
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
