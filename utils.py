import os
import secrets

from PIL import Image
from config import PATH_UPLOAD_IMAGE


def resize_pic(pic, a, b):
    random_name_pic = secrets.token_hex(20)
    _, file_ext = os.path.splitext(pic.filename)
    picture_fn = random_name_pic + file_ext
    full_path = PATH_UPLOAD_IMAGE
    if not os.path.exists(full_path):
        os.makedirs(full_path)
    picture_path = os.path.join(full_path, picture_fn)
    output_size = (a, b)
    image = Image.open(pic)
    image.thumbnail(output_size)
    image.save(picture_path)
    return picture_path
