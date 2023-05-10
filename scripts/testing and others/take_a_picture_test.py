import cv2 as cv


cam = cv.VideoCapture(0)

while True:
    ret_val, img = cam.read()
    
    # Check if the image is valid
    if not ret_val:
        continue  # Skip this iteration if the image was not captured successfully
    if img is None or img.size == 0:
        continue  # Skip this iteration if the image has an invalid size
    
    cv.imshow('my webcam', img)
    
    if cv.waitKey(1) == 27:
        cv.imwrite('picture.png', img)
        cam.release()
        cv.destroyAllWindows()
        break