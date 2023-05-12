#!/usr/bin/env python



import cv2
import math as m
import mediapipe as mp
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from std_msgs.msg import Int32




# Calculate distance
def findDistance(x1, y1, x2, y2):
    dist = m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist


# Calculate angle.
def findAngle(x1, y1, x2, y2):
    theta = m.acos((y2 - y1) * (-y1) / (m.sqrt(
        (x2 - x1) ** 2 + (y2 - y1) ** 2) * y1))
    degree = int(180 / m.pi) * theta
    return degree


"""python
Function to send alert. Use this function to send alert when bad posture detected.
Feel free to get creative and customize as per your convenience.
"""


def sendWarning():
    pass


# =============================CONSTANTS and INITIALIZATIONS=====================================#
# Initilize frame counters.
good_frames = 0
bad_frames = 0

# Font type.
font = cv2.FONT_HERSHEY_SIMPLEX

# Colors.
blue = (255, 127, 0)
red = (50, 50, 255)
green = (127, 255, 0)
dark_blue = (127, 20, 0)
light_green = (127, 233, 100)
yellow = (0, 255, 255)
pink = (255, 0, 255)

# Initialize mediapipe pose class.
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
# ===============================================================================================#


if __name__ == "__main__":
    # For webcam input replace file name with 0.
 
    time_publisher = rospy.Publisher('/bad_posture_time',Int32,queue_size=10)
    rospy.init_node('bad_posture', anonymous=True)
    # define subscriber on ROS topic '/webcam' with Image data 
    
    bridge = CvBridge()
    rate = rospy.Rate(10) # 1Hz
    last_image = None


    # callback function called when an image is recieved on '/webcam'
    def callback(data):
        global last_image
        # convert the recieved image into suitable format using CvBridge
        last_image = bridge.imgmsg_to_cv2(data, "bgr8")

    rospy.Subscriber('/webcam', Image, callback)


    #file_name = 'input.mp4'
    #cap = cv2.VideoCapture(0)
    while not rospy.is_shutdown():

        if last_image is not None:
 
            h, w = last_image.shape[:2]

            # Convert the BGR image to RGB.
            last_image = cv2.cvtColor(last_image, cv2.COLOR_BGR2RGB)

            # Process the image.
            keypoints = pose.process(last_image)

            # Convert the image back to BGR.
            last_image = cv2.cvtColor(last_image, cv2.COLOR_RGB2BGR)

            # Use lm and lmPose as representative of the following methods.
            lm = keypoints.pose_landmarks
            lmPose = mp_pose.PoseLandmark

            # Acquire the landmark coordinates.
            # Once aligned properly, left or right should not be a concern.      
            # Left shoulder.
            try:
                l_shldr_x = int(lm.landmark[lmPose.LEFT_SHOULDER].x * w)
                l_shldr_y = int(lm.landmark[lmPose.LEFT_SHOULDER].y * h)
                # Right shoulder
                r_shldr_x = int(lm.landmark[lmPose.RIGHT_SHOULDER].x * w)
                r_shldr_y = int(lm.landmark[lmPose.RIGHT_SHOULDER].y * h)
                # Left ear.
                l_ear_x = int(lm.landmark[lmPose.LEFT_EAR].x * w)
                l_ear_y = int(lm.landmark[lmPose.LEFT_EAR].y * h)
                # Left hip.
                l_hip_x = int(lm.landmark[lmPose.LEFT_HIP].x * w)
                l_hip_y = int(lm.landmark[lmPose.LEFT_HIP].y * h)
            except:
                last_image = None
                continue

            # Calculate distance between left shoulder and right shoulder points.
            offset = findDistance(l_shldr_x, l_shldr_y, r_shldr_x, r_shldr_y)

            # Assist to align the camera to point at the side view of the person.
            # Offset threshold 30 is based on results obtained from analysis over 100 samples.
            #if offset < 100:
            #    cv2.putText(last_image, str(int(offset)) + ' Aligned', (w - 150, 30), font, 0.9, green, 2)
            #else:
            #    cv2.putText(last_image, str(int(offset)) + ' Not Aligned', (w - 150, 30), font, 0.9, red, 2)

            # Calculate angles.
            neck_inclination = findAngle(l_shldr_x, l_shldr_y, l_ear_x, l_ear_y)
            torso_inclination = findAngle(l_hip_x, l_hip_y, l_shldr_x, l_shldr_y)

            # Draw landmarks.
            cv2.circle(last_image, (l_shldr_x, l_shldr_y), 7, yellow, -1)
            cv2.circle(last_image, (l_ear_x, l_ear_y), 7, yellow, -1)

            # Let's take y - coordinate of P3 100px above x1,  for display elegance.
            # Although we are taking y = 0 while calculating angle between P1,P2,P3.
            cv2.circle(last_image, (l_shldr_x, l_shldr_y - 100), 7, yellow, -1)
            cv2.circle(last_image, (r_shldr_x, r_shldr_y), 7, pink, -1)
            cv2.circle(last_image, (l_hip_x, l_hip_y), 7, yellow, -1)

            # Similarly, here we are taking y - coordinate 100px above x1. Note that
            # you can take any value for y, not necessarily 100 or 200 pixels.
            cv2.circle(last_image, (l_hip_x, l_hip_y - 100), 7, yellow, -1)

            # Put text, Posture and angle inclination.
            # Text string for display.
            angle_text_string = 'Neck : ' + str(int(neck_inclination)) + '  Torso : ' + str(int(torso_inclination))

            # Determine whether good posture or bad posture.
            # The threshold angles have been set based on intuition.
            if neck_inclination < 40 and torso_inclination < 10:
                bad_frames = 0
                good_frames += 1
                
                #cv2.putText(last_image, angle_text_string, (10, 30), font, 0.9, light_green, 2)
                #cv2.putText(last_image, str(int(neck_inclination)), (l_shldr_x + 10, l_shldr_y), font, 0.9, light_green, 2)
                #cv2.putText(last_image, str(int(torso_inclination)), (l_hip_x + 10, l_hip_y), font, 0.9, light_green, 2)

                # Join landmarks.
                cv2.line(last_image, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), green, 4)
                cv2.line(last_image, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 100), green, 4)
                cv2.line(last_image, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), green, 4)
                cv2.line(last_image, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), green, 4)

            else:
                good_frames = 0
                bad_frames += 1

                #cv2.putText(last_image, angle_text_string, (10, 30), font, 0.9, red, 2)
                #cv2.putText(last_image, str(int(neck_inclination)), (l_shldr_x + 10, l_shldr_y), font, 0.9, red, 2)
                #cv2.putText(last_image, str(int(torso_inclination)), (l_hip_x + 10, l_hip_y), font, 0.9, red, 2)

                # Join landmarks.
                cv2.line(last_image, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), red, 4)
                cv2.line(last_image, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 100), red, 4)
                cv2.line(last_image, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), red, 4)
                cv2.line(last_image, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), red, 4)

            # Calculate the time of remaining in a particular posture.
            good_time = (1/4) * good_frames
            bad_time =  (1/4) * bad_frames

            # Pose time.
            if good_time > 0:
                time_string_good = 'Good : ' + str(round(good_time, 1)) + 's'
                cv2.putText(last_image, time_string_good, (10, h - 20), font, 0.9, green, 2)

            else:
                time_string_bad = 'Bad : ' + str(round(bad_time, 1)) + 's'
                cv2.putText(last_image, time_string_bad, (10, h - 20), font, 0.9, red, 2)
                
            time_publisher.publish(round(bad_time))
            # If you stay in bad posture for more than 3 minutes (180s) send an alert.
            if bad_time > 180:
                sendWarning()

            # Display.
            cv2.imshow('MediaPipe Pose', last_image)
            last_image = None
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break

