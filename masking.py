from PIL import Image
import numpy as np

# Load ROI and mask images
roi_image = Image.open("roi.png")
mask_image = Image.open("mask.png")

# Ensure both images have the same dimensions
roi_image = roi_image.resize(mask_image.size)

# Convert the images to NumPy arrays
roi_array = np.array(roi_image)
mask_array = np.array(mask_image)

# Create a new transparent image with the same dimensions as ROI image
result_array = np.zeros_like(roi_array, dtype=np.uint8)

# Mask the ROI image based on the mask using NumPy
mask_black = (mask_array[..., 0] == 0)  # Check only the red channel for black pixels
result_array[mask_black] = [0, 0, 0, 0]

# Use a mask to copy the ROI pixels where the mask is white
mask_white = (mask_array[..., 0] != 0)  # Check only the red channel for white pixels
result_array[mask_white] = roi_array[mask_white]

# Convert the NumPy array back to an image
result_image = Image.fromarray(result_array)

# Save the result image
result_image.save("result.png")
