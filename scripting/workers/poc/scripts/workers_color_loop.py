# to enable console run blender.exe from cmd cd "C:\Program Files\Blender Foundation\Blender 2.81"
import bpy
import os
from random import randint
import numpy as np
from math import pi

DEBUG_MODE = False # to use outside blender
if DEBUG_MODE:
    from skimage import io
    

""" General render parameters """
render_engines = ['CYCLES','BLENDER_EEVEE','BLENDER_WORKBENCH']
RENDER_ENGINE = render_engines[1] # choose the render engine
# Cycles: Raytracing render - 10 seg per image
# Eevee: Realtime videogame-like render - 1 seg per image aprox
# Workbench: Same render that blender use on the viewport

if not DEBUG_MODE:
    bpy.context.scene.render.engine = RENDER_ENGINE # set the selected render engine
    if RENDER_ENGINE == 'CYCLES':
        # Choose the number of samples
        bpy.context.scene.cycles.samples = 32 #128 64 32
        
        # Title size
        bpy.context.scene.render.tile_x = 256 #256 128 64 32
        bpy.context.scene.render.tile_y = 256 #256 128 64 32
        
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
    elif RENDER_ENGINE == 'BLENDER_EEVEE':
        # Title size
        bpy.context.scene.render.tile_x = 256 #256 128 64 32
        bpy.context.scene.render.tile_y = 256 #256 128 64 32  
        
    elif RENDER_ENGINE == 'BLENDER_WORKBENCH':   
        # Title size
        bpy.context.scene.render.tile_x = 256 #256 128 64 32
        bpy.context.scene.render.tile_y = 256 #256 128 64 32   

def rgb2hsv(rgba):
    r,g,b=rgba[0],rgba[1],rgba[2]
    if len(rgba)==4:
        r,g,b,_ = rgba
    else:
        r,g,b = rgba

    maxc=max(r,g,b)
    minc=min(r,g,b)
    diff=maxc-minc
    
    #Saturation
    if maxc==0:
        s=0
    else:
        s=diff/maxc
        
    #Value
    v = maxc
    
    #hue
    h=0
    if diff == 0:
        return [h,s,v,0]
    
    if maxc == r:
        if g>b:
            h=60*(g-b)/diff
        else:
            h=60*(g-b)/diff+360
    if maxc == g:
        h=60*(b-r)/diff+120
    if maxc == b:
        h=60*(r-g)/diff+240
    
    return [h,s,v,0]



def hsv2rgb(hsv):
    
    h,s,v=hsv[0],hsv[1],hsv[2]
    while h>360:
        h=h-360
    while h<0:
        h=360+h
    s = color_limiter_float64(s)
    v = color_limiter_float64(v)
    
    c=v*s
    m=v-c
    x=c*(1-abs((h/60)%2-1))
    
    r,g,b=c,0,x
    
    if h<300:
        r,g,b=x,0,c
    if h<240:
        r,g,b=0,x,c
    if h<180:
        r,g,b=0,c,x
    if h<120:
        r,g,b=x,c,0
    if h<60:
        r,g,b=c,x,0
    
    r,g,b=r+m,g+m,b+m
    
    return [r,g,b,0]

def create_rgba_color(r,g,b,alpha=0.0):
    if r>1 or g>1 or b>1:
        r = color_limiter_float64(r/255)
        g = color_limiter_float64(g/255)
        b = color_limiter_float64(b/255)
        alpha = max(min(1.0, alpha),0.0)
    return [float(r),float(g),float(b),float(alpha)]

def create_hsv_noise(delta_h=(-60,60),delta_s=(-10,15), delta_v=(-10,-5)):
    #h+randint(-10,10),s+randint(-1,1)/10,v+randint(-10,-5)/20,0]
    return [delta_h,delta_s,delta_v]

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
        
def next_frame(t):
    if DEBUG_MODE:
        print('animation frame {}'.format(t))
    else:
        bpy.context.scene.frame_set(t)
        
def load_image(image_path):
    if DEBUG_MODE:
        print("bpy.data.images.load(image_path)")
    else:
        bpy.data.images.load(image_path)

class OrbitCamera():
    def __init__(self,target_name, n_points=40, radius = 15, cam_name = 'Camera' ):
        
        self.cam_name = cam_name
        self.target_name = target_name
        self.n_points = n_points
        # define N*N points over a sub-sphere
        theta = np.linspace(0, 2 * np.pi, n_points) #horizontal plane rotation
        phi   = np.linspace(0.25*np.pi, 0.5*np.pi, self.n_points) #vertical plane rotation
        THETA, PHI = np.meshgrid(theta, phi) 
        
        # using spherical coords
        R = radius
        X = R * np.sin(PHI) * np.cos(THETA)
        Y = R * np.sin(PHI) * np.sin(THETA)
        Z = R * np.cos(PHI)
        
        self.PHI = THETA
        self.THETA = PHI
        self.X = X
        self.Y = Y
        self.Z = Z

    def update_position(self):
        # select a random point over the sphere
        i = randint(0,self.n_points-1)
        j = randint(0,self.n_points-1)
        
        # select camera and target objects
        cam = bpy.data.objects[self.cam_name]
        target = bpy.data.objects[self.target_name]
        
        # update camera location as:
        # sphere_point + target_position
        cam.location =  (self.X[i][j] + target.x,
                         self.Y[i][j] + target.y,
                         self.Z[i][j] + target.z)
        
        # update camera rotation as:
        # sphere_radius_dir_angle + [0, 0, pi/2]

        cam.rotation_euler = (self.PHI[i,j], #x
                              0, #y
                              pi/2+self.THETA[i,j]) #z
            
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
        image_name = self.image_names[i]
        self.set_texture(image_name)
        
        return image_name
    
class WorkerCascos():
    def __init__(self):
        # RGBa format
        diffuse_colors = {}
        diffuse_colors["amarillo"] = create_rgba_color(240, 250, 0)
        diffuse_colors["azul"] = create_rgba_color(0,1,255)
        diffuse_colors["blanco"] = create_rgba_color(1,1,1)
        diffuse_colors["naranjo"] = create_rgba_color(1,0.068,0)
        diffuse_colors["otro"] = create_rgba_color(90,70,90) #gris
        diffuse_colors["rojo"] = create_rgba_color(1,0,0)
        diffuse_colors["sin_casco"] = create_rgba_color(0,0,0,alpha=1)
        diffuse_colors["verde"] = create_rgba_color(0,0.7,0)

        diffuse_noise = {}
        diffuse_noise["amarillo"] = create_hsv_noise(delta_h=(-1,1),delta_s=(-2,2), delta_v=(-5,5))
        diffuse_noise["azul"] = create_hsv_noise(delta_h=(-3,3),delta_s=(5,15), delta_v=(-12,-5))
        diffuse_noise["blanco"] = create_hsv_noise(delta_h=(-1,1),delta_s=(-2,2), delta_v=(-10,5))
        diffuse_noise["naranjo"] = create_hsv_noise(delta_h=(-2,2),delta_s=(-1,1), delta_v=(-2,2))
        diffuse_noise["otro"] = create_hsv_noise()
        diffuse_noise["rojo"] = create_hsv_noise(delta_h=(-2,2),delta_s=(-1,1), delta_v=(-12,0))
        diffuse_noise["sin_casco"] = create_hsv_noise()
        diffuse_noise["verde"] = create_hsv_noise(delta_h=(-5,5),delta_s=(-5,10), delta_v=(-10,-8))
        
        self.diffuse_colors = diffuse_colors
        self.diffuse_noise = diffuse_noise
        self.object_name = 'Hats'
        self.material_name = 'Casco'
        
    def get_opacity_casco(self, color_casco):
        if color_casco == "sin_casco": 
            return 0.0 # hacemos el casco invisible
        return 1.0
    
    def get_diffuse_casco(self, color_casco):
        return self.diffuse_colors[color_casco]

    def randomize_color(self, rgba, hsv_noise):
        print('random_color')
        print(rgba)
        h,s,v,_=rgb2hsv(rgba)
        #hsv = [h,s,v,1]
        #rgb = hsv2rgb(hsv)
        #print(rgb)
        #print(hsv)
        #print('')        
        #return rgb
    
        (hmin, hmax), (smin,smax), (vmin,vmax) = hsv_noise
        hsv = [h+randint(hmin,hmax),
               s+randint(smin,smax)/20,
               v+randint(vmin,vmax)/20,
               1]
        hsv_glossy = [h,randint(5,15)/20,randint(5,15)/20,1]
        rgb_glossy = hsv2rgb(hsv_glossy)
        rgb=hsv2rgb(hsv)
        print(rgb)
        print(hsv)
        return rgb ,rgb_glossy

    def get_diffuse_noisy(self, color_casco):
        rgba = self.get_diffuse_casco(color_casco)
        hsv_noise = self.diffuse_noise[color_casco]
        rgba_new, rgb_glossy = self.randomize_color(rgba,hsv_noise)
        
        return rgba_new, rgb_glossy
    """
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
    """    
    def set_diffuse_color(self, color_casco):
        diffuse_color_rgba, glossy_color_rgba = self.get_diffuse_noisy(color_casco)
        if DEBUG_MODE:
            print('setting diffuse_color: {}'.format(color_casco))
        else:
            if color_casco == 'sin_casco':
                bpy.data.objects["Hats"].hide_render = True
            else:
                bpy.data.objects[self.object_name].hide_render = False
                bpy.data.materials[self.material_name].node_tree.nodes["Diffuse BSDF"].inputs[0].default_value = diffuse_color_rgba
                bpy.data.materials[self.material_name].node_tree.nodes["Glossy BSDF"].inputs[0].default_value = glossy_color_rgba

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
#colores = ["azul", "azul"]
worker_cascos = WorkerCascos()
worker_chalecos = WorkerChalecos(script_path)
worker_camera = OrbitCamera(target_name='Hats')
n_samples = 1 #samples per frame
n_frames = 10 #total animated frames
total_images = n_frames*n_samples*len(colores)

if not DEBUG_MODE:
    n_frames = bpy.context.scene.frame_end
    
print('se gerarán {} imagenes'.format(total_images))    

for t in range(0,n_frames):
    next_frame(t)
    for color_casco in colores:
        #if DEBUG_MODE:
            #color_samples = np.ones((n_samples,n_samples*10,3),dtype=np.float64)
        for i in range(0,n_samples):
            print(color_casco)
            worker_chalecos.set_random_texture() # cambiar el color del chaleco
            worker_cascos.set_diffuse_color(color_casco) # cambiar el color del casco
            worker_camera.update_position() # move the camera
            render_filename = 'worker_{}_sample_{}_time_{}.png'.format(color_casco,i,t)
            render_output_path = os.path.join(output_folder,render_filename)
            
            do_render(render_output_path)
            """
            if DEBUG_MODE:     
                color_sample = worker_cascos.get_diffuse_noisy(color_casco)
                color_samples[:,i*10:(i+1)*10,:] = color_samples[:,i*10:(i+1)*10,:]*color_sample[0:3]
            """
        #if DEBUG_MODE:
            #print(color_sample)
            #print(color_samples.min())
            #print(color_samples.max())
            #io.imshow(color_samples)
            #io.show()


        
