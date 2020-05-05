from time import sleep

from picamera import PiCamera


camera = PiCamera()
camera.start_preview()
camera.rotation = 180
camera.brightness = 75
camera.capture('./image3.jpg')
# for i in range(5):
#     sleep(5)
#     camera.capture('./image%.jpg' % i)
# camera.stop_preview()

# camera.resolution = (2592, 1944)
# camera.framerate = 15
# camera.brightness = 70
# camera.contrast = 1

#for effect in camera.EXPOSURE_MODES:
#    camera.exposure_mode = effect
#    camera.annotate_text = "Effect: %s" % effect
#    camera.capture('./image%s.jpg' % effect)
#    sleep(1)

camera.stop_preview()
