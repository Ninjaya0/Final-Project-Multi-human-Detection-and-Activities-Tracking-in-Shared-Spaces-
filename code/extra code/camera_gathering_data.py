#!/usr/bin/env python
# coding: utf-8

# In[40]:


import sys
print(sys.executable)


# In[41]:


import mediapipe as mp
print("OK")


# In[42]:


import cv2
import mediapipe as mp
import numpy as np
import os


STROKE = "backhand"  

SAVE_PATH = f"data/{STROKE}_v1_multijoint"
os.makedirs(SAVE_PATH, exist_ok=True)


mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils


cap = cv2.VideoCapture(0)

recording = False
frames = []
counter = len(os.listdir(SAVE_PATH)) + 1

print("Press R to start/stop recording")

# 11 joints 
joint_ids = [
    12, 11,  # shoulders
    14, 13,  # elbows
    16, 15,  # wrists
    24, 23,  # hips
    26, 25,  # knees
    0        # nose
]

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = pose.process(rgb)

    if result.pose_landmarks:
        mp_draw.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        if recording:
            landmarks = result.pose_landmarks.landmark

            joints = []
            for j in joint_ids:
                joints.append([landmarks[j].x, landmarks[j].y])

            frames.append(joints)

    cv2.putText(frame, f"{STROKE}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.imshow("Recorder", frame)

    key = cv2.waitKey(1)

    if key == ord('r'):
        recording = not recording

        if recording:
            print("RECORD START")
            frames = []
        else:
            print("RECORD END")

            if len(frames) > 20:
                data = np.array(frames)
                name = f"{STROKE}_{counter:03d}.npy"
                np.save(os.path.join(SAVE_PATH, name), data)
                print("[SAVED]", name)
                counter += 1

    elif key == 27:
        break

cap.release()
cv2.destroyAllWindows()


# In[8]:


import cv2
import mediapipe as mp
import numpy as np
import os


VIDEO_PATHS = [
    r"C:\Users\DellG5\Desktop\B1.mp4",
    r"C:\Users\DellG5\Desktop\B2.mp4",
    r"C:\Users\DellG5\Desktop\B3.mp4"
]

SAVE_DIR = "data/backhand_v1_multijoint"
os.makedirs(SAVE_DIR, exist_ok=True)


mp_pose = mp.solutions.pose
pose = mp_pose.Pose()


JOINTS = [
    mp_pose.PoseLandmark.RIGHT_WRIST,
    mp_pose.PoseLandmark.RIGHT_ELBOW,
    mp_pose.PoseLandmark.RIGHT_SHOULDER,
    mp_pose.PoseLandmark.LEFT_WRIST,
    mp_pose.PoseLandmark.LEFT_ELBOW,
    mp_pose.PoseLandmark.LEFT_SHOULDER,
    mp_pose.PoseLandmark.RIGHT_HIP,
    mp_pose.PoseLandmark.LEFT_HIP,
    mp_pose.PoseLandmark.RIGHT_KNEE,
    mp_pose.PoseLandmark.LEFT_KNEE,
    mp_pose.PoseLandmark.NOSE  
]


recording = False
stroke = []
file_index = 1


existing = [f for f in os.listdir(SAVE_DIR) if f.endswith(".npy")]
if existing:
    file_index = len(existing) + 1


for video_path in VIDEO_PATHS:

    cap = cv2.VideoCapture(video_path)
    print(f"Processing: {video_path}")
    print("Press R to start/stop recording")

    
    cv2.namedWindow("Backhand Video", cv2.WINDOW_NORMAL)

    while cap.isOpened():

        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)

        if results.pose_landmarks:

            landmarks = results.pose_landmarks.landmark

            frame_data = []
            for j in JOINTS:
                lm = landmarks[j]
                frame_data.append([lm.x, lm.y])

            frame_data = np.array(frame_data)

           
            if recording:
                stroke.append(frame_data)

           
            mp.solutions.drawing_utils.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS
            )

       
        display = cv2.resize(frame, (960, 540))
        cv2.imshow("Backhand Video", display)

        key = cv2.waitKey(10) & 0xFF

        if key == ord('r'):
            recording = not recording

            if recording:
                print("RECORD START")
                stroke = []

            else:
                print("RECORD END")

                if len(stroke) > 10:  
                    file_name = f"backhand_{file_index:03d}.npy"
                    save_path = os.path.join(SAVE_DIR, file_name)

                    np.save(save_path, np.array(stroke))
                    print(f"[SAVED] {file_name}")

                    file_index += 1
                else:
                    print("Too short, ignored")

        if key == 27:
            break

    cap.release()

cv2.destroyAllWindows()
print("Done ")


# In[10]:


import cv2
import mediapipe as mp
import numpy as np
import os


VIDEO_PATHS = [
    r"C:\Users\DellG5\Desktop\S1.mp4",
    r"C:\Users\DellG5\Desktop\S2.mp4"
]

SAVE_DIR = "data/serve_v1_multijoint"
os.makedirs(SAVE_DIR, exist_ok=True)


mp_pose = mp.solutions.pose
pose = mp_pose.Pose()


JOINTS = [
    mp_pose.PoseLandmark.RIGHT_WRIST,
    mp_pose.PoseLandmark.RIGHT_ELBOW,
    mp_pose.PoseLandmark.RIGHT_SHOULDER,
    mp_pose.PoseLandmark.LEFT_WRIST,
    mp_pose.PoseLandmark.LEFT_ELBOW,
    mp_pose.PoseLandmark.LEFT_SHOULDER,
    mp_pose.PoseLandmark.RIGHT_HIP,
    mp_pose.PoseLandmark.LEFT_HIP,
    mp_pose.PoseLandmark.RIGHT_KNEE,
    mp_pose.PoseLandmark.LEFT_KNEE,
    mp_pose.PoseLandmark.NOSE  
]


recording = False
stroke = []
file_index = 1


existing = [f for f in os.listdir(SAVE_DIR) if f.endswith(".npy")]
if existing:
    file_index = len(existing) + 1


for video_path in VIDEO_PATHS:

    cap = cv2.VideoCapture(video_path)
    print(f"Processing: {video_path}")
    print("Press R to start/stop recording")

  
    cv2.namedWindow("Serve Video", cv2.WINDOW_NORMAL)

    while cap.isOpened():

        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)

        if results.pose_landmarks:

            landmarks = results.pose_landmarks.landmark

            frame_data = []
            for j in JOINTS:
                lm = landmarks[j]
                frame_data.append([lm.x, lm.y])

            frame_data = np.array(frame_data)

            
            if recording:
                stroke.append(frame_data)

            mp.solutions.drawing_utils.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS
            )

      
        display = cv2.resize(frame, (960, 540))
        cv2.imshow("Serve Video", display)

        key = cv2.waitKey(10) & 0xFF

        if key == ord('r'):
            recording = not recording

            if recording:
                print("RECORD START")
                stroke = []

            else:
                print("RECORD END")

                if len(stroke) > 10:
                    file_name = f"serve_{file_index:03d}.npy"
                    save_path = os.path.join(SAVE_DIR, file_name)

                    np.save(save_path, np.array(stroke))
                    print(f"[SAVED] {file_name}")

                    file_index += 1
                else:
                    print("Too short, ignored it")

        if key == 27:
            break

    cap.release()

cv2.destroyAllWindows()
print("Serve recording done ")


# In[19]:


import numpy as np
import os


data_paths = {
    "backhand": r"C:\Users\DellG5\Desktop\TENNIS DATA\backhand_v1_multijoint",
    "serve": r"C:\Users\DellG5\Desktop\TENNIS DATA\serve_v1_multtijoint"
}


output_paths = {
    "backhand": r"C:\Users\DellG5\Desktop\TENNIS DATA\backhand_v2_centered",
    "serve": r"C:\Users\DellG5\Desktop\TENNIS DATA\serve_v2_centered"
}

for key in data_paths:
    os.makedirs(output_paths[key], exist_ok=True)

    for file in os.listdir(data_paths[key]):
        if file.endswith(".npy"):
            data = np.load(os.path.join(data_paths[key], file))

          
            mid_hip = (data[:, 8, :] + data[:, 9, :]) / 2

            # Center body
            centered = data - mid_hip[:, None, :]

            np.save(os.path.join(output_paths[key], file), centered)

print("Centering DONE ")


# In[38]:


import numpy as np
import os
import matplotlib.pyplot as plt


FOREHAND = r"C:\Users\DellG5\Desktop\TENNIS DATA\forehand_v2_resampled"
BACKHAND = r"C:\Users\DellG5\Desktop\TENNIS DATA\backhand_v2_centered"
SERVE = r"C:\Users\DellG5\Desktop\TENNIS DATA\serve_v2_centered"



RIGHT_WRIST = 4
LEFT_WRIST = 7


# In[32]:


import numpy as np
import os
import matplotlib.pyplot as plt

FOREHAND = r"C:\Users\DellG5\Desktop\TENNIS DATA\forehand_v2_resampled"
BACKHAND = r"C:\Users\DellG5\Desktop\TENNIS DATA\backhand_v2_centered"
SERVE = r"C:\Users\DellG5\Desktop\TENNIS DATA\serve_v2_centered"


RIGHT_WRIST = 4
LEFT_WRIST = 7


# In[33]:


plt.figure(figsize=(6,6))

for f in os.listdir(FOREHAND):
    traj = np.load(os.path.join(FOREHAND, f))
    wrist = traj[:, RIGHT_WRIST, :]
    plt.plot(wrist[:,0], wrist[:,1], color="green", alpha=0.5)

plt.gca().invert_yaxis()
plt.title("Forehand Wrist Trajectories (Right Wrist)")
plt.xlabel("X")
plt.ylabel("Y")
plt.show()


# In[34]:


plt.figure(figsize=(6,6))

for f in os.listdir(BACKHAND):
    traj = np.load(os.path.join(BACKHAND, f))
    wrist = traj[:, LEFT_WRIST, :]
    plt.plot(wrist[:,0], wrist[:,1], color="blue", alpha=0.5)

plt.gca().invert_yaxis()
plt.title("Backhand Wrist Trajectories (Left Wrist)")
plt.xlabel("X")
plt.ylabel("Y")
plt.show()


# In[35]:


plt.figure(figsize=(6,6))

for f in os.listdir(SERVE):
    traj = np.load(os.path.join(SERVE, f))
    wrist = traj[:, RIGHT_WRIST, :]
    plt.plot(wrist[:,0], wrist[:,1], color="red", alpha=0.5)

plt.gca().invert_yaxis()
plt.title("Serve Wrist Trajectories (Right Wrist)")
plt.xlabel("X")
plt.ylabel("Y")
plt.show()


# In[36]:


plt.figure(figsize=(7,7))

# Forehand
for f in os.listdir(FOREHAND):
    traj = np.load(os.path.join(FOREHAND, f))
    wrist = traj[:, RIGHT_WRIST, :]
    plt.plot(wrist[:,0], wrist[:,1], color="green", alpha=0.3, label="Forehand")

# Backhand
for f in os.listdir(BACKHAND):
    traj = np.load(os.path.join(BACKHAND, f))
    wrist = traj[:, LEFT_WRIST, :]
    plt.plot(wrist[:,0], wrist[:,1], color="blue", alpha=0.3, label="Backhand")

plt.gca().invert_yaxis()
plt.title("Forehand vs Backhand Wrist Comparison")
plt.xlabel("X")
plt.ylabel("Y")


handles = [
    plt.Line2D([0], [0], color='green', label='Forehand'),
    plt.Line2D([0], [0], color='blue', label='Backhand')
]
plt.legend(handles=handles)

plt.show()


# In[37]:


plt.figure(figsize=(8,8))

# Forehand
for f in os.listdir(FOREHAND):
    traj = np.load(os.path.join(FOREHAND, f))
    wrist = traj[:, RIGHT_WRIST, :]
    plt.plot(wrist[:,0], wrist[:,1], color="green", alpha=0.25)

# Backhand
for f in os.listdir(BACKHAND):
    traj = np.load(os.path.join(BACKHAND, f))
    wrist = traj[:, LEFT_WRIST, :]
    plt.plot(wrist[:,0], wrist[:,1], color="blue", alpha=0.25)

# Serve
for f in os.listdir(SERVE):
    traj = np.load(os.path.join(SERVE, f))
    wrist = traj[:, RIGHT_WRIST, :]
    plt.plot(wrist[:,0], wrist[:,1], color="red", alpha=0.25)

plt.gca().invert_yaxis()
plt.title("Wrist Movement Comparison: Forehand vs Backhand vs Serve")
plt.xlabel("X")
plt.ylabel("Y")

handles = [
    plt.Line2D([0], [0], color='green', label='Forehand'),
    plt.Line2D([0], [0], color='blue', label='Backhand'),
    plt.Line2D([0], [0], color='red', label='Serve')
]
plt.legend(handles=handles)

plt.show()


# In[43]:


import cv2
import mediapipe as mp
import numpy as np
import os
from scipy.signal import resample
from collections import deque



MODE = "auto"   
VIDEO_PATHS = [
    r"C:\Users\DellG5\Desktop\GA1.mp4",
    r"C:\Users\DellG5\Desktop\GA2.mp4"
]

FH_DIR = r"C:\Users\DellG5\Desktop\TENNIS DATA\forehand_v2_resampled"
BH_DIR = r"C:\Users\DellG5\Desktop\TENNIS DATA\backhand_v3_resampled"
SV_DIR = r"C:\Users\DellG5\Desktop\TENNIS DATA\serve_v3_resampled"

for d in [FH_DIR, BH_DIR, SV_DIR]:
    os.makedirs(d, exist_ok=True)

# HSV BALL RANGE
LOWER_YELLOW = np.array([20, 80, 80])
UPPER_YELLOW = np.array([45, 255, 255])



mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

JOINTS = [
    16, 14, 12,   
    15, 13, 11,   
    24, 23,       
    26, 25,      
    0             
]



def get_next_index(folder, prefix):
    files = [f for f in os.listdir(folder) if f.endswith(".npy")]
    if not files:
        return 1
    nums = [int(f.split("_")[1].split(".")[0]) for f in files]
    return max(nums) + 1

def extract_skeleton(frame, last_valid):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb)

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        data = []
        for idx in JOINTS:
            lm = landmarks[idx]
            data.append([lm.x, lm.y])
        return np.array(data)
    else:
        return last_valid

def resample_clip(clip):
    clip = np.array(clip)
    return resample(clip, 30, axis=0)

def normalize_frame(frame):
    h, w = frame.shape[:2]
    if h > w:
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        h, w = frame.shape[:2]
    print(f"Video: {w}x{h} → normalized to 1280x720")
    return cv2.resize(frame, (1280, 720))

def detect_ball(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, LOWER_YELLOW, UPPER_YELLOW)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        c = max(contours, key=cv2.contourArea)
        if cv2.contourArea(c) > 30:
            (x, y), radius = cv2.minEnclosingCircle(c)
            return int(x), int(y)
    return None



fh_index = get_next_index(FH_DIR, "forehand")
bh_index = get_next_index(BH_DIR, "backhand")
sv_index = get_next_index(SV_DIR, "serve")

session_counts = {"FH":0, "BH":0, "SV":0}



if MODE == "auto":

    print("MODE: AUTO (Forehand/Backhand)")
    for video_path in VIDEO_PATHS:

        cap = cv2.VideoCapture(video_path)
        ret, first = cap.read()
        first = normalize_frame(first)
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        buffer_frames = deque(maxlen=60)
        buffer_skeletons = deque(maxlen=60)

        last_ball_pos = None
        ball_visible_count = 0
        ball_missing_count = 0
        last_valid_skeleton = None

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = normalize_frame(frame)
            skeleton = extract_skeleton(frame, last_valid_skeleton)
            if skeleton is not None:
                last_valid_skeleton = skeleton

            ball = detect_ball(frame)

            if ball:
                ball_visible_count += 1
                ball_missing_count = 0
                if last_ball_pos:
                    velocity = abs(ball[0] - last_ball_pos[0])
                else:
                    velocity = 0
                last_ball_pos = ball
            else:
                ball_missing_count += 1
                velocity = 0

           
            trigger = False
            width = frame.shape[1]

            if ball_visible_count >= 3 and ball_missing_count >= 5:
                trigger = True

            if velocity > 0.15 * width:
                trigger = True

            if ball and last_valid_skeleton is not None:
                torso_center = np.mean(last_valid_skeleton[2:6,0]) * width
                if abs(ball[0] - torso_center) < 10:
                    trigger = True

            buffer_frames.append(frame.copy())
            buffer_skeletons.append(skeleton)

           
            cv2.putText(frame, "MODE: AUTO", (20,40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

            cv2.putText(frame,
                        f"FH:{session_counts['FH']}  BH:{session_counts['BH']}  SV:{session_counts['SV']}",
                        (20,80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255),2)

            if ball:
                cv2.circle(frame, ball, 6, (0,255,255), -1)

            cv2.imshow("Tennis Collector", frame)

            if trigger and len(buffer_skeletons) == 60:
                print(" Stroke candidate detected. Press F/B/S")

                preview = list(buffer_frames)
                clip = list(buffer_skeletons)

                paused = True
                while paused:
                    for f in preview:
                        cv2.imshow("Preview", f)
                        if cv2.waitKey(20) & 0xFF != 255:
                            break

                    key = cv2.waitKey(0) & 0xFF

                    if key == ord('f'):
                        save_clip = resample_clip(clip)
                        filename = f"forehand_{fh_index:03d}.npy"
                        np.save(os.path.join(FH_DIR, filename), save_clip)
                        print(f"[SAVED] {filename}")
                        fh_index += 1
                        session_counts["FH"] += 1
                        paused = False

                    elif key == ord('b'):
                        save_clip = resample_clip(clip)
                        filename = f"backhand_{bh_index:03d}.npy"
                        np.save(os.path.join(BH_DIR, filename), save_clip)
                        print(f"[SAVED] {filename}")
                        bh_index += 1
                        session_counts["BH"] += 1
                        paused = False

                    elif key == ord('s'):
                        print("Skipped")
                        paused = False

                cv2.destroyWindow("Preview")

            if cv2.waitKey(1) & 0xFF == 27:
                break

        cap.release()



if MODE == "manual":

    print("MODE: MANUAL (Serve)")

    source = input("Type 'video' or 'webcam': ").lower()
    if source == "video":
        cap = cv2.VideoCapture(VIDEO_PATHS[0])
    else:
        cap = cv2.VideoCapture(0)

    recording = False
    clip = []
    last_valid_skeleton = None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = normalize_frame(frame)
        skeleton = extract_skeleton(frame, last_valid_skeleton)
        if skeleton is not None:
            last_valid_skeleton = skeleton

        if recording:
            clip.append(skeleton)
            cv2.circle(frame, (30,30), 10, (0,0,255), -1)

        cv2.putText(frame, "MODE: MANUAL (Serve)", (20,40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0),2)

        cv2.imshow("Tennis Collector", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('r'):
            recording = not recording
            if recording:
                print("Recording started")
                clip = []
            else:
                print("Recording stopped")
                if len(clip) > 15:
                    save_clip = resample_clip(clip)
                    filename = f"serve_{sv_index:03d}.npy"
                    np.save(os.path.join(SV_DIR, filename), save_clip)
                    print(f"[SAVED] {filename}")
                    sv_index += 1
                    session_counts["SV"] += 1
                else:
                    print("Too short, ignored")

        if key == 27:
            break

    cap.release()

cv2.destroyAllWindows()
print("Done ")


# In[2]:


import cv2
import mediapipe as mp
import numpy as np
import os
import time


VIDEO_PATHS = [
    r"C:\Users\DellG5\Desktop\GA1.mp4",
    r"C:\Users\DellG5\Desktop\GA2.mp4"
]

SAVE_DIR = r"C:\Users\DellG5\Desktop\TENNIS DATA\forehand_v2_resampled"
os.makedirs(SAVE_DIR, exist_ok=True)


SLOW_FACTOR = 0.8  


mp_pose = mp.solutions.pose
pose = mp_pose.Pose()


JOINTS = [
    mp_pose.PoseLandmark.RIGHT_WRIST,
    mp_pose.PoseLandmark.RIGHT_ELBOW,
    mp_pose.PoseLandmark.RIGHT_SHOULDER,
    mp_pose.PoseLandmark.LEFT_WRIST,
    mp_pose.PoseLandmark.LEFT_ELBOW,
    mp_pose.PoseLandmark.LEFT_SHOULDER,
    mp_pose.PoseLandmark.RIGHT_HIP,
    mp_pose.PoseLandmark.LEFT_HIP,
    mp_pose.PoseLandmark.RIGHT_KNEE,
    mp_pose.PoseLandmark.LEFT_KNEE,
    mp_pose.PoseLandmark.NOSE
]


recording = False
stroke = []

# auto index
existing = [f for f in os.listdir(SAVE_DIR) if f.endswith(".npy")]
file_index = len(existing) + 1

print(f"Existing clips: {len(existing)}")
print("Press R to start/stop recording")
print("ESC to quit")


for video_path in VIDEO_PATHS:

    cap = cv2.VideoCapture(video_path)
    print(f"\nProcessing: {video_path}")

    cv2.namedWindow("Forehand Collector", cv2.WINDOW_NORMAL)

    while cap.isOpened():

        ret, frame = cap.read()
        if not ret:
            break

        # slow motion
        time.sleep((1 - SLOW_FACTOR) * 0.03)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)

        if results.pose_landmarks:

            landmarks = results.pose_landmarks.landmark

            frame_data = []
            for j in JOINTS:
                lm = landmarks[j]
                frame_data.append([lm.x, lm.y])

            frame_data = np.array(frame_data)

            if recording:
                stroke.append(frame_data)

            mp.solutions.drawing_utils.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS
            )

        
    
        status = "RECORDING" if recording else "READY"
        color = (0, 0, 255) if recording else (0, 255, 0)

        cv2.putText(frame, f"FOREHAND MODE",
                    (20, 40), cv2.FONT_HERSHEY_SIMPLEX,
                    1.2, (255, 255, 255), 3)

        cv2.putText(frame, status,
                    (20, 80), cv2.FONT_HERSHEY_SIMPLEX,
                    1.0, color, 2)

       
        if recording:
            cv2.circle(frame, (600, 40), 12, (0, 0, 255), -1)

       
        display = cv2.resize(frame, (960, 540))
        cv2.imshow("Forehand Collector", display)

        key = cv2.waitKey(10) & 0xFF

        
        if key == ord('r'):
            recording = not recording

            if recording:
                print("\n[RECORD START]")
                stroke = []

            else:
                print("[RECORD END]")

                if len(stroke) > 15:
                    file_name = f"forehand_{file_index:03d}.npy"
                    save_path = os.path.join(SAVE_DIR, file_name)

                    np.save(save_path, np.array(stroke))
                    print(f"[SAVED] {file_name} | frames: {len(stroke)}")

                    file_index += 1
                else:
                    print("Too short → ignored")

        if key == 27:
            break

    cap.release()

cv2.destroyAllWindows()
print("Done ")


# In[3]:


import cv2
import mediapipe as mp
import numpy as np
import os
import time


VIDEO_PATH = r"C:\Users\DellG5\Desktop\GA2.mp4"

SAVE_F = r"C:\Users\DellG5\Desktop\TENNIS DATA\extra\F"
SAVE_B = r"C:\Users\DellG5\Desktop\TENNIS DATA\extra\B"

os.makedirs(SAVE_F, exist_ok=True)
os.makedirs(SAVE_B, exist_ok=True)

SLOW_FACTOR = 0.8


def next_index(folder):
    files = [f for f in os.listdir(folder) if f.endswith(".npy")]
    return len(files) + 1

idx_F = next_index(SAVE_F)
idx_B = next_index(SAVE_B)

print("Forehand existing:", idx_F - 1)
print("Backhand existing:", idx_B - 1)


mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

JOINTS = [
    mp_pose.PoseLandmark.RIGHT_WRIST,
    mp_pose.PoseLandmark.RIGHT_ELBOW,
    mp_pose.PoseLandmark.RIGHT_SHOULDER,
    mp_pose.PoseLandmark.LEFT_WRIST,
    mp_pose.PoseLandmark.LEFT_ELBOW,
    mp_pose.PoseLandmark.LEFT_SHOULDER,
    mp_pose.PoseLandmark.RIGHT_HIP,
    mp_pose.PoseLandmark.LEFT_HIP,
    mp_pose.PoseLandmark.RIGHT_KNEE,
    mp_pose.PoseLandmark.LEFT_KNEE,
    mp_pose.PoseLandmark.NOSE
]

recording = False
stroke = []
current_class = None

print("\nControls:")
print("1 = Forehand START/STOP")
print("2 = Backhand START/STOP")
print("ESC = quit")


cap = cv2.VideoCapture(VIDEO_PATH)
cv2.namedWindow("Stroke Collector", cv2.WINDOW_NORMAL)

while cap.isOpened():

    ret, frame = cap.read()
    if not ret:
        break

    # slow motion
    time.sleep((1 - SLOW_FACTOR) * 0.03)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb)

    if results.pose_landmarks:

        landmarks = results.pose_landmarks.landmark

        frame_data = []
        for j in JOINTS:
            lm = landmarks[j]
            frame_data.append([lm.x, lm.y])

        frame_data = np.array(frame_data)

        if recording:
            stroke.append(frame_data)

        mp.solutions.drawing_utils.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )


    status = "RECORDING" if recording else "READY"
    color = (0, 0, 255) if recording else (255, 255, 255)

    cv2.putText(frame, status,
                (20, 40), cv2.FONT_HERSHEY_SIMPLEX,
                1.2, color, 3)

    if recording:
        cv2.circle(frame, (600, 40), 12, (0, 0, 255), -1)

    display = cv2.resize(frame, (960, 540))
    cv2.imshow("Stroke Collector", display)

    key = cv2.waitKey(10) & 0xFF

    
    if key == ord('1'):

        if not recording:
            recording = True
            current_class = "F"
            stroke = []
            print("\n[START] Forehand")

        else:
            recording = False
            print("[END] Forehand")

            if len(stroke) > 15:
                fname = f"forehand_{idx_F:03d}.npy"
                path = os.path.join(SAVE_F, fname)
                np.save(path, np.array(stroke))
                print(f"[SAVED] {fname} | frames: {len(stroke)}")
                idx_F += 1
            else:
                print("Too short → ignored")

  
    if key == ord('2'):

        if not recording:
            recording = True
            current_class = "B"
            stroke = []
            print("\n[START] Backhand")

        else:
            recording = False
            print("[END] Backhand")

            if len(stroke) > 15:
                fname = f"backhand_{idx_B:03d}.npy"
                path = os.path.join(SAVE_B, fname)
                np.save(path, np.array(stroke))
                print(f"[SAVED] {fname} | frames: {len(stroke)}")
                idx_B += 1
            else:
                print("Too short → ignored")

    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
print("Done ")


# In[4]:


import cv2
import mediapipe as mp
import numpy as np
import os


VIDEO_PATH = r"C:\Users\DellG5\Desktop\GA.mp4"

SAVE_F = r"C:\Users\DellG5\Desktop\TENNIS DATA\extra\F"
SAVE_B = r"C:\Users\DellG5\Desktop\TENNIS DATA\extra\B"

os.makedirs(SAVE_F, exist_ok=True)
os.makedirs(SAVE_B, exist_ok=True)


mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils
pose = mp_pose.Pose()

cap = cv2.VideoCapture(VIDEO_PATH)


recording = False
current_label = None
sequence = []

# Count existing
f_count = len(os.listdir(SAVE_F))
b_count = len(os.listdir(SAVE_B))

print("Press 1 = Forehand")
print("Press 2 = Backhand")
print("ESC to quit")


while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

    
    cv2.waitKey(30)

   
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb)

    
    if results.pose_landmarks:
        mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

  
    if recording and results.pose_landmarks:
        landmarks = []
        for lm in results.pose_landmarks.landmark:
            landmarks.extend([lm.x, lm.y, lm.z, lm.visibility])
        sequence.append(landmarks)


    cv2.imshow("Stroke Recorder", frame)

    key = cv2.waitKey(1) & 0xFF

 
    if key == ord('1'):
        if not recording:
            print("[FOREHAND START]")
            recording = True
            current_label = "F"
            sequence = []
        else:
            print("[FOREHAND END]")
            recording = False

            if len(sequence) > 5:
                f_count += 1
                filename = f"forehand_raw_{f_count:03}.npy"
                np.save(os.path.join(SAVE_F, filename), np.array(sequence))
                print(f"[SAVED] {filename} | frames:", len(sequence))


    if key == ord('2'):
        if not recording:
            print("[BACKHAND START]")
            recording = True
            current_label = "B"
            sequence = []
        else:
            print("[BACKHAND END]")
            recording = False

            if len(sequence) > 5:
                b_count += 1
                filename = f"backhand_raw_{b_count:03}.npy"
                np.save(os.path.join(SAVE_B, filename), np.array(sequence))
                print(f"[SAVED] {filename} | frames:", len(sequence))

  
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
print("Done ")


# In[5]:


import cv2
import mediapipe as mp
import numpy as np
import os


VIDEO_PATH = r"C:\Users\DellG5\Desktop\GA.mp4"
SAVE_F = r"C:\Users\DellG5\Desktop\TENNIS DATA\extra\F"
SAVE_B = r"C:\Users\DellG5\Desktop\TENNIS DATA\extra\B"
os.makedirs(SAVE_F, exist_ok=True)
os.makedirs(SAVE_B, exist_ok=True)


mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils
pose = mp_pose.Pose()


cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    print("Error: Cannot open video file")
    exit()


ret, frame = cap.read()
if not ret:
    print("Error: Cannot read first frame")
    exit()

orig_height, orig_width = frame.shape[:2]
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)


max_width = 1000
ratio = max_width / orig_width
new_width = int(orig_width * ratio)
new_height = int(orig_height * ratio)


recording = False
current_label = None
sequence = []

f_count = len(os.listdir(SAVE_F))
b_count = len(os.listdir(SAVE_B))

print("Press 1 = Forehand")
print("Press 2 = Backhand")
print("ESC to quit")


cv2.namedWindow("Stroke Recorder", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Stroke Recorder", new_width, new_height)


while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

   
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb)

   
    if results.pose_landmarks:
        mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    if recording and results.pose_landmarks:
        landmarks = []
        for lm in results.pose_landmarks.landmark:
            landmarks.extend([lm.x, lm.y, lm.z, lm.visibility])
        sequence.append(landmarks)

    
    cv2.imshow("Stroke Recorder", frame)

    key = cv2.waitKey(30) & 0xFF

   
    if key == ord('1'):
        if not recording:
            print("[FOREHAND START]")
            recording = True
            current_label = "F"
            sequence = []
        else:
            print("[FOREHAND END]")
            recording = False
            if len(sequence) > 5:
                f_count += 1
                filename = f"forehand_raw_{f_count:03}.npy"
                np.save(os.path.join(SAVE_F, filename), np.array(sequence))
                print(f"[SAVED] {filename} | frames: {len(sequence)}")

    
    if key == ord('2'):
        if not recording:
            print("[BACKHAND START]")
            recording = True
            current_label = "B"
            sequence = []
        else:
            print("[BACKHAND END]")
            recording = False
            if len(sequence) > 5:
                b_count += 1
                filename = f"backhand_raw_{b_count:03}.npy"
                np.save(os.path.join(SAVE_B, filename), np.array(sequence))
                print(f"[SAVED] {filename} | frames: {len(sequence)}")

    # EXIT
    if key == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()
print("Done ")


# In[ ]:


the next is 3 videos we will do the same thing 1 for forehand and 2 for backhand there path is C:\Users\DellG5\Desktop\T1.mp4 , C:\Users\DellG5\Desktop\T2.mp4 , C:\Users\DellG5\Desktop\T3.mp4 


# In[6]:


import cv2
import numpy as np
import mediapipe as mp
import os
import time


videos = [
    r"C:\Users\DellG5\Desktop\T1.mp4",
    r"C:\Users\DellG5\Desktop\T2.mp4",
    r"C:\Users\DellG5\Desktop\T3.mp4"
]

save_path = r"C:\Users\DellG5\Desktop\TENNIS DATA\extra\F"
os.makedirs(save_path, exist_ok=True)


mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils


recording = False
stroke_label = None
frames = []


existing = len([f for f in os.listdir(save_path) if f.endswith(".npy")])
print(f"Existing clips: {existing}")
print("Press 1 = forehand | 2 = backhand | ESC = quit")


for video in videos:
    print(f"\nProcessing: {video}")
    cap = cv2.VideoCapture(video)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

       
        time.sleep(0.03)

        
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(img_rgb)

        if results.pose_landmarks:
            mp_draw.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS
            )

       
        if recording and results.pose_landmarks:
            keypoints = []
            for lm in results.pose_landmarks.landmark:
                keypoints.extend([lm.x, lm.y, lm.z])
            frames.append(keypoints)

        cv2.imshow("Stroke Recorder", frame)

        key = cv2.waitKey(1) & 0xFF

      
        if key == ord('1'):
            if not recording:
                print("[FOREHAND START]")
                recording = True
                stroke_label = "forehand"
                frames = []
            else:
                print("[FOREHAND END]")
                recording = False

                filename = f"{stroke_label}_{existing+1:03d}.npy"
                np.save(os.path.join(save_path, filename), np.array(frames))

                print(f"[SAVED] {filename} | frames: {len(frames)}")
                existing += 1

        
        if key == ord('2'):
            if not recording:
                print("[BACKHAND START]")
                recording = True
                stroke_label = "backhand"
                frames = []
            else:
                print("[BACKHAND END]")
                recording = False

                filename = f"{stroke_label}_{existing+1:03d}.npy"
                np.save(os.path.join(save_path, filename), np.array(frames))

                print(f"[SAVED] {filename} | frames: {len(frames)}")
                existing += 1

    
        if key == 27:
            cap.release()
            cv2.destroyAllWindows()
            exit()

    cap.release()

cv2.destroyAllWindows()
print("Done ")


# In[1]:


import cv2
import numpy as np
import mediapipe as mp
import os
import time


videos = [
    r"C:\Users\DellG5\Desktop\T1.mp4",
    r"C:\Users\DellG5\Desktop\T2.mp4",
    r"C:\Users\DellG5\Desktop\T3.mp4"
]
save_path = r"C:\Users\DellG5\Desktop\TENNIS DATA\extra\F"
os.makedirs(save_path, exist_ok=True)


mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils


recording = False
stroke_label = None
frames = []


existing = len([f for f in os.listdir(save_path) if f.endswith(".npy")])
print(f"Existing clips: {existing}")
print("Press 1 = forehand | 2 = backhand | ESC = quit")

cv2.namedWindow("Stroke Recorder", cv2.WINDOW_NORMAL)  


first_frame_read = False
window_width = 1000  


for video in videos:
    print(f"\nProcessing: {video}")
    cap = cv2.VideoCapture(video)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
      
        time.sleep(0.03)
        
        
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(img_rgb)
        if results.pose_landmarks:
            mp_draw.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS
            )
        
        
        if recording and results.pose_landmarks:
            keypoints = []
            for lm in results.pose_landmarks.landmark:
                keypoints.extend([lm.x, lm.y, lm.z])
            frames.append(keypoints)
        
        
        if not first_frame_read:
            h, w = frame.shape[:2]
            ratio = window_width / w
            new_w = int(w * ratio)
            new_h = int(h * ratio)
            cv2.resizeWindow("Stroke Recorder", new_w, new_h)
            first_frame_read = True
        
        
        cv2.imshow("Stroke Recorder", frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        
        if key == ord('1'):
            if not recording:
                print("[FOREHAND START]")
                recording = True
                stroke_label = "forehand"
                frames = []
            else:
                print("[FOREHAND END]")
                recording = False
                filename = f"{stroke_label}_{existing+1:03d}.npy"
                np.save(os.path.join(save_path, filename), np.array(frames))
                print(f"[SAVED] {filename} | frames: {len(frames)}")
                existing += 1
        
        
        if key == ord('2'):
            if not recording:
                print("[BACKHAND START]")
                recording = True
                stroke_label = "backhand"
                frames = []
            else:
                print("[BACKHAND END]")
                recording = False
                filename = f"{stroke_label}_{existing+1:03d}.npy"
                np.save(os.path.join(save_path, filename), np.array(frames))
                print(f"[SAVED] {filename} | frames: {len(frames)}")
                existing += 1
        
      
        if key == 27:
            cap.release()
            cv2.destroyAllWindows()
            exit()
    
    cap.release()
    first_frame_read = False  

cv2.destroyAllWindows()
print("Done ")


# In[ ]:


import numpy as np
import mediapipe as mp
import os
import time
import ctypes


videos = [
    r"C:\Users\DellG5\Desktop\ST1.mp4",
    r"C:\Users\DellG5\Desktop\ST2.mp4",
    r"C:\Users\DellG5\Desktop\ST3.mp4",
    r"C:\Users\DellG5\Desktop\ST4.mp4"
]


SAVE_F = r"C:\Users\DellG5\Desktop\TENNIS DATA\extra\F"
SAVE_B = r"C:\Users\DellG5\Desktop\TENNIS DATA\extra\B"
SAVE_S = r"C:\Users\DellG5\Desktop\TENNIS DATA\extra\S"

os.makedirs(SAVE_F, exist_ok=True)
os.makedirs(SAVE_B, exist_ok=True)
os.makedirs(SAVE_S, exist_ok=True)

user32 = ctypes.windll.user32
screen_w = user32.GetSystemMetrics(0)
screen_h = user32.GetSystemMetrics(1)


mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils


def count_files(path):
    return len([f for f in os.listdir(path) if f.endswith(".npy")])

count_F = count_files(SAVE_F)
count_B = count_files(SAVE_B)
count_S = count_files(SAVE_S)

print(f"Existing Forehands: {count_F}")
print(f"Existing Backhands: {count_B}")
print(f"Existing Serves: {count_S}")

print("\nControls:")
print("1 = Forehand")
print("2 = Backhand")
print("3 = Serve")
print("ESC = Quit")


recording = False
frames = []
stroke_label = None
save_path = None

for video in videos:

    print(f"\nProcessing: {video}")
    cap = cv2.VideoCapture(video)

    while cap.isOpened():

        ret, frame = cap.read()
        if not ret:
            break

        time.sleep(0.03)  

        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(img_rgb)

        if results.pose_landmarks:
            mp_draw.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS
            )

       
        if recording and results.pose_landmarks:
            keypoints = []
            for lm in results.pose_landmarks.landmark:
                keypoints.extend([lm.x, lm.y, lm.z])
            frames.append(keypoints)

        
        h, w, _ = frame.shape
        scale = min(screen_w / w, screen_h / h)
        new_w = int(w * scale)
        new_h = int(h * scale)
        resized = cv2.resize(frame, (new_w, new_h))

        cv2.imshow("Stroke Recorder", resized)

        key = cv2.waitKey(1) & 0xFF

       
        if key == ord('1'):
            if not recording:
                print("[FOREHAND START]")
                recording = True
                stroke_label = "forehand"
                save_path = SAVE_F
                frames = []
            else:
                print("[FOREHAND END]")
                recording = False
                count_F += 1
                filename = f"forehand_{count_F:03d}.npy"
                np.save(os.path.join(save_path, filename), np.array(frames))
                print(f"[SAVED] {filename} | frames: {len(frames)}")


        if key == ord('2'):
            if not recording:
                print("[BACKHAND START]")
                recording = True
                stroke_label = "backhand"
                save_path = SAVE_B
                frames = []
            else:
                print("[BACKHAND END]")
                recording = False
                count_B += 1
                filename = f"backhand_{count_B:03d}.npy"
                np.save(os.path.join(save_path, filename), np.array(frames))
                print(f"[SAVED] {filename} | frames: {len(frames)}")

        if key == ord('3'):
            if not recording:
                print("[SERVE START]")
                recording = True
                stroke_label = "serve"
                save_path = SAVE_S
                frames = []
            else:
                print("[SERVE END]")
                recording = False
                count_S += 1
                filename = f"serve_{count_S:03d}.npy"
                np.save(os.path.join(save_path, filename), np.array(frames))
                print(f"[SAVED] {filename} | frames: {len(frames)}")

        if key == 27:
            cap.release()
            cv2.destroyAllWindows()
            exit()

    cap.release()

cv2.destroyAllWindows()
print("Done ")


# In[1]:


import cv2
import mediapipe as mp
import numpy as np
import os
import time


VIDEOS = [
    r"C:\Users\DellG5\Desktop\T6.MP4",
    r"C:\Users\DellG5\Desktop\T7.MP4"
]


SAVE_F = r"C:\Users\DellG5\Desktop\TENNIS DATA\extra\F"
SAVE_B = r"C:\Users\DellG5\Desktop\TENNIS DATA\extra\B"
SAVE_S = r"C:\Users\DellG5\Desktop\TENNIS DATA\extra\S"

os.makedirs(SAVE_F, exist_ok=True)
os.makedirs(SAVE_B, exist_ok=True)
os.makedirs(SAVE_S, exist_ok=True)


f_count = len([f for f in os.listdir(SAVE_F) if f.endswith(".npy")])
b_count = len([f for f in os.listdir(SAVE_B) if f.endswith(".npy")])
s_count = len([f for f in os.listdir(SAVE_S) if f.endswith(".npy")])

print("Existing Forehands:", f_count)
print("Existing Backhands:", b_count)
print("Existing Serves:", s_count)

print("\nControls:")
print("1 = Forehand")
print("2 = Backhand")
print("3 = Serve")
print("ESC = Quit\n")


mp_pose = mp.solutions.pose
pose = mp_pose.Pose()


JOINTS = [
    mp_pose.PoseLandmark.RIGHT_WRIST,
    mp_pose.PoseLandmark.RIGHT_ELBOW,
    mp_pose.PoseLandmark.RIGHT_SHOULDER,
    mp_pose.PoseLandmark.LEFT_WRIST,
    mp_pose.PoseLandmark.LEFT_ELBOW,
    mp_pose.PoseLandmark.LEFT_SHOULDER,
    mp_pose.PoseLandmark.RIGHT_HIP,
    mp_pose.PoseLandmark.LEFT_HIP,
    mp_pose.PoseLandmark.RIGHT_KNEE,
    mp_pose.PoseLandmark.LEFT_KNEE,
    mp_pose.PoseLandmark.NOSE
]


recording = False
stroke = []
current_class = None


for video in VIDEOS:

    print("Processing:", video)

    cap = cv2.VideoCapture(video)

  
    if not cap.isOpened():
        print("ERROR: Could not open", video)
        continue

    cv2.namedWindow("Tennis Recorder", cv2.WINDOW_NORMAL)

    while cap.isOpened():

        ret, frame = cap.read()
        if not ret:
            break

       
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)

        if results.pose_landmarks:

            landmarks = results.pose_landmarks.landmark

            frame_data = []
            for j in JOINTS:
                lm = landmarks[j]
                frame_data.append([lm.x, lm.y])

            frame_data = np.array(frame_data)

            if recording:
                stroke.append(frame_data)

         
            mp.solutions.drawing_utils.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS
            )

      
        h, w = frame.shape[:2]
        screen_w = 1200
        scale = screen_w / w
        new_h = int(h * scale)
        display = cv2.resize(frame, (screen_w, new_h))

       
        if current_class == 1:
            label = "FOREHAND"
            color = (0, 255, 0)
        elif current_class == 2:
            label = "BACKHAND"
            color = (255, 0, 0)
        elif current_class == 3:
            label = "SERVE"
            color = (0, 0, 255)
        else:
            label = "NONE"
            color = (200, 200, 200)

        cv2.putText(display, label, (40, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, color, 4)

     
        if recording:
            cv2.circle(display, (50, 120), 15, (0, 0, 255), -1)

        cv2.imshow("Tennis Recorder", display)

        key = cv2.waitKey(30) & 0xFF

       
        if key == ord('1'):
            if not recording:
                recording = True
                current_class = 1
                stroke = []
                print("\n[START] Forehand")
            else:
                recording = False
                if len(stroke) > 15:
                    f_count += 1
                    name = f"forehand_{f_count:03d}.npy"
                    np.save(os.path.join(SAVE_F, name), np.array(stroke))
                    print("[SAVED]", name, "| frames:", len(stroke))
                else:
                    print("Too short, ignored")

        
        if key == ord('2'):
            if not recording:
                recording = True
                current_class = 2
                stroke = []
                print("\n[START] Backhand")
            else:
                recording = False
                if len(stroke) > 15:
                    b_count += 1
                    name = f"backhand_{b_count:03d}.npy"
                    np.save(os.path.join(SAVE_B, name), np.array(stroke))
                    print("[SAVED]", name, "| frames:", len(stroke))
                else:
                    print("Too short, ignored")

     
        if key == ord('3'):
            if not recording:
                recording = True
                current_class = 3
                stroke = []
                print("\n[START] Serve")
            else:
                recording = False
                if len(stroke) > 15:
                    s_count += 1
                    name = f"serve_{s_count:03d}.npy"
                    np.save(os.path.join(SAVE_S, name), np.array(stroke))
                    print("[SAVED]", name, "| frames:", len(stroke))
                else:
                    print("Too short, ignored")

        if key == 27:
            break

        time.sleep(0.01)

    cap.release()

cv2.destroyAllWindows()
print("Done ")


# In[3]:


import numpy as np
import os
from scipy.signal import resample


BASE = r"C:\Users\DellG5\Desktop\TENNIS DATA"


NEW_B = os.path.join(BASE, "new data", "B")
NEW_F = os.path.join(BASE, "new data", "F")
NEW_S = os.path.join(BASE, "new data", "S")


OUT_B = os.path.join(BASE, "backhand_v3_resampled")
OUT_F = os.path.join(BASE, "forehand_v2_resampled")
OUT_S = os.path.join(BASE, "serve_v3_resampled")

TARGET_FRAMES = 30


R_HIP_IDX = 6
L_HIP_IDX = 7

print(" Imports done")
print(f"New B folder: {NEW_B}")
print(f"New F folder: {NEW_F}")
print(f"New S folder: {NEW_S}")


# In[4]:


def preprocess_clip(data):
    
    hip_mid = (data[:, R_HIP_IDX, :] + data[:, L_HIP_IDX, :]) / 2.0
    hip_mid = hip_mid[:, np.newaxis, :]                                  
    data = data - hip_mid                                                

    
    data = resample(data, TARGET_FRAMES, axis=0)                      

    return data.astype(np.float32)

print(" Preprocessing function ready")


# In[5]:


def process_folder(input_folder, output_folder, label_name, prefix):
    
    os.makedirs(output_folder, exist_ok=True)
    files = sorted([f for f in os.listdir(input_folder) if f.endswith(".npy")])
    
    if len(files) == 0:
        print(f"  No .npy files found in {input_folder}")
        return 0

    saved = 0
    for f in files:
        raw = np.load(os.path.join(input_folder, f))

        
        if raw.ndim != 3 or raw.shape[1] != 11 or raw.shape[2] != 2:
            print(f"    Skipping {f} — unexpected shape {raw.shape}")
            continue

        cleaned = preprocess_clip(raw)

      
        new_name = f"court_{prefix}_{saved+1:03d}.npy"
        np.save(os.path.join(output_folder, new_name), cleaned)
        saved += 1

    print(f" {label_name}: {saved} clips processed → saved to {output_folder}")
    return saved


n_b = process_folder(NEW_B, OUT_B, "Backhand", "backhand")
n_f = process_folder(NEW_F, OUT_F, "Forehand", "forehand")
n_s = process_folder(NEW_S, OUT_S, "Serve",    "serve")

print(f"\n Total new clips added: {n_b + n_f + n_s}")


# In[6]:


def verify_folder(folder, label_name):
    files = sorted([f for f in os.listdir(folder) if f.endswith(".npy")])
    errors = []
    
    for f in files:
        data = np.load(os.path.join(folder, f))
        if data.shape != (30, 11, 2):
            errors.append(f"  ❌ {f} → shape {data.shape}")
        if np.isnan(data).any():
            errors.append(f"  ❌ {f} → contains NaN")
        if np.all(data == 0):
            errors.append(f"  ❌ {f} → all zeros (empty)")

    if errors:
        print(f"\n⚠️  {label_name} — {len(errors)} problem(s) found:")
        for e in errors:
            print(e)
    else:
        print(f"✅ {label_name}: {len(files)} clips — all clean (shape 30,11,2) ✓")

verify_folder(OUT_F, "Forehand")
verify_folder(OUT_B, "Backhand")
verify_folder(OUT_S, "Serve")

print("\n Final clip counts:")
for name, folder in [("Forehand", OUT_F), ("Backhand", OUT_B), ("Serve", OUT_S)]:
    count = len([f for f in os.listdir(folder) if f.endswith(".npy")])
    print(f"  {name}: {count} clips")


# In[7]:


from scipy.signal import resample
import numpy as np
import os

FOREHAND_FOLDER = r"C:\Users\DellG5\Desktop\TENNIS DATA\forehand_v2_resampled"

fixed = 0
for f in sorted(os.listdir(FOREHAND_FOLDER)):
    if not f.endswith(".npy"):
        continue
    path = os.path.join(FOREHAND_FOLDER, f)
    data = np.load(path)
    
    if data.shape != (30, 11, 2):
       
        data_fixed = resample(data, 30, axis=0).astype(np.float32)
        np.save(path, data_fixed)
        print(f"  Fixed: {f}  {data.shape} → {data_fixed.shape}")
        fixed += 1

print(f"\n Fixed {fixed} files")


# In[8]:


JOINT_INDICES_33 = [16, 14, 12, 15, 13, 11, 24, 23, 26, 25, 0]
R_HIP_IDX = 6
L_HIP_IDX = 7

def rescue_99(data_flat):
    """
    Input: (frames, 99) — 33 joints × 3 (x, y, visibility)
    Output: (30, 11, 2) — our 11 joints, hip-centered, resampled
    """
    frames = data_flat.shape[0]
    all_joints = data_flat.reshape(frames, 33, 3)   
    xy = all_joints[:, :, :2]                        )
    
   
    our_joints = xy[:, JOINT_INDICES_33, :]          
    
    
    hip_mid = (our_joints[:, R_HIP_IDX, :] + our_joints[:, L_HIP_IDX, :]) / 2.0
    hip_mid = hip_mid[:, np.newaxis, :]
    our_joints = our_joints - hip_mid
    
    
    our_joints = resample(our_joints, 30, axis=0).astype(np.float32)
    
    return our_joints  


rescue_map = {
    r"C:\Users\DellG5\Desktop\TENNIS DATA\new data\B": (r"C:\Users\DellG5\Desktop\TENNIS DATA\backhand_v3_resampled", "backhand"),
    r"C:\Users\DellG5\Desktop\TENNIS DATA\new data\F": (r"C:\Users\DellG5\Desktop\TENNIS DATA\forehand_v2_resampled", "forehand"),
    r"C:\Users\DellG5\Desktop\TENNIS DATA\new data\S": (r"C:\Users\DellG5\Desktop\TENNIS DATA\serve_v3_resampled",    "serve"),
}

total_rescued = 0

for src_folder, (dst_folder, prefix) in rescue_map.items():
    rescued = 0
    for f in sorted(os.listdir(src_folder)):
        if not f.endswith(".npy"):
            continue
        data = np.load(os.path.join(src_folder, f))
        
        if data.ndim == 2 and data.shape[1] == 99:
            fixed = rescue_99(data)
         
            existing = [x for x in os.listdir(dst_folder) if x.startswith(f"court_{prefix}")]
            new_name = f"court_{prefix}_rescued_{rescued+1:03d}.npy"
            np.save(os.path.join(dst_folder, new_name), fixed)
            rescued += 1
    
    print(f" Rescued {rescued} clips → {dst_folder}")
    total_rescued += rescued

print(f"\n Total rescued: {total_rescued}")


# In[9]:


def verify_folder(folder, label_name):
    files = sorted([f for f in os.listdir(folder) if f.endswith(".npy")])
    errors = []
    for f in files:
        data = np.load(os.path.join(folder, f))
        if data.shape != (30, 11, 2):
            errors.append(f"  ❌ {f} → shape {data.shape}")
        if np.isnan(data).any():
            errors.append(f"  ❌ {f} → contains NaN")

    if errors:
        print(f"⚠️  {label_name} — {len(errors)} problem(s):")
        for e in errors: print(e)
    else:
        print(f"✅ {label_name}: {len(files)} clips — all clean ")

verify_folder(r"C:\Users\DellG5\Desktop\TENNIS DATA\forehand_v2_resampled", "Forehand")
verify_folder(r"C:\Users\DellG5\Desktop\TENNIS DATA\backhand_v3_resampled", "Backhand")
verify_folder(r"C:\Users\DellG5\Desktop\TENNIS DATA\serve_v3_resampled",    "Serve")

print("\n Final clip counts:")
for name, folder in [
    ("Forehand", r"C:\Users\DellG5\Desktop\TENNIS DATA\forehand_v2_resampled"),
    ("Backhand", r"C:\Users\DellG5\Desktop\TENNIS DATA\backhand_v3_resampled"),
    ("Serve",    r"C:\Users\DellG5\Desktop\TENNIS DATA\serve_v3_resampled"),
]:
    count = len([f for f in os.listdir(folder) if f.endswith(".npy")])
    print(f"  {name}: {count} clips")


# In[10]:


import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


BASE = r"C:\Users\DellG5\Desktop\TENNIS DATA"
FOLDERS = {
    "Forehand": os.path.join(BASE, "forehand_v2_resampled"),
    "Backhand": os.path.join(BASE, "backhand_v3_resampled"),
    "Serve":    os.path.join(BASE, "serve_v3_resampled"),
}
COLORS = {"Forehand": "#00C850", "Backhand": "#C85000", "Serve": "#0050FF"}

def load_class(folder):
    clips = []
    for f in sorted(os.listdir(folder)):
        if f.endswith(".npy"):
            clips.append(np.load(os.path.join(folder, f)))
    return np.array(clips)  

data = {}
for name, folder in FOLDERS.items():
    data[name] = load_class(folder)
    print(f"✅ {name}: {data[name].shape}")


# In[11]:


JOINT_NAMES = ["R_Wrist","R_Elbow","R_Shoulder","L_Wrist","L_Elbow",
               "L_Shoulder","R_Hip","L_Hip","R_Knee","L_Knee","Nose"]

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Average Joint Trajectory Per Stroke Class", fontsize=14, fontweight='bold')

for ax, coord, coord_name in zip(axes, [0, 1], ["X (Horizontal)", "Y (Vertical)"]):
    for class_name, clips in data.items():
        
        mean_traj = clips[:, :, 0, coord].mean(axis=0)  
        std_traj  = clips[:, :, 0, coord].std(axis=0)
        
        t = np.arange(30)
        ax.plot(t, mean_traj, color=COLORS[class_name], label=class_name, linewidth=2.5)
        ax.fill_between(t, mean_traj - std_traj, mean_traj + std_traj,
                        color=COLORS[class_name], alpha=0.15)
    
    ax.set_xlabel("Frame", fontsize=11)
    ax.set_ylabel(f"R_Wrist {coord_name} (hip-centered)", fontsize=11)
    ax.set_title(f"R_Wrist {coord_name} Motion", fontsize=12)
    ax.legend()
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("fig1_avg_trajectory.png", dpi=150, bbox_inches='tight')
plt.show()
print(" Saved: fig1_avg_trajectory.png")


# In[12]:


fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle("Right Wrist Path in 2D Space (Hip-Centered, All Clips Overlaid)",
             fontsize=13, fontweight='bold')

for ax, (class_name, clips) in zip(axes, data.items()):
    for clip in clips:
        wrist_x = clip[:, 0, 0]
        wrist_y = clip[:, 0, 1]  
        ax.plot(wrist_x, wrist_y, color=COLORS[class_name], alpha=0.3, linewidth=1)
    
    
    mean_x = clips[:, :, 0, 0].mean(axis=0)
    mean_y = clips[:, :, 0, 1].mean(axis=0)
    ax.plot(mean_x, mean_y, color='black', linewidth=2.5, label='Mean path')
    ax.plot(mean_x[0], mean_y[0], 'go', markersize=8, label='Start')
    ax.plot(mean_x[-1], mean_y[-1], 'rs', markersize=8, label='End')
    
    ax.set_title(class_name, fontsize=13, color=COLORS[class_name], fontweight='bold')
    ax.set_xlabel("X (horizontal)")
    ax.set_ylabel("Y (vertical)")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.invert_yaxis()  

plt.tight_layout()
plt.savefig("fig2_wrist_path.png", dpi=150, bbox_inches='tight')
plt.show()
print("✅ Saved: fig2_wrist_path.png")


# In[13]:


sample_raw_path = os.path.join(BASE, "forehand_v2_resampled", 
                               sorted(os.listdir(os.path.join(BASE, "forehand_v2_resampled")))[0])
sample = np.load(sample_raw_path)  


fake_offset = np.array([0.5, 0.4])
sample_before = sample + fake_offset

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle("Hip Centering: Before vs After Normalization", fontsize=13, fontweight='bold')

for ax, clip, title in zip(axes, [sample_before, sample], ["Before (Raw Position)", "After (Hip-Centered)"]):
    for joint_idx in range(11):
        ax.plot(clip[:, joint_idx, 0], clip[:, joint_idx, 1],
                alpha=0.6, linewidth=1.5, label=JOINT_NAMES[joint_idx])
    ax.set_title(title, fontsize=12)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.invert_yaxis()
    ax.grid(True, alpha=0.3)

axes[0].legend(fontsize=7, loc='upper right')
plt.tight_layout()
plt.savefig("fig3_hip_centering.png", dpi=150, bbox_inches='tight')
plt.show()
print(" Saved: fig3_hip_centering.png")


# In[14]:


counts = {name: len(clips) for name, clips in data.items()}

fig, ax = plt.subplots(figsize=(7, 5))
bars = ax.bar(counts.keys(), counts.values(),
              color=[COLORS[k] for k in counts.keys()],
              edgecolor='black', linewidth=0.8, width=0.5)

for bar, val in zip(bars, counts.values()):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            str(val), ha='center', va='bottom', fontsize=13, fontweight='bold')

ax.axhline(y=50, color='gray', linestyle='--', linewidth=1.5, label='Target (50)')
ax.set_ylim(0, 65)
ax.set_ylabel("Number of Clips", fontsize=12)
ax.set_title("Dataset Balance: Clips Per Class", fontsize=13, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig("fig4_dataset_balance.png", dpi=150, bbox_inches='tight')
plt.show()
print(" Saved: fig4_dataset_balance.png")


# In[15]:


fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle("Joint Movement Magnitude Per Class (Mean Absolute Displacement)",
             fontsize=13, fontweight='bold')

for ax, (class_name, clips) in zip(axes, data.items()):
    
    movement = clips.std(axis=1).mean(axis=0)  
    magnitude = np.sqrt(movement[:, 0]**2 + movement[:, 1]**2)  
    
    bars = ax.barh(JOINT_NAMES, magnitude, color=COLORS[class_name], edgecolor='black', linewidth=0.5)
    ax.set_title(class_name, fontsize=13, color=COLORS[class_name], fontweight='bold')
    ax.set_xlabel("Movement Magnitude")
    ax.grid(True, alpha=0.3, axis='x')
    ax.invert_yaxis()

plt.tight_layout()
plt.savefig("fig5_joint_movement.png", dpi=150, bbox_inches='tight')
plt.show()
print(" Saved: fig5_joint_movement.png")


# In[ ]:




