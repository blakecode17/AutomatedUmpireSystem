from re import T
from tkinter import Frame
import cv2
import numpy as np
from strike_zone import personalized_strike_zone
from screeninfo import get_monitors

# Open up a camera
camera = cv2.VideoCapture(1)

# Define the boundries of the baseball
whiteUpper = (180, 18, 255)
whiteLower = (0, 0, 231)


# Frame height and width so that the size can be adjusted
screen = get_monitors()
frame_height = screen[0].height
frame_width = screen[0].width

# Empty list that will store the coordinates of the pitch
pitch_coordinates = []

while True:
    ret, frame = camera.read() # ret is a variable that holds true and returns it if the camera is available
    if ret != True: # If there is no camera availbale then the program will stop running
        break
    
    # Resize the frame & assign the resized frame to the frame variable
    frame = cv2.resize(frame, (frame_width, frame_height))
    
    # Makes the frame of the video into a HSV color space. 
    color_space = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Extract the white regions because a baseball is predominantly white
    mask_white = cv2.inRange(color_space, whiteLower, whiteUpper)

    # Find the contours within the mask
    contours, hierarchy = cv2.findContours(mask_white.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 

    if len(contours) > 0:
        max_contour = max(contours, key=cv2.contourArea)
        (x, y), radius = cv2.minEnclosingCircle(max_contour)
        center_coordinates = (int(x), int(y))
        if radius > 10:
            cv2.circle(frame, center_coordinates, int(radius), (0, 255, 0), 2) # circle(Image, center_coordinates, radius, color, thickness)
            pitch_coordinates.append(center_coordinates)

    # Insert the strike zone graphic somewhere here
    personalized_strike_zone(camera, frame)
    
    cv2.imshow("Automated Home Plate Umpire", frame) # Title of the window that opens up

    if cv2.waitKey(1) & 0xFF == 27:  # 27 is equal to the 'Esc' key. Pressing the 'Esc' key exits the tracking
        break

# Close all of the windows including the camera
cv2.destroyAllWindows()