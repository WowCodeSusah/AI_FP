import cv2
import mediapipe as mp
import numpy as np
from matplotlib import pyplot as plt
import os

# Get original MediaPipe landmarks from an image
def getLandmarksfromImage(image):
    os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
    # Load MediaPipe Pose model
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()

    # Convert image to RGB (MediaPipe accepts RGB images)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Perform pose estimation
    results = pose.process(image_rgb)

    # Draw pose landmarks on the image
    if results.pose_landmarks:

        landmark_dict = {}

        for i, landmark in enumerate(results.pose_landmarks.landmark):
            landmark_name = mp_pose.PoseLandmark(i).name
            x = landmark.x
            y = landmark.y
            z = landmark.z  # Correctly assign the z value
            visibility = landmark.visibility

            # Add to landmark_dict
            landmark_dict[landmark_name] = (x, y, z, visibility)
            
    return landmark_dict


# Function to detect poses and draw them on the image
def detect_and_draw_pose(image, visibility_threshold=0.5):
    os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
    # Load MediaPipe Pose model
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()

    # Convert image to RGB (MediaPipe accepts RGB images)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Perform pose estimation
    results = pose.process(image_rgb)

    # Draw pose landmarks on the image
    if results.pose_landmarks:
        mp_drawing = mp.solutions.drawing_utils
        annotated_image = image.copy()
        
        landmark_dict = {}

        for i, landmark in enumerate(results.pose_landmarks.landmark):
            landmark_name = mp_pose.PoseLandmark(i).name
            x = int(landmark.x * image.shape[1])
            y = int(landmark.y * image.shape[0])
            visibility = landmark.visibility

            # Add to landmark_dict
            landmark_dict[landmark_name] = (x, y, visibility)

            # Draw on image only if visibility is above the threshold
            if visibility > visibility_threshold:
                # Draw point
                cv2.circle(annotated_image, (x, y), 5, (0, 255, 0), -1)

        # Draw connections
        for connection in mp_pose.POSE_CONNECTIONS:
            start_idx = connection[0]
            end_idx = connection[1]
            if results.pose_landmarks.landmark[start_idx].visibility > visibility_threshold and results.pose_landmarks.landmark[end_idx].visibility > visibility_threshold:
                start_point = (int(results.pose_landmarks.landmark[start_idx].x * image.shape[1]), 
                               int(results.pose_landmarks.landmark[start_idx].y * image.shape[0]))
                end_point = (int(results.pose_landmarks.landmark[end_idx].x * image.shape[1]), 
                             int(results.pose_landmarks.landmark[end_idx].y * image.shape[0]))
                cv2.line(annotated_image, start_point, end_point, (0, 255, 0), 2)

        return annotated_image, landmark_dict
    else:
        return image, None

import helper
def run(image_input, frameName , csvFile, output_folder = ''):
    os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
    image_path = 'input/' + image_input
    image = cv2.imread(image_path)
    annotated_image, pose_landmarks_dict = detect_and_draw_pose(image, visibility_threshold=0.6)

    # Original Pose Dictionary
    pose_dict = {"folderName": str(image_input.replace('/'+ frameName, '')), "fileName": str(frameName.replace('.jpg', ''))}

    if pose_landmarks_dict:
        for name, (x, y, visibility) in pose_landmarks_dict.items():
            print(f'{name}: ({x}, {y}), visibility: {visibility:.2f}')
            pose_dict[str(name) + '_x'] = x
            pose_dict[str(name) + '_y'] = y
            pose_dict[str(name) + '_v'] = visibility

    # add if varible for shot connection based on file name
    if 'out' in str(image_input.replace('/'+ frameName, '')):
        pose_dict["shot"] = False
    elif 'in' in str(image_input.replace('/'+ frameName, '')):
        pose_dict["shot"] = True
    else:
        pose_dict["shot"] = False

    plt.figure(figsize=(8, 6))
    plt.imshow(cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    # plt.show()

    output_path = output_folder + '/' + str(frameName.replace('.jpg', '')) + '_annotated_image.jpg'
    cv2.imwrite(output_path, annotated_image)

    getLandmarksfromImage(image)
    plt.close()

    return pose_dict