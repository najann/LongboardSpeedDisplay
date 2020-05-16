import logging
import os
from collections import deque
from time import sleep
from time import time

from picamera import PiCamera
from picamera import array

from calc_speed import calculate_speed
from color_matrix import initialize, light_up
from get_color import define_color, extract_value


def main():
    try:
        with PiCamera() as camera:
            # camera.rotation = 180
            # camera.brightness = 65
            # camera.resolution = (1440, 960)
            camera.contrast = 10
            camera.awb_mode = 'sunlight'
            # camera.framerate = 90 # resolution => 720x480
            print(camera.resolution)
            i = 0
            logging.basicConfig(format='%(asctime)s - %(message)s',
                                level=logging.INFO, filename='speed.log')
            device = initialize()
            new_color = 0
            device.display(light_up(1)) # show ready
            camera.capture('./image1.jpg')
            last_speeds = deque(maxlen=10)
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
                    counter = counter + 1
                    start = time()
                    image = frame.array
                    hue = extract_value(image[170][360])
                    old_color = new_color
                    new_color = define_color(hue)
                    speed = calculate_speed(old_color, new_color)
                    if len(last_speeds) == 10:
                        last_speeds.popleft()
                    last_speeds.append(speed)
                    if counter == 10:
                        print(sum(last_speeds)//8)
                        image = light_up(sum(last_speeds)//8)
                        device.display(image)
                        counter = 0
                    logging.info(
                        "Hue: {} - Old: {} - New: {} - Speed: {} - Time: {} ".format(hue, old_color, new_color, speed, time() - start))
                    print("Hue: {} - Old: {} - New: {} - Speed: {} - Time: {} ".format(hue, old_color, new_color, speed, time() - start))
                    output.truncate(0)
                    sleep(0.09)

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

                
    except KeyboardInterrupt:
        device.clear()


if __name__ == "__main__":
    main()
