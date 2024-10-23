"""
Paper: "UTRNet: High-Resolution Urdu Text Recognition In Printed Documents" presented at ICDAR 2023
Authors: Abdur Rahman, Arjun Ghosh, Chetan Arora
GitHub Repository: https://github.com/abdur75648/UTRNet-High-Resolution-Urdu-Text-Recognition
Project Website: https://abdur75648.github.io/UTRNet/
Copyright (c) 2023-present: This work is licensed under the Creative Commons Attribution-NonCommercial
4.0 International License (http://creativecommons.org/licenses/by-nc/4.0/)
"""

import os
import pytz
import math
import argparse
from PIL import Image
from datetime import datetime

import torch
import torch.utils.data

from model import Model
from dataset import NormalizePAD
from STT.utils import CTCLabelConverter, AttnLabelConverter, Logger
import glob
FeatureExtraction="HRNet" 
device_id=None 

def read(character, device,file_path,output_channel):
     

    image_path=file_path   
    saved_model="best_norm_ED.pth" 
    batch_max_length=100 
    imgH=32  
    imgW=400 
    rgb=False
    SequenceModeling="DBiLSTM" 
    Prediction="CTC" 
    num_fiducial=20 
    input_channel=1 
    output_channel=output_channel
    hidden_size=256 
    device = device
    os.makedirs("read_outputs", exist_ok=True)
    datetime_now = str(datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%Y-%m-%d_%H-%M-%S"))
    logger = Logger(f'read_outputs/{datetime_now}.txt')
    """ model configuration """
    if 'CTC' in Prediction:
        converter = CTCLabelConverter(character)
    else:
        converter = AttnLabelConverter(character)
    num_class = len(converter.character)

    if rgb:
        input_channel = 3
    opt=[image_path,saved_model,batch_max_length,imgH,imgW,rgb,FeatureExtraction,SequenceModeling,Prediction,num_fiducial,input_channel,output_channel,hidden_size,device_id,num_class,device]
    # opt=[image_path 0,saved_model 1,batch_max_length 2,imgH 3,imgW 4,rgb 5,FeatureExtraction 6,SequenceModeling 7,Prediction 8,num_fiducial 9,input_channel 10,output_channel 11,hidden_size 12,device_id 13,num_class 14]

    model = Model(opt)
    logger.log('model input parameters', imgH, imgW, num_fiducial, input_channel, output_channel,
          hidden_size, num_class, batch_max_length, FeatureExtraction,
          SequenceModeling, Prediction)
    model = model.to(device)

    # load model
    model.load_state_dict(torch.load(saved_model, map_location=device))
    logger.log('Loaded pretrained model from %s' % saved_model)
    model.eval()
    
    if rgb:
        img = Image.open(image_path).convert('RGB')
    else:
        img = Image.open(image_path).convert('L')
    img = img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    w, h = img.size
    ratio = w / float(h)
    if math.ceil(imgH * ratio) > imgW:
        resized_w = imgW
    else:
        resized_w = math.ceil(imgH * ratio)
    img = img.resize((resized_w, imgH), Image.Resampling.BICUBIC)
    transform = NormalizePAD((1, imgH, imgW))
    img = transform(img)
    img = img.unsqueeze(0)
    # print(img.shape) # torch.Size([1, 1, 32, 400])
    batch_size = img.shape[0] # 1
    img = img.to(device)
    preds = model(img)
    preds_size = torch.IntTensor([preds.size(1)] * batch_size)
    
    _, preds_index = preds.max(2)
    preds_str = converter.decode(preds_index.data, preds_size.data)[0]
    
    logger.log(preds_str)

if __name__ == '__main__':

   
    if FeatureExtraction == "HRNet":
        output_channel = 32
    """ vocab / character number configuration """
    file = open("UrduGlyphs.txt","r",encoding="utf-8")
    content = file.readlines()
    content = ''.join([str(elem).strip('\n') for elem in content])
    character = content+" "
    
    cuda_str = 'cuda'
    if device_id is not None:
        cuda_str = f'cuda:{device_id}'
    device = torch.device(cuda_str if torch.cuda.is_available() else 'cpu')
    print("Device : ", device)
    all_images=glob.glob(r'TestSample\UrduOCR Test/*.png')
    for i in all_images:
        read(character, device,file_path=i,output_channel=32)   