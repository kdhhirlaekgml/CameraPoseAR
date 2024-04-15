# CameraPoseAR
This Python code uses OpenCV to estimate the pose of a camera using a chessboard pattern in a video

Imports: The code imports the necessary libraries, including NumPy and OpenCV (numpy as np and cv2 as cv).
Input Data: It defines the file path for the input video, camera intrinsic matrix K, distortion coefficients dist_coeff, chessboard pattern size, cell size, and criteria for finding the chessboard corners.
Preparing AR Elements: It sets up a 3D box and 3D points on a chessboard for simple Augmented Reality (AR).
Pose Estimation Loop: The code enters a loop to read frames from the video and estimate the camera pose for each frame.
Finding Chessboard Corners: It detects chessboard corners in the current frame using cv.findChessboardCorners().
Estimating Camera Pose: If chessboard corners are found, it estimates the camera pose using cv.solvePnP().
Drawing AR Elements: It projects the 3D box onto the image using the estimated camera pose and draws it.
Drawing Camera Position Information: It calculates the camera position and displays it on the image.
Displaying the Image: It displays the annotated image with the estimated pose and AR elements.
Key Event Handling: It waits for a key press. Pressing the spacebar pauses the video, and pressing the ESC key exits the program.
Cleanup: It releases the video stream and closes all OpenCV windows.

demo video

![CameraPoseEstimationandARvideo-ezgif com-resize](https://github.com/kdhhirlaekgml/CameraPoseAR/assets/86283216/729d697e-6906-4045-85f8-50325bd5857e)
