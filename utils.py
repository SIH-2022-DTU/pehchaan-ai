import shutil
import os
import cv2
import boto3, botocore
from werkzeug.utils import secure_filename
import os
import numpy
import io
import pickle
import string
import random

S3_BUCKET = os.environ.get("S3_BUCKET")
S3_KEY = os.environ.get("S3_ACCESS_KEY")
S3_SECRET = os.environ.get("S3_SECRET_KEY")
S3_REGION = os.environ.get("S3_REGION")
def delete_create_dir(path):
    if (os.path.exists(path) == True):
        shutil.rmtree(path)

    os.mkdir(path)
    return

def show_image(image):
    cv2.imshow('Image',image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


s3 = boto3.client(
   "s3",
   aws_access_key_id=S3_KEY,
   aws_secret_access_key=S3_SECRET
)
def create_temp(img):
    
  
    # initializing size of string 
    N = 10
    
    # using random.choices()
    # generating random strings 
    res = ''.join(random.choices(string.ascii_uppercase +
                                string.digits, k = N))
  
    # print result
    save_path = "./temp/" + res + ".png"
    cv2.imwrite(save_path,img)
    return save_path
    

def upload_file_to_s3(file, bucket_name=S3_BUCKET, acl="public-read"):

    """
    Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
    """

    try:

        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        print("Something Happened: ", e)
        return e

    return file.filename

# only for uploading image function to S3. Nothing to do with preprocessing
def upload_file(imageFile):
    file_path = create_temp(imageFile)
    print(file_path)
    # img = cv2.imread('g4g.png')
    # file = file_path
    
    """
        These attributes are also available

        file.filename               # The actual name of the file
        file.content_type
        file.content_length
        file.mimetype

    """
    bucket = S3_BUCKET
    file_name = file_path
    key_name = secure_filename(file_name)
    s3.upload_file(file_name, bucket, key_name)
    s3_path= "https://" + S3_BUCKET + ".s3." + S3_REGION + ".amazonaws.com/" + key_name
    print(s3_path)
    return s3_path
    # if no file name then select a file
    if file.filename == "":
        return "Please select a file"

    # D.
    if file:
        file.filename = secure_filename(file.filename)
        output = upload_file_to_s3(file)
        return "https://" + S3_BUCKET + ".s3." + S3_REGION + ".amazonaws.com/" + output
    else:
        return null