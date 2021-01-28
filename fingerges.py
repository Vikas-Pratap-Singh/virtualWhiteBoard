import numpy as np
import cv2
from collections import deque


# Define the upper and lower boundaries for a color to be considered "Blue"
blueLower = np.array([100, 60, 60])
blueUpper = np.array([140, 255, 255])

# Define a 5x5 kernel for erosion and dilation
kernel = np.ones((5, 5), np.uint8)

# Setup deques to store separate colors in separate arrays
redpoints = [deque(maxlen=512)]
yellowpoints = [deque(maxlen=512)]
greenpoints = [deque(maxlen=512)]
bluepoints = [deque(maxlen=512)]

greenindex = 0
redindex = 0
yellowindex = 0

blueindex = 0

colors = [(0, 0, 255), (0, 255, 255), (0, 255, 0),(255, 0, 0)]
colorIndex = 0

# Setup the Paint interface
VirtualWhiteBoard = np.zeros((485,636,3)) + 255
VirtualWhiteBoard= cv2.circle(VirtualWhiteBoard, (120,450), 30, (0,0,0), 2)
VirtualWhiteBoard = cv2.circle(VirtualWhiteBoard, (200,450),30, colors[0], -1)
VirtualWhiteBoard = cv2.circle(VirtualWhiteBoard, (280,450), 30, colors[1], -1)
VirtualWhiteBoard = cv2.circle(VirtualWhiteBoard, (360,450),30, colors[2], -1)
VirtualWhiteBoard = cv2.circle(VirtualWhiteBoard, (440,450), 30,colors[3], -1)
cv2.putText(VirtualWhiteBoard, "CLEAR", (100, 455), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1, cv2.LINE_AA)
cv2.putText(VirtualWhiteBoard, "RED", (183, 455), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
cv2.putText(VirtualWhiteBoard, "YELLOW", (260, 455), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
cv2.putText(VirtualWhiteBoard, "GREEN", (340, 455), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
cv2.putText(VirtualWhiteBoard, "BLUE", (420, 455), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (150,150,150), 2, cv2.LINE_AA)
cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)

# Load the video
camera = cv2.VideoCapture(0)

# Keep looping
while True:
    # Grab the current paintWindow
    (grabbed, Tracking) = camera.read()
    # Check to see if we have reached the end of the video
    if not grabbed:
        break
    Tracking = cv2.flip(Tracking, 1)
    hsv = cv2.cvtColor(Tracking, cv2.COLOR_BGR2HSV)

    # Add the coloring options to the Tracking
    Tracking = cv2.circle(Tracking, (120,450), 30, (122,122,122), -1)
    Tracking = cv2.circle(Tracking, (200,450),30, colors[0], -1)
    Tracking = cv2.circle(Tracking, (280,450), 30, colors[1], -1)
    Tracking = cv2.circle(Tracking, (360, 450),30, colors[2], -1)
    Tracking = cv2.circle(Tracking, (440,450), 30, colors[3], -1)

    cv2.putText(Tracking, "CLEAR", (100,455), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(Tracking, "RED", (183, 455), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(Tracking, "YELLOW", (260, 455), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(Tracking, "GREEN", (340, 455), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(Tracking, "BLUE", (420, 455), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (150,150,150), 1, cv2.LINE_AA)



    # Determine which pixels fall within the blue boundaries and then blur the binary image
    blueMask = cv2.inRange(hsv, blueLower, blueUpper)
    blueMask = cv2.erode(blueMask, kernel, iterations=2)
    blueMask = cv2.morphologyEx(blueMask, cv2.MORPH_OPEN, kernel)
    blueMask = cv2.dilate(blueMask, kernel, iterations=1)

    # Find contours in the image
    cnts, _ = cv2.findContours(blueMask.copy(), cv2.RETR_EXTERNAL,
    	cv2.CHAIN_APPROX_SIMPLE)
    center = None

    # Check to see if any contours were found
    if len(cnts) > 0:
    	# Sort the contours and find the largest one -- we
    	# will assume this contour correspondes to the area of the bottle cap
        cnt = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
        # Get the radius of the enclosing circle around the found contour
        ((x, y), radius) = cv2.minEnclosingCircle(cnt)
        # Draw the circle around the contour
        cv2.circle(Tracking, (int(x), int(y)), int(radius), (0, 255, 255), 2)
        # Get the moments to calculate the center of the contour (in this case Circle)
        M = cv2.moments(cnt)
        center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

        if center[1]>410:
            if 90 <= center[0] <= 150: # Clear All
                redpoints = [deque(maxlen=512)]
                yellowpoints = [deque(maxlen=512)]
                greenpoints = [deque(maxlen=512)]
                bluepoints = [deque(maxlen=512)]


                redindex = 0
                yellowindex = 0
                greenindex = 0
                blueindex = 0


                VirtualWhiteBoard[:412,:,:] = 255

            elif 170 <= center[0] <= 230:
                    colorIndex = 0 # Blue
            elif 250 <= center[0] <= 310:
                    colorIndex = 1 # Green
            elif 330 <= center[0] <= 390:
                    colorIndex = 2 # Red
            elif 410 <= center[0] <= 470:
                    colorIndex = 3 # Yellow

        else :
            if colorIndex == 0:
                redpoints[redindex].appendleft(center)
            elif colorIndex == 1:
                yellowpoints[yellowindex].appendleft(center)
            elif colorIndex == 2:
                greenpoints[greenindex].appendleft(center)
            elif colorIndex == 3:
                bluepoints[blueindex].appendleft(center)

    # Append the next deque when no contours are detected (i.e., bottle cap reversed)
    else:
        redpoints.append(deque(maxlen=512))
        redindex += 1
        yellowpoints.append(deque(maxlen=512))
        yellowindex += 1
        greenpoints.append(deque(maxlen=512))
        greenindex += 1
        bluepoints.append(deque(maxlen=512))
        blueindex += 1

    # Draw lines of all the colors (Blue, Green, Red and Yellow)
    points = [redpoints, yellowpoints, greenpoints, bluepoints]
    for i in range(len(points)):
        for j in range(len(points[i])):
            for k in range(1, len(points[i][j])):
                if points[i][j][k - 1] is None or points[i][j][k] is None:
                    continue
                cv2.line(Tracking, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                cv2.line(VirtualWhiteBoard, points[i][j][k - 1], points[i][j][k], colors[i], 2)

    # Show the Tracking and the VirtualWhiteBoard image
    cv2.imshow("Tracking", Tracking)
    cv2.imshow("Virtual White Board", VirtualWhiteBoard)

	# If the 'q' key is pressed, stop the loop
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
