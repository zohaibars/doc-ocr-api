import math
from PIL import Image
import torch
from model import Model
from dataset import NormalizePAD
from utils import CTCLabelConverter, AttnLabelConverter

# Your model configuration
image_path=f""   
saved_model="best_norm_ED.pth" 
batch_max_length=100 
imgH=32  
imgW=400 
rgb=False
FeatureExtraction="HRNet"
SequenceModeling="DBiLSTM" 
Prediction="CTC" 
num_fiducial=20 
input_channel=1 
output_channel=512
hidden_size=256 
device_id=None
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print('device:',device)
if FeatureExtraction == "HRNet":
        output_channel = 32
else:
    output_channel=output_channel
""" 
vocab / character number configuration 
"""
file = open("UrduGlyphs.txt","r",encoding="utf-8")
content = file.readlines()
content = ''.join([str(elem).strip('\n') for elem in content])
character = content+" "
if 'CTC' in Prediction:
    converter = CTCLabelConverter(character)
else:
    converter = AttnLabelConverter(character)
num_class = len(converter.character)
opt=[image_path,saved_model,batch_max_length,imgH,imgW,rgb,FeatureExtraction,SequenceModeling,Prediction,num_fiducial,input_channel,output_channel,hidden_size,device_id,num_class,device]


# Load model
model = Model(opt)
model = model.to(device)

# Load model weights
model.load_state_dict(torch.load(saved_model, map_location=device))
print("urdu ocr loaded!!!")
model.eval()

# Character configuration
file = open("UrduGlyphs.txt", "r", encoding="utf-8")
content = file.readlines()
content = ''.join([str(elem).strip('\n') for elem in content])
character = content + " "

def read_image(image_path):
    """Perform OCR on an image."""
    # Model inference setup
    converter = CTCLabelConverter(character)

    if rgb:
        input_channel = 3
    else:
        input_channel = 1

    # Load and preprocess the image
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
    img = img.to(device)

    # Model inference
    preds = model(img)
    preds_size = torch.IntTensor([preds.size(1)] * 1)  # Assuming batch size is always 1 for inference
    _, preds_index = preds.max(2)
    preds_str = converter.decode(preds_index.data, preds_size.data)[0]

    return preds_str

# Example usage
# image_path= r"../TestSample/UrduOCR Test/chunk_First_4.png"

# output = read_image(image_path=image_path)
# print('output :',output)

