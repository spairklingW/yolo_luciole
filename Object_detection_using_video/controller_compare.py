# USAGE
# python yolo_video.py --input videos/airport.mp4 --output output/airport_output.avi --yolo yolo-coco

# import the necessary packages
import numpy as np
import argparse
import imutils
import time
import cv2
import os
from VideoStream import *
from Ambiancer import *

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
	help="path to input video")
ap.add_argument("-o", "--output", required=True,
	help="path to output video")
ap.add_argument("-y", "--yolo", required=True,
	help="base path to YOLO directory")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
ap.add_argument("-t", "--threshold", type=float, default=0.3,
	help="threshold when applyong non-maxima suppression")
args = vars(ap.parse_args())

# load the COCO class labels our YOLO model was trained on
labelsPath = os.path.sep.join([args["yolo"], "coco.names"])
LABELS = open(labelsPath).read().strip().split("\n")

# initialize a list of colors to represent each possible class label
np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
	dtype="uint8")

# derive the paths to the YOLO weights and model configuration
weightsPath = os.path.sep.join([args["yolo"], "yolov3.weights"])
configPath = os.path.sep.join([args["yolo"], "yolov3.cfg"])

# load our YOLO object detector trained on COCO dataset (80 classes)
# and determine only the *output* layer names that we need from YOLO
print("[INFO] loading YOLO from disk...")
net3 = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

ln = net.getLayerNames()
ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]

# initialize the video stream, pointer to output video file, and
# frame dimensions
#vs = cv2.VideoCapture(args["input"])
writer = None
(W, H) = (None, None)

video_stream = VideoStream(args["input"])
video_stream.start()

frames_proc = []

_confidences = []

lay = None

# loop over frames from the video file stream
while True:

	print("increment")

	if video_stream.is_stopped():
		break

	#frame = video_stream.read()
	frame = cv2.imread('C:\\Users\\brene\\source\\repos\\github\\yolo_luciole\\images\\gospel.jpg')
	# if the frame dimensions are empty, grab them
	if W is None or H is None:
		(H, W) = frame.shape[:2]

	# construct a blob from the input frame and then perform a forward
	# pass of the YOLO object detector, giving us our bounding boxes
	# and associated probabilities
	blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
		swapRB=True, crop=False)
	net.setInput(blob)
	start = time.time()
	layerOutputs = net.forward(ln)
	end = time.time()

	lay = layerOutputs

	# initialize our lists of detected bounding boxes, confidences,
	# and class IDs, respectively
	boxes = []
	confidences = []
	classIDs = []

	# loop over each of the layer outputs
	for output in layerOutputs:
		# loop over each of the detections
		for detection in output:
			# extract the class ID and confidence (i.e., probability)
			# of the current object detection
			scores = detection[5:]
			#print(scores)
			#print("BLALAAAAAA")

			classID = np.argmax(scores)

			if classID != 0:
				print("print classID")
				print(classID)
			confidence = scores[classID]

			_confidences.append(confidence)

			# filter out weak predictions by ensuring the detected
			# probability is greater than the minimum probability
			if confidence > args["confidence"]:
				# scale the bounding box coordinates back relative to
				# the size of the image, keeping in mind that YOLO
				# actually returns the center (x, y)-coordinates of
				# the bounding box followed by the boxes' width and
				# height
				box = detection[0:4] * np.array([W, H, W, H])
				(centerX, centerY, width, height) = box.astype("int")

				# use the center (x, y)-coordinates to derive the top
				# and and left corner of the bounding box
				x = int(centerX - (width / 2))
				y = int(centerY - (height / 2))

				# update our list of bounding box coordinates,
				# confidences, and class IDs
				boxes.append([x, y, int(width), int(height)])
				confidences.append(float(confidence))
				classIDs.append(classID)

	# apply non-maxima suppression to suppress weak, overlapping
	# bounding boxes
	idxs = cv2.dnn.NMSBoxes(boxes, confidences, args["confidence"],
		args["threshold"])

	# ensure at least one detection exists
	if len(idxs) > 0:
		# loop over the indexes we are keeping
		for i in idxs.flatten():
			# extract the bounding box coordinates
			(x, y) = (boxes[i][0], boxes[i][1])
			(w, h) = (boxes[i][2], boxes[i][3])

			# draw a bounding box rectangle and label on the frame
			#color = [int(c) for c in COLORS[classIDs[i]]]
			color = [int(c) for c in COLORS[classIDs[i]]]

			text = "{}: {:.4f}".format(LABELS[classIDs[i]],
				confidences[i])
			class_object = LABELS[classIDs[i]]

			if class_object == "person":
				#cv2.putText(frame, text, (x, y - 5),
					#cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
				cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

			# show the output image
			#cv2.imshow("Image", frame)
			#print(frame.shape[:2])
			#cv2.waitKey(0)

	# check if the video writer is None
	if writer is None:
		# initialize our video writer
		fourcc = cv2.VideoWriter_fourcc(*"MJPG")
		writer = cv2.VideoWriter(args["output"], fourcc, 30,
			(frame.shape[1], frame.shape[0]), True)

	frames_proc.append(frame)

	# write the output frame to disk
	writer.write(frame)

	break

# release the file pointers
print("[INFO] cleaning up...")
writer.release()
#vs.release()

show_image = True

if show_image:
	for f in frames_proc:
		# show the output image
		cv2.imshow("Image", f)
		cv2.waitKey(0)

#*********************************************

ambiancer = Ambiancer(labelsPath, weightsPath, configPath)

ambiancer.start_stream_proc(args["input"], args["confidence"], args["threshold"], args["output"])

ambiancer.show_images(False)

net_ambiancer = ambiancer.get_net()

net2 = net
#assert scores.all() == ambiancer.get_scores().all()
assert ambiancer.get_weightpath() == weightsPath
assert ambiancer.get_configpath() == configPath

print(scores)

print("ALLLEERRRR")
print(ambiancer.get_scores())
#assert confidences == ambiancer.get_confidence()

print(lay)
print("BOBOOO")
print(ambiancer.get_layerout())
assert lay.any() == ambiancer.get_layerout().any()
#assert net3 == net

print("ok")
#assert net == net