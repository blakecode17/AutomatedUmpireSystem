import cv2
import math
import mediapipe as mp

"""
NO LONGER IN USE
"""

###############################################################################
# Detects the batter when batter walks into view of the video capture         #
# - Finds the position of their chest (Substituted shoulders for chest)       #
#   - This becomes the upper horizontal boundary of the zone                  #
# - Finds the position of their knees                                         #
#   - This becomes the lower horizontal boundary of the zone                  #
# - Left & Right verticle boundarys based on the width of home plate          #
#   - Can be entered manually as home plate is a set width                    #
# *************************************************************************** #
# *Could possibly attempt for the chest and knees to br tracked continuously* #
# * - Strike zone would adjust with upward or downward movement of both     * #
# *************************************************************************** #
###############################################################################

def shoulders_to_knees(frame, frame_horizontal, frame_vertical):
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()

    process_frame = pose.process(frame)

    if process_frame.pose_landmarks is not None:
        # Lefty Batter
        left_shoulder = process_frame.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
        left_shoulder_x = int(left_shoulder.x * frame_horizontal)
        left_shoulder_y = int(left_shoulder.y * frame_vertical)
        left_knee = process_frame.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE]
        left_knee_x = int(left_knee.x * frame_horizontal)
        left_knee_y = int(left_knee.y * frame_vertical)

        # Righty Batter
        right_shoulder = process_frame.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        right_shoulder_x = int(right_shoulder.x * frame_horizontal)
        right_shoulder_y = int(left_shoulder.y * frame_vertical)
        right_knee = process_frame.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE]
        right_knee_x = int(right_knee.x * frame_horizontal)
        right_knee_y = int(right_knee.y * frame_vertical)
    
        return left_shoulder_y, right_shoulder_y, left_knee_y, right_knee_y
