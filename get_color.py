import colorsys
from PIL import Image


def extract_value(pic):
    with Image.open(pic) as im:
        px = im.load()
    pval = px[360, 240]
    # print(pval[0], pval[1], pval[2])
    # print(f"HLS: {colorsys.rgb_to_hls(pval[0]/255, pval[1]/255, pval[2]/255)}")
    # print(f"HSV: {colorsys.rgb_to_hsv(pval[0]/255, pval[1]/255, pval[2]/255)}")
    # print(f"H: {int(colorsys.rgb_to_hsv(pval[0]/255, pval[1]/255, pval[2]/255)[0]*360)}")
    hsv = colorsys.rgb_to_hsv(pval[0] / 255, pval[1] / 255, pval[2] / 255)
    print(hsv)
    if hsv[1] <= 0.1 and hsv[2] >= 0.8:
        hue = "white"
    elif hsv[2] <= 0.3:
        hue = "black"
    else:
        hue = int(hsv[0] * 360)
    return hue

def define_color(hue):
    if type(hue) == str:
        if hue == "white":
            return 2
        else: #black
            return 2 #TODO
    else:
        if (hue <= 30 and hue >= 0) or (hue > 335 and hue <= 360):
            return 3 #"red" 
        elif hue > 30 and hue <= 65:
            return 5 #"yellow"
        elif hue > 65 and hue <= 165:
            return 4 #"green"
        elif hue > 165 and hue <= 275:
            return 1 #"blue
        else:
            return 0
