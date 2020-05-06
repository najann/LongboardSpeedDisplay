import logging
import os
from time import sleep

from picamera import PiCamera

from calc_speed import calculate_speed
from color_matrix import initialize, light_up
from get_color import define_color, extract_value



def main():
    camera = PiCamera()
    # camera.start_preview()
    camera.rotation = 180
    camera.brightness = 75
    camera.contrast = 10
    i = 0
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO, filename='speed.log')
    device = initialize()
    new_color = 0
    device.display(light_up(1)) # show ready
    
    while True:
        camera.capture('./image{}.jpg'.format(i))
        hue = extract_value('./image{}.jpg'.format(i))
        old_color = new_color
        new_color = define_color(hue)
        speed = calculate_speed(old_color, new_color)
        image = light_up(speed)
        logging.info("Hue: {} - Old: {} - New: {} - Speed: {} ".format(hue, old_color, new_color, speed))
        print("Hue: {} - Old: {} - New: {} - Speed: {} ".format(hue, old_color, new_color, speed))
        device.display(image)
        #os.remove('./image{}.jpg'.format(i))
        i = i + 1
        sleep(0.02)
        
    device.clear()
    # camera.stop_preview()
    camera.close()


if __name__ == "__main__":
	main()
    
