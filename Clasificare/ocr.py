from PIL import Image
import pytesseract
import argparse
import cv2
import os

# parse the argumnets
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to input image")
ap.add_argument("-p", "--preprocess", type=str, default="thresh",
                help="type of preprocessing to be done (thresholding or blur)")
ap.add_argument("-v", "--view", action='store_true',
                help="view the before and after image")
arguments = vars(ap.parse_args())

# load the input image and convert it to grayscale for easier ocr
input_image = cv2.imread(arguments["image"])
grayscale_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)

# check which type of preprocessing should be applied

if arguments["preprocess"] == "thresholding":
    grayscale_image = cv2.threshold(grayscale_image, 0, 255,
                                    cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

elif arguments["preprocess"] == "blur":
    grayscale_image = cv2.medianBlur(grayscale_image, 3)

# write the modified image on disk for the ocr
filename = "{}.png".format(os.getpid())
cv2.imwrite(filename, grayscale_image)

# load and call the tesseract ocr on the image opened as a Pillow image
# then delete the temporary image
output_text = pytesseract.image_to_string(Image.open(filename))
os.remove(filename)
print(output_text)

# if necessary, open the images for previewing

if arguments["view"]:
    cv2.imshow("Image", input_image)
    cv2.imshow("Output", grayscale_image)
    cv2.waitKey(0)
