#!/usr/bin/env python3

import argparse
import shutil
import os
from lib.config import config
import lib.UVtoolsBootstrap as uvtools
from gimpformats.gimpXcfDocument import GimpDocument
import glob
from System import Array, Double, Byte
from Emgu.CV import Mat, Image
from Emgu.CV.Structure import Gray
import System
from lib.array_convert import asNetArray
import numpy as np
parser = argparse.ArgumentParser(description='Convert gimp to 3d print.')
parser.add_argument('command', type=str, choices=["convert", "template", "open"])
parser.add_argument('file', type=str, default="pattern.xcf", nargs='?', help='filename')
args = parser.parse_args()
if args.command == "template":
    shutil.copyfile("templates/template.xcf", args.file)
elif args.command == "open":
    if os.path.isfile(args.file):
        os.system(f"open {config['gimppath']} {args.file}")
    else:
        print("file does not exist")
        exit(-1)
elif args.command =="convert":
    print(f'{uvtools.About.SoftwareWithVersionArch}')
    project = GimpDocument(args.file)

    layers = project.layers

    index = 0

    images = {}
    files = glob.glob('output-images/*') + glob.glob('output-print/*')
    for f in files:
        os.remove(f)
    for layer in layers:
        if layer.isGroup:
            continue
        image = layer.image.convert('L')
        image.save(f"output-images/{layer.name}.png")
        images[layer.name] = image
    file = "templates/template.pwmb"
    for (layername, image) in images.items():

        slicerFile = uvtools.FileFormat.Open(file)
        if slicerFile is None:
            print(f"Unable to open {file}")
            exit(-1)

        oldMat = slicerFile.GetLayer(0).LayerMat
        width, height = oldMat.Width, oldMat.Height

        cx, cy = width//2, height//2
        large_arr = np.zeros((height,width,1), dtype=np.uint8)
        small_arr = np.array(image)
        sw, sh = small_arr.shape[1], small_arr.shape[0]
        sx, sy = cx - sw//2, cy - sh//2
        large_arr[sy: sy+sh, sx:sx+sw,0] = small_arr
        large_arr[0,0,0]=255
        large_arr[-1,0,0]=255
        large_arr[0,-1,0]=255
        large_arr[-1,-1,0]=255

        net_array = asNetArray(np.array(large_arr))

        slicerFile.GetLayer(0).LayerMat = Image[Gray, Byte](net_array).Mat

        slicerFile.SaveAs(f"output-print/{layername}{os.path.splitext(file)[-1]}")

'''

file = "templates/pattern.pwmb"
slicerFile = None
try:
    slicerFile = uvtools.FileFormat.Open(file)
except Exception as e:
    print(e)
    exit(-1)

if slicerFile is None:
    print(f'Unable to find {file} or it\'s invalid file')
    exit(-1)
print(type(slicerFile))
mat = slicerFile.GetLayer(0).LayerMat

print(mat.Height,mat.Width)
ba = bytearray(uvtools.FileFormat.EncodeImage("PNG",mat))
newFile = open("filename.png", "wb")

newFile.write(ba)

for layer in slicerFile:
    print(type(layer))
'''
