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

def upload_file_to_s3(file,bucket_name=S3_BUCKET, acl="public-read"):

    """
    Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
    """
    # my_array = numpy.random.randn(10)

    # upload without using disk
    # my_array_data = io.BytesIO()
    
    # pickle.dump(file, my_array_data)
    
    # my_array_data.seek(0)
    print(type(file))
    # print(file)
    try:

        # s3.upload_fileobj(file, bucket_name, filename, ExtraArgs={'ACL': acl, 'ContentType': file_content_type})
        s3.put_object(
            ACL= acl,
            ContentType=file.content_type,
            Body=file,
            Bucket=bucket_name,
            Key=file.filename,
        )
        # s3.upload_fileobj(
        #     file,
        #     bucket_name,
        #     filename,
        #     ExtraArgs={
        #         "ACL": acl,
        #         "ContentType": file_content_type
        #     }
        # )

    except Exception as e:
        print("Something Happened: ", e)
        return e

    return file.filename

# only for uploading image function to S3. Nothing to do with preprocessing
def upload_file(imageFile):
    file_path = create_temp(imageFile)
    file = file_path
    """
        These attributes are also available

        filename               # The actual name of the file
        file.content_type
        file.content_length
        file.mimetype

    """

    # if no file name then select a file
    # if filename == "":
    #     return "Please select a file"

    # D.
    
    filename = secure_filename(file)
    output = upload_file_to_s3(filename)
    print(output)
    return "https://" + S3_BUCKET + ".s3." + S3_REGION + ".amazonaws.com/" + output
    