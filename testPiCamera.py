from picamera import PiCamera
from time import sleep
camera = PiCamera()
camera.resolution = (640, 480)
camera.brightness = 70
camera.contrast = 70
camera.saturation = 10
camera.awb_mode = 'auto'
camera.start_preview()
sleep(5)
camera.capture('click.jpg')
camera.stop_preview()