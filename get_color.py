import colorsys
from PIL import Image


def extract_value(pic):
    if isinstance(pic, str):
        with Image.open(pic) as im:
            px = im.load()
            size = px.size
        pic = px[size[0] // 2, size[1] // 2]
    # print(f"HLS: {colorsys.rgb_to_hls(pval[0]/255, pval[1]/255, pval[2]/255)}")
    # print(f"HSV: {colorsys.rgb_to_hsv(pval[0]/255, pval[1]/255, pval[2]/255)}")
    # print(f"H: {int(colorsys.rgb_to_hsv(pval[0]/255, pval[1]/255, pval[2]/255)[0]*360)}")
    hsv = colorsys.rgb_to_hsv(pic[0] / 255, pic[1] / 255, pic[2] / 255)
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
        else:
            # black
            return 6
    else:
        if (hue <= 35 and hue >= 0) or (hue > 330 and hue <= 360):
            # red
            return 3
        elif hue > 35 and hue <= 65:
            # yellow
            return 5
        elif hue > 65 and hue <= 175:
            # green
            return 4
        elif hue > 175 and hue <= 265:
            # blue
            return 1
        else:
            return 0
