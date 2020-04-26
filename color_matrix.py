from PIL import Image
from time import sleep

from luma.core.interface.serial import noop, spi
from luma.core.render import canvas
from luma.led_matrix.device import max7219


def initialize():
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial)
    return device

def light_up(count):
    img = Image.new('1', (8, 8))
    for row in range(count):
        for col in range(8):
            img.putpixel((col, row), 1)
    return img
