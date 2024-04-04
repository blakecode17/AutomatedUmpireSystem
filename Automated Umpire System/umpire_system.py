from re import T
from tkinter import Frame
import cv2
import numpy as np
import mediapipe as mp
from screeninfo import get_monitors

# Open up a camera
camera = cv2.VideoCapture(0)

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
    #personalized_strike_zone(camera, frame)
    
    cv2.imshow("Automated Home Plate Umpire", frame) # Title of the window that opens up
 
    strike_count = 0
    ball_count = 0
    
    frame_vertical, frame_horizontal, _= frame.shape

    # Find the center of the horizontal aspect of the frame
    frame_horizontal_center = frame_horizontal//2

    # The width of home plate (To my closest estimation of what 17 inches is)
    home_plate = 320

    # Finds where zone needs to start and end based on the plate
    plate_start = frame_horizontal_center - (home_plate//2)
    plate_end = frame_horizontal_center + (home_plate//2)

    # Start of code that was previously batter_tracker.py
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()

    # Convert the frame to RGB for MediaPipe Pose
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    process_frame = pose.process(rgb_frame)

    if process_frame.pose_landmarks is not None:
        #Lefty Batter
        left_shoulder = process_frame.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
        left_shoulder_x = int(left_shoulder.x * frame_horizontal)
        left_shoulder_y = int(left_shoulder.y * frame_vertical)
        left_knee = process_frame.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE]
        left_knee_x = int(left_knee.x * frame_horizontal)
        left_knee_y = int(left_knee.y * frame_vertical)
        #Righty Batter
        right_shoulder = process_frame.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        right_shoulder_x = int(right_shoulder.x * frame_horizontal)
        right_shoulder_y = int(left_shoulder.y * frame_vertical)
        right_knee = process_frame.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE]
        right_knee_x = int(right_knee.x * frame_horizontal)
        right_knee_y = int(right_knee.y * frame_vertical)

        # The upper and lower horizonatal boundries of the zone
        upper_horizontal = min(left_shoulder_y, right_shoulder_y)
        lower_horizontal = max(left_knee_y, right_knee_y)

        # Strike Zone starting and ending point
        zone_start = (plate_start, upper_horizontal)
        zone_end = (plate_end, lower_horizontal)

        # Strike Zone color and thickness of the outline
        zone_color = (255, 0, 0)
        zone_outline_thickness = 2

        # Strike Zone
        zone = cv2.rectangle(frame, zone_start, zone_end, zone_color, zone_outline_thickness)

    for coordinates in pitch_coordinates: # Runs though the coordinates stores in the list
        pitch_x, pitch_y = coordinates # Assigns each pair of coordinates to variables
        if plate_start < pitch_x < plate_end: # Checks if pitch is within the width of the zone
            if upper_horizontal < pitch_y < lower_horizontal: # Checks if the pitch is in the height of the zone
                print("Strike")
                strike_count += 1
            else: # If pitch is within the width, but not height make sure to return False
                print("Ball")
                ball_count +=1
        else:
            print("Ball")
            ball_count += 1
    
    if strike_count < 2:
        print("Strike")
        strike_count += 1
    elif strike_count == 2:
        print("Strike 3, You're Out!")
        strike_count = 0
        ball_count = 0
    elif ball_count < 3:
        print("Ball")
        ball_count += 1
    elif ball_count == 3:
        print("Ball 4, Take your base!")
        ball_count = 0
        strike_count = 0

    if cv2.waitKey(70) == ord("f"): #Foul
        if strike_count >= 2:
            strike_count = strike_count - 1
        else:
            strike_count = strike_count + 1
            ball_count = ball_count - 1
        print('Foul')
    elif cv2.waitKey(80) == ord("p"): #HBP
        strike_count = 0
        ball_count = 0
        print('Hit By Pitch! Take Your Base')
    elif cv2.waitKey(72) == ord("h"): #Hit
        strike_count = 0
        ball_count = 0
        print('Hit')
    elif cv2.waitKey(79) == ord("o"): #Out
        strike_count = 0
        ball_count = 0
        print("You're Out")

    
    key = cv2.waitKey(1) & 0xFF == 27  # 27 is equal to the 'Esc' key. Pressing the 'Esc' key exits the tracking
    if key == 27:
        break

# Close all of the windows including the camera
cv2.destroyAllWindows()