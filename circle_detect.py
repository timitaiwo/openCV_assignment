import cv2
import numpy as np

def red_filter(image):
    '''
    filter out colours other than red in the image
    '''

    lower_boundary = np.array([0,0,87])
    upper_boundary = np.array([90,90,255])
    
    mask = cv2.inRange(image, lower_boundary, upper_boundary)  # Filters out the RGB values within the range of the upper and lower boundaries
    filtered_red = cv2.bitwise_and(image, image, mask=mask) # Overlays the mask over the original image

    return filtered_red


def circle_detect(orig_image, red_image):
    '''
    detect cirle in inputed image (np image array)
    '''

    orig_image = orig_image.copy()

    # Convert image to greyscale and blur it to reduce noise
    gray = cv2.cvtColor(red_image, cv2.COLOR_BGR2GRAY)
    blurred_gray = cv2.medianBlur(gray, 15)

    # Detect Circles with Hough Transform
    rows = gray.shape[0]
    circles = cv2.HoughCircles(blurred_gray, cv2.HOUGH_GRADIENT, 1.5, rows/8, param1=100, param2=30, maxRadius=-1)

    if type(circles) != type(None):
        chosen_circle = circles[0][0] # Takes the first circle detected to reduce complexity

        circle_x, circle_y, _ = np.around(chosen_circle).astype(int)
        centre =(circle_x, circle_y)

        # circle center
        cv2.circle(blurred_gray, centre, 1, (0, 100, 100), 3)

        return blurred_gray, circle_x, circle_y
    
    else:
        return orig_image, None, None

def circle_centre(image):
    '''
    Returns the centre of circle in the image
    '''

    return circle_detect(image, red_filter(image))