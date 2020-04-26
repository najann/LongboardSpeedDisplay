import colorsys
from PIL import Image


def extract_value(pic):
    with Image.open(pic) as im:
        px = im.load()
    pval = px[5, 5]
    # print(pval[0], pval[1], pval[2])
    # print(f"HLS: {colorsys.rgb_to_hls(pval[0]/255, pval[1]/255, pval[2]/255)}")
    # print(f"HSV: {colorsys.rgb_to_hsv(pval[0]/255, pval[1]/255, pval[2]/255)}")
    # print(f"H: {int(colorsys.rgb_to_hsv(pval[0]/255, pval[1]/255, pval[2]/255)[0]*360)}")
    hue = int(colorsys.rgb_to_hsv(pval[0] / 255, pval[1] / 255, pval[2] / 255)[0] * 360)
    return hue

def define_color(hue):
    if hue <= 20 or hue > 335 and hue <= 360:
        return 1 #"red" 
    elif hue > 20 and hue <= 35:
        return 2 #"orange"
    elif hue > 35 and hue <= 70:
        return 3 #"yellow"
    elif hue > 70 and hue <= 170:
        return 4 #"green"
    elif hue > 170 and hue <= 190:
        return 5 #"light blue"
    elif hue > 190 and hue <= 265:
        return 6 #"blue"
    elif hue > 265 and hue <= 285:
        return 7 #"purple"
    elif hue > 285 and hue <= 335:
        return 8 #"pink"
    else:
        return 0
