
"""
The purpose of this code is to check that the center of the image is inside a circle.
If this is the case the circle is drawn in green, else it's drawn in red.
https://opencv24-python-tutorials.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_houghcircles/py_houghcircles.html
"""

import cv2
import numpy as np


def is_inside(circle_x: int, circle_y: int,
              rad: int, x_pos: int, y_pos: int) -> bool:
    """
    Compare radius of circle with distance of its center from given point
    :param circle_x: X center of the circle
    :param circle_y: Y center of the circle
    :param rad: Radius of the circle
    :param x_pos: X position of the point you want to check if it is in the circle
    :param y_pos: Y position of the point you want to check if it is in the circle
    :return: True if it is inside else false
    """
    return True if (x_pos - circle_x) * (x_pos - circle_x) + (y_pos - circle_y) * (y_pos - circle_y) <= rad * rad\
        else False


# Reading the image
img = cv2.imread('rond_inside.png')

output = img.copy()
gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)  # Convert to black and white picture

# Reduce noise
gray = cv2.medianBlur(gray, 5)

# Detect circles
circles = cv2.HoughCircles(
    gray,
    cv2.HOUGH_GRADIENT,
    dp=1,
    minDist=10000,
    param1=100,
    param2=40,
    minRadius=0,
    maxRadius=0
)

# Getting the height and width of the image
height = output.shape[0]
width = output.shape[1]

# Get the center of the image
center_height = int(height / 2)
center_width = int(width / 2)

# Draw only the first detected circle
if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        print(i)
        x, y, r = circles[0][0]

        cv2.circle(output, (x, y), 2, (255, 0, 0), 3)  # Center point

        # Check if the center of the image is in the circle
        center_is_inside = is_inside(int(x), int(y), int(r), center_width, center_height)

        color = (0, 255, 0) if center_is_inside else (0, 0, 255)
        cv2.circle(output, (x, y), r, color, 2)  # Circle outline

# Drawing the lines
cv2.line(output, (0, 0), (width, height), (0, 0, 0), 1)
cv2.line(output, (width, 0), (0, height), (0, 0, 0), 1)

# Show result
cv2.imshow('Detected Circle', output)
cv2.waitKey(0)
cv2.destroyAllWindows()
