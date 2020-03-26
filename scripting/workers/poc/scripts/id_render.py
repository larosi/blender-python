import bpy
import os

# user parameteres
interest_objects = {}
interest_objects['names'] = ['Hats','Body','Bottoms','Shoes','Tops','Eyelashes']
interest_objects['pass_index'] = 1

script_path = 'C:\\Users\\Mico\\Desktop\\blender-python\\scripting\\workers\\poc'
output_folder = os.path.join(script_path,'renders')

bpy.context.scene.view_layers["View Layer"].use_pass_object_index = True

bpy.data.scenes['Scene'].use_nodes = True
tree = bpy.data.scenes['Scene'].node_tree
nodes = tree.nodes
links = tree.links
indexOBOutput = tree.get('IndexOB Output')

fileOutput = nodes.new(type="CompositorNodeOutputFile")
fileOutput.base_path = output_folder
fileOutput.file_slots.remove(fileOutput.inputs[0])

for obj in bpy.data.objects:
	if obj.name in interest_objects['names']:
		obj.pass_index = interest_objects['pass_index']
	print('{}:{}'.format(obj.name,obj.pass_index))

idNode = nodes.new(type='CompositorNodeIDMask')
indexPass = interest_objects['pass_index']
idNode.index = indexPass

links.new(nodes.get('Render Layers').outputs.get('IndexOB'), idNode.inputs[0])
fileOutput.file_slots.new('Object_{}'.format(indexPass))

links.new(idNode.outputs[0], fileOutput.inputs[indexPass - 1])

bpy.ops.render.render(use_viewport=False)