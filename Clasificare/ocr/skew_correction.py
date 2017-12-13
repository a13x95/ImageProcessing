import numpy as np
import cv2


def skew_correct(image_path):
    image = cv2.imread(image_path)

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_image = cv2.bitwise_not(gray_image)

    thresholded_image = cv2.threshold(gray_image, 0, 255,
                                      cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    foreground_coords = np.column_stack(np.where(thresholded_image > 0))
    text_angle = cv2.minAreaRect(foreground_coords)[-1]

    if text_angle <= -45:
        text_angle = -1*(90 + text_angle)

    else:
        text_angle = -1*text_angle

    (height, width) = image.shape[:2]
    center = (width // 2, height // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, text_angle, 1.0)
    rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height),
                                   flags=cv2.INTER_CUBIC,
                                   borderMode=cv2.BORDER_REPLICATE)

    return rotated_image
