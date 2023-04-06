import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import cv2
import uuid
import os
import time

from model import U2NET
from torch.autograd import Variable
from skimage import io, transform
from PIL import Image
import requests
from io import BytesIO
import argparse
import gdown
from google_drive_downloader import GoogleDriveDownloader as gdd

ap = argparse.ArgumentParser()
ap.add_argument(
    '-img_path', '--image_path', required=True, help='path to input image'
)

args = vars(ap.parse_args())

input_image_path = args['image_path']

image_filename = input_image_path.split()

global model
print("---Loading Model---")
model_name = 'u2net'
model_dir = os.path.join('saved_models',
                            model_name, model_name + '.pth')
net = U2NET(3, 1)
if torch.cuda.is_available():
    net.load_state_dict(torch.load(model_dir))
    net.cuda()
else:
    net.load_state_dict(torch.load(model_dir, map_location='cpu'))
# ------- Load Trained Model -------
model = net
print("Loaded")

img = cv2.imread(input_image_path)
img_shape = img.shape

img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
initial_img = img.copy()

#  processing
image = transform.resize(img, (320, 320), mode='constant')

tmpImg = np.zeros((image.shape[0], image.shape[1], 3))

tmpImg[:, :, 0] = (image[:, :, 0]-0.485)/0.229
tmpImg[:, :, 1] = (image[:, :, 1]-0.456)/0.224
tmpImg[:, :, 2] = (image[:, :, 2]-0.406)/0.225

tmpImg = tmpImg.transpose((2, 0, 1))
tmpImg = np.expand_dims(tmpImg, 0)
image = torch.from_numpy(tmpImg)

image = image.type(torch.FloatTensor)
image = Variable(image)

d1, d2, d3, d4, d5, d6, d7 = model(image)
pred = d1[:, 0, :, :]
ma = torch.max(pred)
mi = torch.min(pred)
dn = (pred-mi)/(ma-mi)
pred = dn

predict = pred
predict = predict.squeeze()
predict_np = predict.cpu().data.numpy()
im = Image.fromarray(predict_np*255).convert('RGB')
# image = io.imread(image_name)
imo = im.resize((img_shape[1], img_shape[0]))
pb_np = np.array(imo)
# Make and apply mask
mask = pb_np[:, :, 0]
mask = np.expand_dims(mask, axis=2)
imo = np.concatenate((initial_img, mask), axis=2)
imo = Image.fromarray(imo, 'RGBA')
print("Saving....")
imo.save("results/segmented_image.png")
print("Saved....")