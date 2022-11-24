import sys
import os
MODULES_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(1, MODULES_DIR)

from modules.ball_detection import CircleDetectorEditor

circle_detector = CircleDetectorEditor()
params = circle_detector.open_editor()