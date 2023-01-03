import os

import cv2
import numpy as np
from cv2 import aruco


class ArucoDetector:
    def __init__(self, aruco_size_cm=4.75):
        self._aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
        self._parameters = aruco.DetectorParameters_create()
        self._a = aruco_size_cm
        self._aruco_marker_points = np.array([[-self._a / 2, self._a / 2, 0],
                                              [self._a / 2, self._a / 2, 0],
                                              [self._a / 2, -self._a / 2, 0],
                                              [-self._a / 2, -self._a / 2, 0]])

        try:
            self._mtx = np.load(os.path.dirname(__file__) + "/mtx.npy")
        except FileNotFoundError:
            print("mtx.npy not found in ", os.path.dirname(__file__))
            exit(1)
        try:
            self._dist = np.load(os.path.dirname(__file__) + "/dist.npy")
        except FileNotFoundError:
            print("dist.npy not found in ", os.path.dirname(__file__))
            exit(1)

        self._ids = None
        self._corners = None

    def detection(self, gray_image):
        # Trying to detect an aruco marker
        corners, ids, rejectedImgPoints = aruco.detectMarkers(
            gray_image, self._aruco_dict, parameters=self._parameters)

        success = True if ids else False

        # Updating _ids and _corners attributes
        if success:
            self._ids = ids[0]
            self._corners = corners[0]
        else:
            self._ids = None
            self._corners = None

        return success, corners, ids

    def get_deviation(self):
        _, rot, trans = cv2.solvePnP(objectPoints=self._aruco_marker_points,
                                     imagePoints=self._corners,  # We take the first detected aruco
                                     cameraMatrix=self._mtx,
                                     distCoeffs=self._dist)
        
        rot_matrix, _ = cv2.Rodrigues(rot)
        heading_error = np.degrees(np.arctan2(rot_matrix[1, 0], rot_matrix[0, 0])) - 90
        distance_error = trans[2, 0] - 20

        return heading_error, distance_error


def find_euler(rot_matrix):
    # Computing roll angle from rotation matrix
    roll = np.degrees(np.arctan2(rot_matrix[2, 1], rot_matrix[2, 2]))
    # Computing pitch angle from rotation matrix
    pitch = np.degrees(
        np.arctan2(-rot_matrix[2, 0], np.sqrt(rot_matrix[2, 1] ** 2 + rot_matrix[2, 2] ** 2)))
    # Computing yaw angle from rotation matrix
    yaw = np.degrees(np.arctan2(rot_matrix[1, 0], rot_matrix[0, 0]))
    return roll, pitch, yaw


def move_into_new_frame(rvec, tvec):
    # Computing rotation matrix from camera to Aruco marker
    rot_cam_at, _ = cv2.Rodrigues(rvec)
    # Computing rotation matrix from Aruco marker to camera
    rot_at_cam = rot_cam_at.T
    # Computing translation from Aruco marker to camera
    trans_at_cam = - rot_at_cam @ tvec
    return rot_at_cam, trans_at_cam


def get_real_world_pose(rot, trans):
    # Retrieving Euler angles from rotation matrix
    roll, pitch, yaw = find_euler(rot)
    # Retrieving camera position
    position = trans + np.array([500, 200, 300]).reshape(3, 1)
    # Retrieving camera orientation
    euler_angle = np.array([roll, pitch, yaw])
    return position, euler_angle


def print_position(position):
    x = round(position[0, 0])
    y = round(position[1, 0])
    z = round(position[2, 0])
    print(f"\nx : {x}\ty : {y}\tz : {z}")
    return x, y, z


def print_euler(rvec):
    rot, _ = cv2.Rodrigues(rvec)
    roll, pitch, yaw = find_euler(rot)
    roll = round(roll)
    pitch = round(pitch)
    yaw = round(yaw)
    print(f"Roll : {roll}\tPitch : {pitch}\tYaw : {yaw}\n")
    return roll, pitch, yaw
