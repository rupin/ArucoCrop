from picamera import PiCamera
from time import sleep
camera = PiCamera()
camera.resolution = (640, 480)
camera.brightness = 50
camera.contrast = 70
camera.saturation = 50
camera.awb_mode = 'incandescent'
camera.start_preview()
sleep(5)
camera.capture('click.jpg')
camera.stop_preview()