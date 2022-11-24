import sys
import os
MODULES_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(1, MODULES_DIR)

from modules.ball_detection import FilterColorEditor
import cv2

cap = cv2.VideoCapture(0)
filter = FilterColorEditor(video_feed=cap)
params = filter.open_editor()
