import numpy as np
import os
import sys
import math
from PIL import Image, ImageDraw

def get_ied(x1,y1,x2,y2):
    d = (x1-x2)*(x1-x2)+(y1-y2)*(y1-y2)
    return int(np.sqrt(d))

def get_star_pos(p):
    xEyeLeft,yEyeLeft, xEyeRight, yEyeRight, xNose, yNose, xMouthLeft, yMouthLeft, xMouthRight, yMouthRight = tuple(p[1:])
    v=[]
    r= np.random.uniform(0.4, 0.7)
    v.append( (xNose+r*(xEyeLeft-xEyeRight) , yNose+r*(yEyeLeft-yEyeRight)))
    r= np.random.uniform(-0.7, -0.4)
    v.append( (xNose+r*(xEyeLeft-xEyeRight) , yNose+r*(yEyeLeft-yEyeRight)))
    r= np.random.uniform(0.1, 1.0)
    x = xEyeLeft + 0.6 * (xEyeLeft-xMouthLeft) + r * (xEyeRight-xEyeLeft)
    y = yEyeLeft + 0.6 * (yEyeLeft-yMouthLeft) + r * (yEyeRight-yEyeLeft)
    v.append( (x,y))
    return v

def read_qualECM(liste):
    v = {}
    with open(liste) as f:
        n=0
        for line in f:
            if n==0:
                n+=1
                # print (line)
            else:
                k = line.split()

                name= k[0]
                ied = get_ied(float(k[6]), float(k[7]), float(k[8]), float(k[9]))
                v[name]=[ied,float(k[6]), float(k[7]), float(k[8]), float(k[9]),float(k[10]), float(k[11]),float(k[12]), float(k[13]), float(k[14]), float(k[15])]
    return v


# Fonction pour dessiner une étoile à 5 branches sur une image
def draw_star(image_path, p, size, output_path):# size en cm
    colors = [(246,87,198),(249,217,39),(114,192,243)]
    size = size * p[0] / 6.5
    with Image.open(image_path) as img:
        # Créer un objet de dessin
        draw = ImageDraw.Draw(img)
        # Définir les coordonnées de l'étoile à 5 branches
        for x,y in get_star_pos(p):
            star_coordinates = [
                (x, y - size),  # Pointe du haut
                (x + size * 0.2245, y - size * 0.3090),  # Droite du haut
                (x + size * 0.9511, y - size * 0.3090),  # Droite
                (x + size * 0.3633, y + size * 0.1180),  # Droite du bas
                (x + size * 0.5878, y + size * 0.8090),  # Bas droite
                (x, y + size * 0.3810),  # Bas
                (x - size * 0.5878, y + size * 0.8090),  # Bas gauche
                (x - size * 0.3633, y + size * 0.1180),  # Gauche du bas
                (x - size * 0.9511, y - size * 0.3090),  # Gauche
                (x - size * 0.2245, y - size * 0.3090),  # Gauche du haut
            ]
            # Dessiner une étoile à 5 branches
            draw.polygon(star_coordinates, fill=colors[np.random.randint(0, 3)])
        # Sauvegarder l'image avec l'étoile
        img.save(output_path)

def draw_grid(image_path, p, transparency, output_path):# size en cm
    k = 0.00002  # Coefficient de distorsion
    # Fonction pour appliquer une distorsion en barillet
    def barrel_distortion(x, y, width, height, k):
        cx, cy = 0.8*width , 0.5*height # Centre de l'image
        dx, dy = x - cx, y - cy
        r = math.sqrt(dx * dx + dy * dy)
        factor = 1 + k * r * r
        new_x = cx + dx * factor
        new_y = cy + dy * factor
        return new_x, new_y

    with Image.open(image_path).convert("RGBA") as img:
        # Créer un objet de dessin
        width, height = img.size
        grid_image = Image.new('RGBA', (width, height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(grid_image)
        # draw = ImageDraw.Draw(img)
        grid_color = (0, 0, 255, transparency)
        grid_size = int(p[0]*0.1)  # Taille de chaque cellule de la grille
        # Dessiner les lignes verticales avec distorsion en barillet
        for x in range(0, img.width, grid_size):
            points = [barrel_distortion(x, y, img.width, img.height, k) for y in range(0, img.height)]
            draw.line(points, fill=grid_color)

        # Dessiner les lignes horizontales avec distorsion en barillet
        for y in range(0, img.height, grid_size):
            points = [barrel_distortion(x, y, img.width, img.height, k) for x in range(0, img.width)]
            draw.line(points, fill=grid_color)
    # Sauvegarder l'image
        combined_image = Image.alpha_composite(img, grid_image)
        combined_image.convert("RGB").save(output_path)


rep_images='ima/'

print("nb arg = ",len(sys.argv))
if len(sys.argv)==3:
    mode = sys.argv[1]
    size = int(sys.argv[2])
    transparency = int(sys.argv[2])
else:
    size = 10
    transparency = 128
    mode = "pimp_star" # "pimp_star" "grid"

rep = "tpl"
v = read_qualECM("%s/stem.log"%rep)

if mode == "pimp_star":
    out = "pimp"
    os.makedirs("%s_%02d/"%(out,size), exist_ok=True)
elif mode == "grid":
    out = "grid"
    os.makedirs("%s_%02d/" % (out, transparency), exist_ok=True)
else:
    print("unknow mode")


n=0
for ima in v:
    n+=1
    if mode == "pimp_star":
        draw_star(rep_images+ima, v[ima],0.1*size, "%s_%02d/"%(out,size)+ima)
    if mode == "grid":
        draw_grid(rep_images+ima, v[ima],transparency, "%s_%02d/"%(out,transparency)+ima)


# Message de succès
if mode == "pimp_star":
    print("Une étoile à 5 branches de taille %d a été dessinée sur %d images et sauvegardée dans %s_%02d"%(size,n,out,size))
if mode == "grid":
     print("Une grille de transparence %d a été dessinée sur %d images et sauvegardée dans %s_%02d" % (transparency, n, out, transparency))