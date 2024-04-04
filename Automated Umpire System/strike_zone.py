import cv2
import mediapipe as mp

###########################################################################
# Builds a generic strike zone                                            #
# - Inputs: The video capture, Frame of video capture window that pops up #
###########################################################################

def generic_zone_builder(camera, frame):
    #Find the size of the frame
    frame_horizontal = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)) # x-axis
    frame_vertical = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)) # y-axis

    #Find the center of the frame
    frame_center = (frame_horizontal//2, frame_vertical//2)

    #Size of the zone
    zone_size = 200

    #Assign the coordinates needed to variables
    zone_x1 = (frame_horizontal//2) - zone_size//2
    zone_x2 = (frame_horizontal//2) + zone_size//2
    zone_y1 = (frame_vertical//2) - zone_size//2
    zone_y2 = (frame_vertical//2) + zone_size//2

    #Strike Zone starting and ending point
    zone_start = (zone_x1, zone_y1)
    zone_end = (zone_x2, zone_y2)

    #Strike Zone color and thickness
    zone_color = (255, 0, 0)
    zone_outline_thickness = 2

    #Strike Zone
    zone = cv2.rectangle(frame, zone_start, zone_end, zone_color, zone_outline_thickness) #cv2.rectangle(image, start_point, end_point, color, thickness)

###########################################################################
# Builds a unique strike zone based on information from batter_tracker.py #
# - Inputs: The video capture, Frame of video capture window that pops up #
###########################################################################

def personalized_strike_zone(camera, frame):
    # Find the size of the frame
    """
    frame_horizontal = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)) # x-axis
    frame_vertical = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)) # y-axis
    """
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

#############################################################################
# Looks at where the pitchs last location was prior to leaving the screen   #
# - If the pitch has a last location in the strike zone                     #
#   - return True                                                           #
# - If the pitch has a last location outside of the strike zone             #
#   - return False                                                          #
#############################################################################

def strike_or_ball(pitch_coordinates):
    for coordinates in pitch_coordinates: # Runs though the coordinates stores in the list
        pitch_x, pitch_y = coordinates # Assigns each pair of coordinates to variables
        if personalized_strike_zone.plate_start < pitch_x < personalized_strike_zone.plate_end: # Checks if pitch is within the width of the zone
            if personalized_strike_zone.upper_horizonatal < pitch_y < personalized_strike_zone.lower_horizontal: # Checks if the pitch is in the height of the zone
                return True
            else: # If pitch is within the width, but not height make sure to return False
                return False
        else:
            return False
