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
from PIL import Image as im

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
        # print(contents)
        filename=file.filename
        file_content_type = file.content_type
        print(filename)
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

        # get s3 link from here
        uploaded_image_url = utils.upload_file(image_prediction)


        print(uploaded_image_url)

    return {"Uploaded Filenames": [file.filename for file in files]}
    