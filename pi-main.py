import cv2
import cv2.aruco as aruco
import numpy as np
from PIL import Image
import picamera
from io import BytesIO


# Create a PiCamera instance
camera = picamera.PiCamera()

# Set camera resolution (optional)
camera.resolution = (640, 480)
camera.brightness = 70
camera.contrast = 70
camera.saturation = 0
camera.awb_mode = 'incandescent'

# Create an OpenCV VideoCapture object
cap = cv2.VideoCapture()

# Create an in-memory stream for capturing images without saving to disk
stream = BytesIO()



"""# Check if the webcam is opened successfully
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()
"""
markerIds=None

# Define the ArUco dictionary and parameters
aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_100)
parameters = aruco.DetectorParameters_create()

camera.start_preview()


while (markerIds is None or len(markerIds)!=4):

    camera.capture(stream, format='png')
    
    # Reset the stream position to the beginning
    stream.seek(0)
    
    # Read the image from the stream using OpenCV
    frame = cv2.imdecode(np.frombuffer(stream.read(), dtype=np.uint8), 1)
    #ret, frame = cap.read()
    #cv2.imshow("Window", frame)
    #cv2.waitKey(1)
    # Detect ArUco markers in the image
    corners, markerIds, rejectedCandidates = aruco.detectMarkers(frame, aruco_dict, parameters=parameters)
    #print(len(markerIds))

camera.stop_preview()

boundingBoxCorners=[[0, 0], [0, 0], [0, 0], [0, 0]]
if markerIds is not None:
    print("Aruco Detected")
    for i in range(len(markerIds)):
        #print("--"+str(markerIds[i])+"--")
        #print(corners[i][0])
        
        # Draw a red bounding box around the detected ArUco code on the original frame
        corner=corners[i][0]
        if(markerIds[i]==0):
            boundingBoxCorners[0][0]=corner[3][0]
            boundingBoxCorners[0][1]=corner[3][1]
            #boundingBoxCorners.insert(0,corners[i][0][3])
        if(markerIds[i]==1):
            boundingBoxCorners[1][0]=corner[2][0]
            boundingBoxCorners[1][1]=corner[2][1]

        if(markerIds[i]==2):
            boundingBoxCorners[2][0]=corner[1][0]
            boundingBoxCorners[2][1]=corner[1][1]

        if(markerIds[i]==3):
           boundingBoxCorners[3][0]=corner[0][0]
           boundingBoxCorners[3][1]=corner[0][1]
        
    #print(boundingBoxCorners)    
        
    # Calculate the width and height of the bounding box
    width = np.linalg.norm(boundingBoxCorners[0][0] - boundingBoxCorners[1][0])
    height = np.linalg.norm(boundingBoxCorners[1][1] - boundingBoxCorners[2][1])

    #print(width)
    #print(height)
    #print(boundingBoxCorners)
    # Get the rotation matrix and apply the perspective transform to extract the ROI
    pts1 = np.float32(boundingBoxCorners)
    pts2 = np.float32([[0, 0], [width, 0], [width, height],[0, height] ])  # Define the bounding box size dynamically

    M = cv2.getPerspectiveTransform(pts1, pts2)
    roi = cv2.warpPerspective(frame, M, (int(width), int(height)))

    # Save the ROI as a separate image
    cv2.imwrite(f'roi.png', roi)       

# Save the first image with red bounding boxes around the ArUco codes
cv2.polylines(frame, [np.int32(corners[i])], isClosed=True, color=(0, 0, 255), thickness=2)
#cv2.imwrite('original_with_bounding_boxes.png', frame)


# Load ROI and mask images
roi_image = Image.open("roi.png")
mask_image = Image.open("mask.png")
roi_image=roi_image.copy()
# Ensure both images have the same dimensions
roi_image = roi_image.resize(mask_image.size)

# Create a new transparent image with the same dimensions as ROI image
result_image = Image.new("RGBA", roi_image.size, (0, 0, 0, 0))

# Iterate through each pixel in the mask and apply the mask to ROI
for x in range(mask_image.width):
    for y in range(mask_image.height):
        pixel = mask_image.getpixel((x, y))
        roi_pixel = roi_image.getpixel((x, y))
        #print(pixel)
        if pixel == (0, 0, 0, 255):  # Black pixel in mask
            #print("Found Black Pixel")
            result_image.putpixel((x, y), (0, 0, 0, 0))  # Make it transparent
        else:  # White pixel in mask
            result_image.putpixel((x, y), roi_pixel)  # Copy ROI pixel

# Save the result image
result_image.save("result.png")
