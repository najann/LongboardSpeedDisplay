import logging
import os
from collections import deque
from time import time

from picamera import PiCamera
from picamera import array

# from calc_speed import calculate_speed
from color_matrix import initialize, light_up
from get_color import define_color, extract_value


def main():
    with PiCamera() as camera:
        # camera.rotation = 180
        # camera.brightness = 65
        # camera.resolution = (1440, 960)
        camera.contrast = 10
        camera.awb_mode = 'sunlight'
        # camera.framerate = 90 # resolution => 720x480
        print(camera.resolution)
        logging.basicConfig(format='%(asctime)s - %(message)s',
                            level=logging.INFO, filename='speed.log')
        device = initialize()
        device.display(light_up(1))  # show ready
        camera.capture('./image1.jpg')
        last_speeds = deque(maxlen=1000)
        counter = 0

        # solution no. 1 takes about 0.4s
        # with array.PiRGBArray(camera) as output:
        #     while True:
        #         start = time()
        #         camera.capture(output, 'rgb')
        #         hue = extract_value(output.array[360][240])
        #         old_color = new_color
        #         new_color = define_color(hue)
        #         speed = calculate_speed(old_color, new_color)
        #         image = light_up(speed)
        #         logging.info(
        #             "Hue: {} - Old: {} - New: {} - Speed: {} - Time: {} ".format(hue, old_color, new_color, speed, time() - start))
        #         print("Hue: {} - Old: {} - New: {} - Speed: {} - Time: {} ".format(hue, old_color, new_color, speed, time() - start))
        #         device.display(image)
        #         i = i + 1
        #         output.truncate(0)
        #         duration = duration + (time() - start)
        #         print(duration/i)

        # takes 0.0034s on average per iteration
        with array.PiRGBArray(camera) as output:
            for frame in camera.capture_continuous(output, format="bgr", use_video_port=True):
                start = time()
                counter += 1
                image = frame.array
                hue = extract_value(image[170][360])
                color = define_color(hue)
                if color == 6:
                    continue
                last_speeds.append((color, time() - start))
                logging.info(
                    "Hue: {} - Color: {} - Speed: {} - Time: {} ".format(hue, color, speed, time() - start))
                print("Hue: {} - Color: {} - Speed: {} - Time: {} ".format(hue,
                                                                           color, speed, time() - start))
                if counter != 1000:
                    continue
                # measured in cm
                distance = 3.9 * sum(s for s, _ in last_speeds)
                # measured in s
                total_time = sum(t for _, t in last_speeds)
                km_per_h = distance/total_time * 0.036
                image = light_up(km_per_h)
                # image = light_up(sum(last_speeds)*4*0.036)
                device.display(image)
                counter = 0
                last_speeds.clear()
                logging.info(
                    "Hue: {} - Color: {} - Speed: {} - Time: {} ".format(hue, color, speed, time() - start))
                print("Hue: {} - Color: {} - Speed: {} - Time: {} ".format(hue,
                                                                           color, speed, time() - start))
                output.truncate(0)

        # about 0.1s slower than solution no.1
        # while True:
        #     start = time()
        #     camera.capture('./image{}.jpg'.format(i))
        #     hue = extract_value('./image{}.jpg'.format(i))
        #     old_color = new_color
        #     new_color = define_color(hue)
        #     speed = calculate_speed(old_color, new_color)
        #     image = light_up(speed)
        #     logging.info(
        #         "Hue: {} - Old: {} - New: {} - Speed: {} - Time: {} ".format(hue, old_color, new_color, speed, time() - start))
        #     print("Hue: {} - Old: {} - New: {} - Speed: {} - Time: {} ".format(hue, old_color, new_color, speed, time() - start))
        #     device.display(image)
        #     os.remove('./image{}.jpg'.format(i))
        #     i = i + 1
        #     duration = duration + (time() - start)
        #     print(duration/i)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        device.clear()
