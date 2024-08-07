import cv2
import os

def extract_frames(video_path, frame_directory):
    vidObj = cv2.VideoCapture(video_path)
    success = 1
    frame_nth = 0

    while success:
        success, image = vidObj.read()
        if success:
            frame_path = os.path.join(frame_directory, f"frame{frame_nth}.jpg")
            cv2.imwrite(frame_path, image)
            frame_nth += 1
