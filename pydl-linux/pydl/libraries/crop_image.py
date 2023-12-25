from PIL import Image

def crop(path):
    # open the image with PIL
    img = Image.open(path)

    # get the width and height of the image
    width, height = img.size

    # calculate the center of the image
    center_x=width/2
    center_y=height/2

    # calculate the final width/height (w=h because square)
    half_length=(height-120)/2

    # calculate the coordinates relative to the center of the image    
    left = center_x - half_length
    right = center_x + half_length
    up = center_y - half_length
    down = center_y + half_length

    img = img.crop((left, up, right, down))
    img.save(path)