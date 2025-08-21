import numpy as np
import cv2
import mediapipe as mp
from PIL import Image
from io import BytesIO

mp_face_mesh = mp.solutions.face_mesh
LEFT_EYE_LANDMARKS = [33, 160, 158, 133, 153, 144]
RIGHT_EYE_LANDMARKS = [362, 385, 387, 263, 373, 380]

def eye_aspect_ratio(eye):
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])
    return (A + B) / (2.0 * C) if C else 0

def detect_eye_state(image_bytes):
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    image = np.array(image)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    with mp_face_mesh.FaceMesh(static_image_mode=True) as face_mesh:
        results = face_mesh.process(image_rgb)

        if not results.multi_face_landmarks:
            return {"error": "No face detected"}

        face_landmarks = results.multi_face_landmarks[0]
        height, width, temp = image.shape

        def get_eye_coords(landmark_ids):
            return np.array([
                [face_landmarks.landmark[i].x * width, face_landmarks.landmark[i].y * height]
                for i in landmark_ids
            ])

        left_eye_coords = get_eye_coords(LEFT_EYE_LANDMARKS)
        right_eye_coords = get_eye_coords(RIGHT_EYE_LANDMARKS)

        left_eye_ear = eye_aspect_ratio(left_eye_coords)
        right_eye_ear = eye_aspect_ratio(right_eye_coords)

        threshold = 0.244
        left_state = "open" if left_eye_ear > threshold else "closed"
        right_state = "open" if right_eye_ear > threshold else "closed"

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(image, f'Left eye: {left_state}', (30, 30), font, 0.8, (0, 255, 0), 2)
        cv2.putText(image, f'Right eye: {right_state}', (30, 70), font, 0.8, (0, 255, 0), 2)

        output_path = "output.jpg"
        cv2.imwrite(output_path, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))

        return {
            "left_eye_state": left_state,
            "right_eye_state": right_state,
            "left_eye_EAR": round(float(left_eye_ear), 3),
            "right_eye_EAR": round(float(right_eye_ear), 3),
            "output_image": output_path
        }