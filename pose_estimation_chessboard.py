import numpy as np
import cv2 as cv

# The given video and calibration data
video_file = r'C:\Users\kdhhi\Desktop\서울과학기술대학교\강의자료\2024 1학기\컴퓨터비전\camera_calibration_sample.mp4'
K = np.array([[541.02582236, 0, 555.08599052],
              [0, 553.3418283, 658.93093562],
              [0, 0, 1]])
dist_coeff = np.array([-0.00743852,  0.04353781,  0.00181177,  0.00076285, -0.03912152])
board_pattern = (6,4)
board_cellsize = 0.025
board_criteria = cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_NORMALIZE_IMAGE + cv.CALIB_CB_FAST_CHECK

# Open a video
video = cv.VideoCapture(video_file)
assert video.isOpened(), 'Cannot read the given input, ' + video_file

# Prepare a 3D box for simple AR
#box_lower = board_cellsize * np.array([[4, 2,  0], [5, 2,  0], [5, 4,  0], [4, 4,  0]])
#box_upper = board_cellsize * np.array([[4, 2, -1], [5, 2, -1], [5, 4, -1], [4, 4, -1]])

triangle_vertices = board_cellsize * np.array([[4.5, 2.5, 0], [5, 4, 0], [4, 4, 0]])
triangle_lines = np.array([[triangle_vertices[0], triangle_vertices[1]],
                           [triangle_vertices[1], triangle_vertices[2]],
                           [triangle_vertices[2], triangle_vertices[0]]], dtype=np.float32)

# Prepare 3D points on a chessboard
obj_points = board_cellsize * np.array([[c, r, 0] for r in range(board_pattern[1]) for c in range(board_pattern[0])])

# Run pose estimation
while True:
    # Read an image from the video
    valid, img = video.read()
    if not valid:
        break

    # Estimate the camera pose
    success, img_points = cv.findChessboardCorners(img, board_pattern, board_criteria)
    if success:
        ret, rvec, tvec = cv.solvePnP(obj_points, img_points, K, dist_coeff)

        # Draw the box on the image
        '''line_lower, _ = cv.projectPoints(box_lower, rvec, tvec, K, dist_coeff)
        line_upper, _ = cv.projectPoints(box_upper, rvec, tvec, K, dist_coeff)
        cv.polylines(img, [np.int32(line_lower)], True, (255, 0, 0), 2)
        cv.polylines(img, [np.int32(line_upper)], True, (0, 0, 255), 2)
        for b, t in zip(line_lower, line_upper):
            cv.line(img, np.int32(b.flatten()), np.int32(t.flatten()), (0, 255, 0), 2)'''
        for line in triangle_lines:
          line_projected, _ = cv.projectPoints(line, rvec, tvec, K, dist_coeff)
          cv.polylines(img, [np.int32(line_projected)], False, (0, 255, 0), 2)

        # Print the camera position
        R, _ = cv.Rodrigues(rvec) # Alternative) `scipy.spatial.transform.Rotation`
        p = (-R.T @ tvec).flatten()
        info = f'XYZ: [{p[0]:.3f} {p[1]:.3f} {p[2]:.3f}]'
        cv.putText(img, info, (10, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0))

    # Show the image and process the key event
    cv.imshow('Pose Estimation (Chessboard)', img)
    key = cv.waitKey(10)
    if key == ord(' '):
        key = cv.waitKey()
    if key == 27: # ESC
        break

video.release()
cv.destroyAllWindows()