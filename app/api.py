
import os
from fastapi import FastAPI ,File, Form, UploadFile
from app import config
from app.color_detect import detect_category
from pathlib import Path
detect_cat = FastAPI()

root_path = Path(os.getcwd())
input_file_path = os.path.join(root_path, 'input')

@detect_cat.get("/")
def read_root():
   return {"Status": "UP"}

@detect_cat.post("/get_plant_status/")
async def get_plant_status(uploaded_file: UploadFile = File(...)):
    path = input_file_path
    
    files_to_delete=os.listdir(path)
    for i in files_to_delete:
        os.remove(path+'/'+i)
    file_location = f"{path}/{uploaded_file.filename}"
    with open(file_location, "wb") as file_object:
        file_object.write(uploaded_file.file.read())
    try:          
        color, plant_status, action, time_stamp = detect_category(file_location)

        return {"detected color" : color,
                "plant status" : plant_status,
                "action" : action,
                "image time taken" : time_stamp
                }
    except Exception as e:
        raise(e)




    
