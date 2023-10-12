import cv2

# Load ROI and mask images using OpenCV
roi_image = cv2.imread("ROI.png")
mask_image = cv2.imread("mask.png")

# Ensure both images have the same dimensions
mask_image = cv2.resize(mask_image, (roi_image.shape[1], roi_image.shape[0]))

# Create a binary mask where black pixels in the mask are 0, and all others are 1
binary_mask = cv2.inRange(mask_image, (0, 0, 0), (0, 0, 0))

# Invert the binary mask to keep white areas as 1
binary_mask = cv2.bitwise_not(binary_mask)

# Create a new image with transparency (4 channels)
result_image = cv2.cvtColor(roi_image, cv2.COLOR_BGR2BGRA)

# Apply the binary mask to set the alpha channel to 0 where the mask is 0
result_image[:, :, 3] = cv2.bitwise_and(result_image[:, :, 3], binary_mask)

# Save the result image
cv2.imwrite("result.png", result_image)
