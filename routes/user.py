from fastapi import APIRouter, File, UploadFile
from typing import List
from PIL import Image
from io import BytesIO
from models.user import User
from config.db import db
from schemas.user import serializeDict, serializeList
from super_resolution import get_high_resolution
import utils
import numpy as np

user = APIRouter()

@user.get("/api/v1/users")
async def get_users():
    users = serializeList(db.users.find())
    return users

@user.post("/api/v1/users")
async def create_user(user: User):
    db.users.insert_one(dict(user))
    return serializeDict(user)

@user.post("/api/v1/verify")
async def upload(files: List[UploadFile] = File(...)):

    # in case you need the files saved, once they are uploaded
    for file in files:
        
        contents = await file.read()
        print(contents)

        try:
            img = np.array(Image.open(BytesIO(contents)))
        except:
            # raise Exception(f"Couldn't read")
            print(f"Cound't read file : Invalid file format")
            # msg = f"Cound't read file : Invalid file format"

            
        if(img.shape[0]*img.shape[1] < 512*512):
            image_prediction = get_high_resolution(img)
        else :
            image_prediction = img



        # get s3 link from here and save it in the database. Then return 200

        # image_prediction = cv2.cvtColor(image_prediction,cv2.COLOR_RGB2BGR)
        # utils.show_image(image_prediction)
        # return get_high_resolution(img)

    return {"Uploaded Filenames": [file.filename for file in files]}
    