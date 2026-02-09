---
id: computer-vision
title: Computer Vision for Robotics
sidebar_label: Computer Vision
sidebar_position: 2
---

# Computer Vision for Robotics

Computer vision enables robots to perceive and understand their environment through cameras. This is essential for navigation, object manipulation, and human-robot interaction.

## Image Processing with OpenCV

```python
import cv2
import numpy as np

# Read image
image = cv2.imread('robot_view.jpg')

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur (noise reduction)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Edge detection (Canny)
edges = cv2.Canny(blurred, 50, 150)

# Display
cv2.imshow('Edges', edges)
cv2.waitKey(0)
```

## Object Detection

```python
# Using pre-trained YOLO model
import cv2

# Load YOLO
net = cv2.dnn.readNet('yolov4.weights', 'yolov4.cfg')
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Load image
img = cv2.imread('scene.jpg')
height, width, _ = img.shape

# Detect objects
blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
net.setInput(blob)
outputs = net.forward(output_layers)

# Process detections
for output in outputs:
    for detection in output:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]

        if confidence > 0.5:
            # Object detected with high confidence
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)

            # Draw bounding box
            cv2.rectangle(img, (center_x - w//2, center_y - h//2),
                         (center_x + w//2, center_y + h//2), (0, 255, 0), 2)
```

## Key Takeaways

- ✅ OpenCV is the standard library for computer vision
- ✅ Image processing pipeline: capture → filter → detect → classify
- ✅ Deep learning models (YOLO, SSD) for object detection
- ✅ Camera calibration ensures accurate measurements

## Next Lesson

Continue to [Motion Planning](./motion-planning) to learn path planning algorithms!
