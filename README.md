# VirtualMouseApp

A gesture-controlled virtual mouse built with Python, OpenCV, and MediaPipe — control your cursor using hand movements without any physical hardware.

## Features

- Real-time hand tracking using MediaPipe (21 hand landmarks detected)
- Index finger tip mapped to cursor movement across the screen
- Pinch gesture (thumb + index finger) triggers mouse click
- Smoothening algorithm to reduce cursor jitter and improve responsiveness
- Click cooldown (0.5s) to prevent accidental multiple clicks
- Frame margin mapping for better control accuracy

## Tech Stack

- Language: Python 3.12
- Computer Vision: OpenCV
- Hand Tracking: MediaPipe
- Mouse Control: PyAutoGUI
- Numerical Processing: NumPy

## How It Works

1. Webcam captures real-time video frames
2. MediaPipe detects hand landmarks (21 points per hand)
3. Index finger tip (Landmark 8) coordinates are mapped to screen resolution
4. Smoothening algorithm reduces jitter between frames
5. Distance between thumb (Landmark 4) and index finger (Landmark 8) is calculated
6. If distance is less than 30 pixels (pinch), a mouse click is triggered

## Setup

1. Clone the repository
2. Create a virtual environment: python -m venv venv
3. Activate: venv\Scripts\activate
4. Install dependencies: pip install opencv-python mediapipe==0.10.13 pyautogui numpy
5. Run: python virtual_mouse.py
6. Press 'q' to quit

## Controls

- Move index finger — moves cursor
- Pinch (thumb + index finger close together) — left click
- Press 'q' on keyboard — quit the application