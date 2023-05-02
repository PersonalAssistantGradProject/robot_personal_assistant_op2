#!/usr/bin/env python
import face_recognition
import cv2
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge





def recongize_faces(omar_image, mohammad_image, ahmad_image):

    print("started facial recognition!")
    rospy.init_node('facial_recognition', anonymous=True)
    bridge = CvBridge()
    rate = rospy.Rate(1) # 1Hz
    last_image = None

    def callback(data):
        nonlocal last_image
        last_image = bridge.imgmsg_to_cv2(data, "bgr8")

    rospy.Subscriber('/webcam', Image, callback)

    while not rospy.is_shutdown():
        if last_image is not None:
            last_image_flipped = cv2.flip(last_image,0)
            cv2.imwrite('op2_tmp/unknown.jpg', last_image_flipped)
            unknown_image = face_recognition.load_image_file("op2_tmp/unknown.jpg")
            # Get the face encodings for each face in each image file
            # Since there could be more than one face in each image, it returns a list of encodings.
            # But since I know each image only has one face, I only care about the first encoding in each image, so I grab index 0.
            try:
                omar_face_encoding = face_recognition.face_encodings(omar_image)[0]
                mohammad_face_encoding = face_recognition.face_encodings(mohammad_image)[0]
                ahmad_face_encoding = face_recognition.face_encodings(ahmad_image)[0]
                unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
            except IndexError:
                print("I wasn't able to locate any faces in the camera feed.")
                return [False, False, False]

            known_faces = [
                omar_face_encoding,
                mohammad_face_encoding,
                ahmad_face_encoding
            ]

            # results is an array of True/False telling if the unknown face matched anyone in the known_faces array
            auth_results = face_recognition.compare_faces(known_faces, unknown_face_encoding, tolerance=0.4)
            return auth_results
            
        rate.sleep()