# to enable console run blender.exe from cmd cd "C:\Program Files\Blender Foundation\Blender 2.81"
import bpy
import os
from random import randint


DEBUG_MODE = False # to use outside blender
if DEBUG_MODE:
    from skimage import io
    import numpy as np

if not DEBUG_MODE:
    # Mark all scene devices as GPU for cycles
    bpy.context.scene.cycles.device = 'GPU'
    
    # Enable CUDA GPU
    bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'
    
    # Disable CPU
    for devices in bpy.context.preferences.addons['cycles'].preferences.get_devices():
        for d in devices:
            d.use = True
            if d.type == 'CPU':
                d.use = False
            print("Device '{}' type {} : {}" . format(d.name, d.type, d.use))
            


def create_rgba_color(r,g,b,alpha=0.0):
    if r>1 or g>1 or b>1:
        r = color_limiter_float64(r/255)
        g = color_limiter_float64(g/255)
        b = color_limiter_float64(b/255)
        alpha = max(min(1.0, alpha),0.0)
    return [float(r),float(g),float(b),float(alpha)]

def create_gaussian(mu=30,sigma=15):
    return [mu,sigma]

def color_limiter_uint8(color_value):
    color_value = max(min(color_value,255),0)
    return int(color_value)

def color_limiter_float64(color_value):
    color_value = max(min(color_value,1.0),0.0)
    return float(color_value)

def do_render(output_path):
    if DEBUG_MODE:
        print('rendering to {}'.format(output_path))
    else:
        bpy.context.scene.render.filepath = render_output_path
        bpy.ops.render.render(write_still=True)
        
def load_image(image_path):
    if DEBUG_MODE:
        print("bpy.data.images.load(image_path)")
    else:
        bpy.data.images.load(image_path)
    
class WorkerChalecos():
    def __init__(self, script_path):
        
        # add all the images of the folder to blender
        textures_folder = os.path.join(script_path,'textures','chalecos')
        textures_filenames = os.listdir(textures_folder)
        self.image_names = textures_filenames
        for texture_filename in textures_filenames:
            image_path = os.path.join(textures_folder,texture_filename)
            load_image(image_path)

    def set_texture(self, image_name):
        if DEBUG_MODE:
            print('setting texture image: {}'.format(image_name))
        else:
            bpy.data.materials['Jacket'].node_tree.nodes['Image Texture'].image = bpy.data.images[image_name]
            
    def set_random_texture(self):
        i = randint(0,len(self.image_names)-1)
        self.set_texture(self.image_names[i])

class WorkerCascos():
    def __init__(self):
        # RGBa format
        diffuse_colors = {}
        diffuse_colors["amarillo"] = create_rgba_color(240, 250, 0)
        diffuse_colors["azul"] = create_rgba_color(0,0,1)
        diffuse_colors["blanco"] = create_rgba_color(1,1,1)
        diffuse_colors["naranjo"] = create_rgba_color(255,127,39)
        diffuse_colors["otro"] = create_rgba_color(90,70,90) #gris
        diffuse_colors["rojo"] = create_rgba_color(240,0,0)
        diffuse_colors["sin_casco"] = create_rgba_color(1,1,1,alpha=1)
        diffuse_colors["verde"] = create_rgba_color(0,210,0)
        
        diffuse_noise = {}
        diffuse_noise["amarillo"] = create_gaussian(20,20)
        diffuse_noise["azul"] = create_gaussian(0,40)
        diffuse_noise["blanco"] = create_gaussian(10,15)
        diffuse_noise["naranjo"] = create_gaussian(5,5)
        diffuse_noise["otro"] = create_gaussian()
        diffuse_noise["rojo"] = create_gaussian(0,40)
        diffuse_noise["sin_casco"] = diffuse_noise["blanco"]
        diffuse_noise["verde"] = create_gaussian(0,40)
        
        self.diffuse_colors = diffuse_colors
        self.diffuse_noise = diffuse_noise
        
    def get_opacity_casco(self, color_casco):
        if color_casco == "sin_casco": 
            return 0.0 # hacemos el casco invisible
        return 1.0
    
    def get_diffuse_casco(self, color_casco):
        return self.diffuse_colors[color_casco]

    
    def get_diffuse_noisy(self, color_casco):
        r,g,b,alpha = self.get_diffuse_casco(color_casco)
        mu,sigma = self.diffuse_noise[color_casco]
        r = int(r*255-mu)
        g = int(g*255-mu)
        b = int(b*255-mu)
        r = color_limiter_uint8(randint(r-sigma, r+sigma))/255
        g = color_limiter_uint8(randint(g-sigma, g+sigma))/255
        b = color_limiter_uint8(randint(b-sigma, b+sigma))/255
        new_color = [r,g,b,alpha]
        
        return new_color
        
    def set_diffuse_color(self, color_casco):
        diffuse_color_rgba = self.get_diffuse_noisy(color_casco)
        if DEBUG_MODE:
            print('setting diffuse_color: {}'.format(color_casco))
        else:
            bpy.data.materials["Casco"].node_tree.nodes["Diffuse BSDF"].inputs[0].default_value = diffuse_color_rgba


script_path = 'C:\\Users\\Mico\\Desktop\\blender-python\\scripting\\workers\\poc'
output_folder = os.path.join(script_path,'renders')

# colores de casco disponibles
colores = [    "amarillo",
                "azul",
                "blanco",
                "naranjo",
                "otro",
                "rojo",
                "sin_casco",
                "verde"]

worker_cascos = WorkerCascos()
worker_chalecos = WorkerChalecos(script_path)
n_samples = 5
for color_casco in colores:
    if DEBUG_MODE:
        color_samples = np.ones((n_samples,n_samples*10,3),dtype=np.float64)
    for i in range(0,n_samples):
        worker_chalecos.set_random_texture() # cambiar el color del chaleco
        worker_cascos.set_diffuse_color(color_casco) # cambiar el color del casco
        render_filename = 'worker_{}_sample_{}.png'.format(color_casco,i)
        render_output_path = os.path.join(output_folder,render_filename)
        
        do_render(render_output_path)

        if DEBUG_MODE:     
            color_sample = worker_cascos.get_diffuse_noisy(color_casco)
            color_samples[:,i*10:(i+1)*10,:] = color_samples[:,i*10:(i+1)*10,:]*color_sample[0:3]
            
    if DEBUG_MODE:  
        print(color_sample)
        print(color_samples.min())
        print(color_samples.max())
        io.imshow(color_samples)
        io.show()


        
