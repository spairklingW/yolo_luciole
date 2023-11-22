import cv2
import numpy as np

#https://github.com/pythonlessons/TensorFlow-2.x-YOLOv3

# Load YOLO
#net = cv2.dnn.readNetFromDarknet("tinyYolo/tiny.cfg", "tinyYolo/yolov3-tiny.weights")
net = cv2.dnn.readNetFromDarknet("yolo-coco/yolov3.cfg", "yolo-coco/yolov3.weights")
layer_names = net.getLayerNames()
output_layers = [layer_names[i-1] for i in net.getUnconnectedOutLayers()]

# Load image
image = cv2.imread("images/baggage_claim.jpg")
#cv2.imshow("People Detection", image)
height, width, channels = image.shape

# Resize image
blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
net.setInput(blob)
outs = net.forward(output_layers)

# Get confidence threshold
conf_threshold = 0.5

# Get bounding boxes, confidences, and class IDs
class_ids = []
confidences = []
boxes = []

for out in outs:
    for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)
        print(class_id)
        confidence = scores[class_id]
        print(confidence)
        if confidence > conf_threshold and class_id == 0:  # 0 corresponds to the person class in COCO dataset
            # Scale back the coordinates to the original image size
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)

            # Calculate the top-left corner of the bounding box
            x = int(center_x - w / 2)
            y = int(center_y - h / 2)

            boxes.append([x, y, w, h])
            confidences.append(float(confidence))
            class_ids.append(class_id)

# Apply non-maximum suppression to remove overlapping bounding boxes
indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, 0.4)

# Draw bounding boxes on the image
if len(indices) > 0:
    for i in indices:
        i = i[0]
        x, y, w, h = boxes[i]
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Display the result
cv2.imshow("People Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

