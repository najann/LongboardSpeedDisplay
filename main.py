import logging
from time import sleep

from picamera import PiCamera

from calc_speed import calculate_speed, get_rows
from color_matrix import initialize, light_up
from get_color import define_color, extract_value



def main():
    try:
        camera = PiCamera()
        camera.start_preview()
        camera.rotation = 180
        camera.brightness = 75
        i = 0
        logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO, filename='speed.log')
        device = initialize()
        
        while True:
            camera.capture('./image{}.jpg'.format(i))
            hue = extract_value('art.png')
            old_color = new_color || 0
            new_color = define_color(hue)
            speed = calculate_speed(old_color, new_color)
            rows = get_rows(speed)
            image = light_up(rows)
            logging.warning("Hue: {} - Color: {} ".format(hue, color))
            device.display(image)
            os.remove('./image{}.jpg'.format(i))
            i = i + 1
            sleep(0.01)
            
        device.clear()
        camera.stop_preview()
        
    except:
        device.clear()
        camera.stop_preview()

if __name__ == "__main__":
	main()
    
