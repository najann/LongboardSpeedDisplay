import logging
from time import sleep

from calc_speed import calculate_speed, get_rows
from color_matrix import initialize, light_up
from get_color import define_color, extract_value


def main():
    while True:
        logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO, filename='speed.log')
        hue = extract_value('art.png')
        old_color = new_color || "start"
        new_color = define_color(hue)
        speed = calculate_speed(old_color, new_color)
        device = initialize()
        rows = get_rows(speed)
        image = light_up(rows)
        logging.warning("Hue: {} - Color: {} ".format(hue, color))
        device.display(image)
        
    device.clear()

if __name__ == "__main__":
	main()
    
