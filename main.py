import logging
import numpy
import os
import sys
from collections import deque
from time import time

from picamera import PiCamera, array

from calc_speed import calculate_speed
from color_matrix import initialize, light_up
from get_color import define_color, extract_value


_SLICE_LENGTH = 3.9
_CONV_FAC = 0.036
_ITERATIONS = 50

def main(device):
    with PiCamera() as camera:
        # camera.rotation = 180
        # camera.brightness = 65
        camera.contrast = 10
        camera.awb_mode = 'sunlight'
        logging.basicConfig(format='%(asctime)s - %(message)s',
                            level=logging.INFO, filename='speed.log')
        device.display(light_up(1))  # show ready
        camera.capture('./image1.jpg')
        last_speeds = deque(maxlen=_ITERATIONS)
        counter = 0
        new_color = 0

        # camera.capture(output, 'rgb') takes about 0.4s
        # camera.capture('./image{}.jpg'.format(i)) takes about 0.5s
        # takes 0.0034s on average per iteration

        with array.PiRGBArray(camera) as output:
            start = time()
            for frame in camera.capture_continuous(output, format="bgr", use_video_port=True):
                counter += 1
                image = frame.array
                y_pos = image.shape[0] // 4
                x_pos = image.shape[1] // 2
                extract = image[y_pos:y_pos+10, x_pos:x_pos+10]

                avg_color_row = numpy.average(extract, axis=0)
                avg_color = numpy.average(avg_color_row, axis=0)
                # hue = extract_value(image[image.shape[0] // 3][image.shape[1] // 2])
                hue = extract_value(avg_color)
                output.truncate(0)

                if new_color == 6:
                    print("Interation Skipped")
                    continue

                old_color = new_color
                new_color = define_color(hue)
                slices = calculate_speed(old_color, new_color)
                last_speeds.append((slices, time() - start))
                logging.info("Hue: {} - Slice: {} - Time: {} ".format(hue, slices, time() - start))

                if counter != _ITERATIONS:
                    continue

                # measured in cm
                distance = _SLICE_LENGTH * sum(s for s, _ in last_speeds)
                # measured in s
                # total_time = sum(t for _, t in last_speeds)
                km_per_h = distance/(time()-start) * _CONV_FAC
                logging.info("Speed: {} - Distance: {} - Time: {} ".format(km_per_h, distance, time() - start))
                image = light_up(int(km_per_h))
                device.display(image)
                counter = 0
                last_speeds.clear()
                start = time()


if __name__ == "__main__":
    try:
        device = initialize()
        main(device)
    except KeyboardInterrupt:
        device.clear()
