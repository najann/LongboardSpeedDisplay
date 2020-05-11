import logging
import os
from time import sleep
from time import time

from picamera import PiCamera
from picamera import array

from calc_speed import calculate_speed
from color_matrix import initialize, light_up
from get_color import define_color, extract_value


def main():
    with picamera.PiCamera() as camera:
        camera.rotation = 180
        camera.brightness = 75
        camera.contrast = 10
        i = 0
        logging.basicConfig(format='%(asctime)s - %(message)s',
                            level=logging.INFO, filename='speed.log')
        device = initialize()
        new_color = 0
        device.display(light_up(1))  # show ready

        while True:
            with picamera.array.PiRGBArray(camera) as output:  # PiArrayOutput
                camera.capture(output, 'rgb')
                print(output.array.shape[0], output.array.shape,
                      output.array[360][240])
            start = time()
            camera.capture('./image{}.jpg'.format(i))
            hue = extract_value('./image{}.jpg'.format(i))
            old_color = new_color
            new_color = define_color(hue)
            speed = calculate_speed(old_color, new_color)
            image = light_up(speed)
            duration = time() - start
            logging.info(
                "Hue: {} - Old: {} - New: {} - Speed: {} - Time: {} ".format(hue, old_color, new_color, speed, duration))
            print("Hue: {} - Old: {} - New: {} - Speed: {} - Time: {} ".format(hue,
                                                                               old_color, new_color, speed, duration))
            device.display(image)
            # os.remove('./image{}.jpg'.format(i))
            i = i + 1
            sleep(0.1)

        device.clear()


if __name__ == "__main__":
    main()
