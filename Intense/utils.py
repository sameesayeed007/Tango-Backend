from PIL import Image
from Intense.models import CompanyInfo,Banner,RolesPermissions,Banner_Image,Currency,Settings,Theme,APIs
from io import BytesIO
from django.core.files import File

def get_image(image_path, width = 300, height = 168):
    '''
    This method is for resizing images. It takes image path, width and height as an argumant and return resized image.
    '''
    image = Image.open(image_path)
    image = image.resize((width,height))
    return image

def get_roles_id(value_name):
    try:
        value_id = RolesPermissions.objects.filter(roleType= value_name).values('id')
        return value_id[0]['id']
    except:
        pass 


