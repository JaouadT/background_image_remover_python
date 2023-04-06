# Image Background Remover Python With U2Net

Remove backgrounds from images with u2net pre-trained model

This repo uses the model and the pre-trained weights described in the paper: *U2-Net: Going Deeper with Nested U-Structure for Salient Object Detection*.

Original repo: [U2-Net](https://github.com/xuebinqin/U-2-Net)

How to use:
1. Clone this repo.
2. Install requirements: `pip install -r requirements.txt`.
3. Run `segment.py` with the command: `python segment.py -img_path image.png`
4. Segmented image will be stored in the 
results folder.

Image: 
![alt text](image.png "Original image")

Segmented image: 
![alt text](/results/segmented_image.png "Original image")


