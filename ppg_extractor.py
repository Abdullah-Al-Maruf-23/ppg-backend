import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
import os

def butter_bandpass(lowcut, highcut, fs, order=4):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    return butter(order, [low, high], btype='band')

def apply_bandpass_filter(data, fs, lowcut=0.5, highcut=5.0):
    b, a = butter_bandpass(lowcut, highcut, fs)
    return filtfilt(b, a, data)

def extract_ppg(video_path, output_folder):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise Exception("Video can't be opened")

    fps = cap.get(cv2.CAP_PROP_FPS)
    green_vals = []
    timestamps = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, _ = rgb.shape
        cropped = rgb[h//3:2*h//3, w//3:2*w//3]
        green = np.mean(cropped[:, :, 1])
        green_vals.append(green)
        timestamps.append(len(timestamps) / fps)

    cap.release()

    green_vals = (np.array(green_vals) - np.mean(green_vals)) / np.std(green_vals)
    filtered = apply_bandpass_filter(green_vals, fps)

    plt.figure(figsize=(12, 4))
    plt.plot(timestamps, filtered, color='green')
    plt.title("Filtered PPG Signal")
    plt.xlabel("Time (s)")
    plt.ylabel("Intensity")
    plt.grid(True)

    os.makedirs(output_folder, exist_ok=True)
    out_path = os.path.join(output_folder, "ppg_result.png")
    plt.savefig(out_path)
    plt.close()
    return out_path
