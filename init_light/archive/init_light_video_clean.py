# USAGE
# python yolo_video.py --input videos/airport.mp4 --output output/airport_output.avi --yolo yolo-coco

# import the necessary packages
import numpy as np
import argparse
import imutils
import time
import cv2
import os
import numpy as np
import time

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
	help="path to input video")
ap.add_argument("-o", "--output", required=True,
	help="path to output video")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
ap.add_argument("-t", "--threshold", type=float, default=0.3,
	help="threshold when applyong non-maxima suppression")
args = vars(ap.parse_args())

# initialize the video stream, pointer to output video file, and
# frame dimensions
vs = cv2.VideoCapture(args["input"])
writer = None
(W, H) = (None, None)

# try to determine the total number of frames in the video file
try:
	prop = cv2.cv.CV_CAP_PROP_FRAME_COUNT if imutils.is_cv2() \
		else cv2.CAP_PROP_FRAME_COUNT
	total = int(vs.get(prop))
	print("[INFO] {} total frames in video".format(total))

# an error occurred while trying to determine the total
# number of frames in the video file
except:
	print("[INFO] could not determine # of frames in video")
	print("[INFO] no approx. completion time can be provided")
	total = -1

# def the previous image for the diff
prev_frame = None
diff = None
frame_light_transition_candidate = None
background_frame = None


def process_image_from_diff(prev_frame, current_frame):

	prev_frame_grey = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
	frame_grey = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)

	diff = cv2.absdiff(frame_grey, prev_frame_grey)

	# find the best threshold :
	# 1- check how many bounding box are generated, increase the threshold until only stays, for the transition images (2)
	# 2- store max sum of pixel intensity of of bounding boxes per image, applied threshold of 0.90max. Do the same for all images
	# and keep in the end the one containing the max of the max -> should be the transition image, apply bounding box to it.
	th, frame_thresh = cv2.threshold(diff, 100, 255, cv2.THRESH_BINARY)

	# opening to erase white noise on background (maybe not necessary after option above)
	kernel = np.ones((5, 5), np.uint8)
	frame_opened = cv2.morphologyEx(frame_thresh, cv2.MORPH_OPEN, kernel)

	return frame_opened


def export_frame_to_video(out_image):
	# check if the video writer is None
	global writer

	if writer is None:
		# initialize our video writer
		fourcc = cv2.VideoWriter_fourcc(*"MJPG")
		writer = cv2.VideoWriter(args["output"], fourcc, 30,
								 (out_image.shape[1], out_image.shape[0]), True)

	rgb_frame = cv2.cvtColor(out_image, cv2.COLOR_GRAY2RGB)
	writer.write(rgb_frame)



def process_images():

	print("into PROCESS IMAGES")

	global frame_light_transition_candidate
	global background_frame
	global H
	global W
	global writer

	prev_frame = None
	cnt = 0
	max_sum_candidate = 0

	setup_time = 1 # second
	elapsed_time = 0

	while elapsed_time < setup_time:

		time_start = time.time()

		# read the next frame from the file
		path = r'/Object_dection_using_image/images/living_room.jpg'
		frame = cv2.imread(path)

		elapsed_time = elapsed_time + time.time() - time_start
		time_start = time.time()
		print("this is the elaspsed time")
		print(elapsed_time)

		if 0.2 < elapsed_time < 0.7:
			cv2.circle(frame, (int(H/2), int(W/2)), 7, (255, 255, 255), -1)
			print("in the cercle")

		# if the frame dimensions are empty, grab them
		if W is None or H is None:
			(H, W) = frame.shape[:2]

		# store background image
		if cnt is 0:
			background_frame = frame

		# insert some code for processing the image and initializing
		if cnt is not 0:

			frame_opened = process_image_from_diff(prev_frame, frame)

			# calculate the frame with biggest sum
			if cnt is 1:
				# first diff frame, store as potential to set up recurrence
				frame_light_transition_candidate = frame_opened
			else:
				sum_opened_frame = np.sum(frame_opened)
				if sum_opened_frame > max_sum_candidate:
					max_sum_candidate = sum_opened_frame
					frame_light_transition_candidate = frame_opened

			out_image = frame_opened

			export_frame_to_video(out_image)

		prev_frame = frame
		cnt = cnt + 1
		elapsed_time = elapsed_time + time.time() - time_start


def find_object_position(frame_light_transition):

	global background_frame

	# compute bounding box on the frame_light_transition
	# detect the contours on the binary image using cv2.CHAIN_APPROX_NONE
	contours, hierarchy = cv2.findContours(image=frame_light_transition, mode=cv2.RETR_TREE,
										   method=cv2.CHAIN_APPROX_NONE)

	# draw contours on the original image
	image_copy = frame_light_transition.copy()
	cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(100, 100, 100), thickness=2,
					 lineType=cv2.LINE_AA)

	# Find the index of the largest contour (should be modified to most dense/ filled up)
	areas = [cv2.contourArea(c) for c in contours]
	max_index = np.argmax(areas)
	largest_contour = contours[max_index]

	x, y, w, h = cv2.boundingRect(largest_contour)
	cv2.rectangle(image_copy, (x, y), (x + w, y + h), (100, 100, 100), 2)

	#cv2.imshow('threshold', image_copy)
	#cv2.waitKey(0)

	# see the results
	#cv2.imshow('None approximation', image_copy)
	#cv2.waitKey(0)

	# compute the center of the contour
	M = cv2.moments(largest_contour)
	cX = int(M["m10"] / M["m00"])
	cY = int(M["m01"] / M["m00"])
	# draw the contour and center of the shape on the image
	cv2.drawContours(background_frame, [largest_contour], -1, (0, 255, 0), 2)
	cv2.circle(background_frame, (cX, cY), 7, (255, 255, 255), -1)
	cv2.putText(background_frame, "center", (cX - 20, cY - 20),
	cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)


process_images()

cv2.imshow("original", frame_light_transition_candidate)
cv2.waitKey(0)

frame_light_transition = frame_light_transition_candidate

find_object_position(frame_light_transition)

# show the image
cv2.imshow("Image", background_frame)
cv2.waitKey(0)

# release the file pointers
print("[INFO] cleaning up...")
writer.release()
vs.release()