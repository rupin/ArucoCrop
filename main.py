import cv2
import numpy as np


dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)
parameters =  cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(dictionary, parameters)

frame = cv2.imread("your_image.png")

corners, markerIds, rejectedCandidates = detector.detectMarkers(frame)

#print(corners)
# Check if any ArUco markers are detected
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

    print(width)
    print(height)
    print(boundingBoxCorners)
    # Get the rotation matrix and apply the perspective transform to extract the ROI
    pts1 = np.float32(boundingBoxCorners)
    pts2 = np.float32([[0, 0], [width, 0], [width, height],[0, height] ])  # Define the bounding box size dynamically

    M = cv2.getPerspectiveTransform(pts1, pts2)
    roi = cv2.warpPerspective(frame, M, (int(width), int(height)))

    # Save the ROI as a separate image
    cv2.imwrite(f'roi.png', roi)       

# Save the first image with red bounding boxes around the ArUco codes
cv2.polylines(frame, [np.int32(corners[i])], isClosed=True, color=(0, 0, 255), thickness=2)
cv2.imwrite('original_with_bounding_boxes.png', frame)
