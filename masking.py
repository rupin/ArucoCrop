from PIL import Image

# Load ROI and mask images
roi_image = Image.open("roi.png")
mask_image = Image.open("mask.png")

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