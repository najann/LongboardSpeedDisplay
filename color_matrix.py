from PIL import Image
from time import sleep

from luma.core.interface.serial import noop, spi
from luma.core.render import canvas
from luma.led_matrix.device import max7219


_MX_SIZE = 8


def initialize():
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial)
    return device


def light_up(count):
    img = Image.new('1', (_MX_SIZE, _MX_SIZE))
    # augment number for better visualization
    count = count * 3
    full_rows = count // _MX_SIZE
    for row in range(full_rows):
        for col in range(_MX_SIZE):
            img.putpixel((col, row), 1)
    remainder = int(count % _MX_SIZE)
    for point in range(remainder):
        img.putpixel((point, full_rows), 1)
    return img