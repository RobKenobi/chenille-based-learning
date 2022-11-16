from modules.ball_detection import FilterColorEditor
import cv2

cap = cv2.VideoCapture(0)
filter = FilterColorEditor(video_feed=cap)
params = filter.open_editor()
