# Facial Landmarks Recognition with Dlib and OpenCV

## Import the necessary packages
from imutils import face_utils
import dlib
import cv2
import os

# Download the shape_predictor_68_face_landmarks.dat file
import urllib.request

url = "https://github.com/italojs/facial-landmarks-recognition/raw/master/shape_predictor_68_face_landmarks.dat"
model_path = "shape_predictor_68_face_landmarks.dat"

if not os.path.exists(model_path):
    print(f"Downloading {model_path}...")
    urllib.request.urlretrieve(url, model_path)
    print("Download complete.")

# Initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
p = "shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(p)

# Start the video capture
cap = cv2.VideoCapture(0)

while True:
    # Load the input image and convert it to grayscale
    _, image = cap.read()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale image
    rects = detector(gray, 0)

    # Loop over the face detections
    for i, rect in enumerate(rects):
        # Determine the facial landmarks for the face region, then
        # convert the facial landmark (x, y)-coordinates to a NumPy
        # array
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        # Loop over the (x, y)-coordinates for the facial landmarks
        # and draw them on the image
        for x, y in shape:
            cv2.circle(image, (x, y), 2, (0, 255, 0), -1)

    # Show the output image with the face detections + facial landmarks
    cv2.imshow("Output", image)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

# Cleanup
cv2.destroyAllWindows()
cap.release()
