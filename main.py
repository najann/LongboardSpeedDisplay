from time import sleep

from color_matrix import initialize, light_up
from get_color import define_color, extract_value


def main():
    hue = extract_value('art.png')
    color = define_color(hue)
    device = initialize()
    image = light_up(color)
    device.display(image)
    sleep(1)
    device.clear()

if __name__ == "__main__":
	main()
    
