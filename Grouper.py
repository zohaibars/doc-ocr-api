from easy_ocr import bounding_box
from config import BASE_FOLDER,CROPS
import os 
import cv2
image_path=r"TestSample\GrouperTest\18-47-03-312.jpg"
temp_name=0
img,results,lang=bounding_box(input_image=image_path)
os.makedirs(os.path.join(BASE_FOLDER,CROPS),exist_ok=True)

for i, (bbox, _, _) in enumerate(results):
    (tl, tr, br, bl) = bbox
    tl = (int(tl[0]), int(tl[1]))
    br = (int(br[0]), int(br[1]))
    crop_object =img[tl[1]:br[1], tl[0]:br[0]]
    store_image_path=os.path.join(BASE_FOLDER,CROPS,str(temp_name)+".png")
    cv2.imwrite(store_image_path, crop_object)
    temp_name=temp_name+1

