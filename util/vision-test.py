# Path hack.
import sys, os
sys.path.insert(0, os.path.abspath('..'))


# Setup:
#
# Disable "White Balance Temperature, Auto"
# (Default value: 1)
# $ v4l2-ctl -d /dev/video2 --set-ctrl=white_balance_temperature_auto=0
# To confirm:
# $ v4l2-ctl -d /dev/video2 --get-ctrl=white_balance_temperature_auto
# white_balance_temperature_auto: 0

#
# Change "Exposure, Auto" to "Manual Mode"
# (Default value: 3)
# $ v4l2-ctl -d /dev/video2 --set-ctrl=exposure_auto=1
# To confirm:
# $ v4l2-ctl -d /dev/video2 --get-ctrl=exposure_auto
# exposure_auto: 1

import cv2
import numpy as np
from skimage import exposure
from squarish import squarish
import time

def drawCorners(img, points):
    p1, p2, p3, p4 = map(tuple, points)

    # Draw outline
    pts = np.array([p1, p2, p3, p4], np.int32)
    pts = pts.reshape((-1,1,2))
    cv2.polylines(img,[pts],True,(0,255,0), 2)

    # Draw corners
    cv2.circle(img, p1, 7, (255, 0, 0), -1)
    cv2.circle(img, p2, 7, (255, 255, 255), -1)
    cv2.circle(img, p3, 7, (255, 255, 255), -1)
    cv2.circle(img, p4, 7, (255, 255, 255), -1)


def drawLabel(img, contour, text='center'):
    #print "Area: %s" % cv2.contourArea(contour)
    #print "Perimeter: %s" % cv2.arcLength(contour, True)
    perimeter = cv2.arcLength(contour, True)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_size = 0.5
    if perimeter >= 800:
        font_size = 1.25
    elif perimeter >= 500:
        font_size = .5
    #else:
    #    font_size = .3

    # Get text boundary
    textsize = cv2.getTextSize(text, font, font_size, 2)[0]

    # Compute the center of the contour
    M = cv2.moments(contour)
    try:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        textX = int(cX - (textsize[0] / 2))
        textY = int(cY + 10)

        cv2.putText(
            img,
            text,
            (textX, textY),
            cv2.FONT_HERSHEY_SIMPLEX,
            font_size,
            (255, 255, 255),
            2)

    except ZeroDivisionError:
        pass

def getRect(curve):
    # We need to determine correct order of points
    # (top-left, top-right, bottom-right, and bottom-left)
    #curve = approx
    pts = curve.reshape(4, 2)
    rect = np.zeros((4, 2), dtype = "float32")

    # The top-left point has the smallest sum whereas the
    # bottom-right has the largest sum
    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # Compute the difference between the points -- the top-right
    # will have the minumum difference and the bottom-left will
    # have the maximum difference
    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect


if __name__ == '__main__':
    cap = cv2.VideoCapture(2)
    if not cap.isOpened():
        print("ERROR: Can't find camera")
    else:
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        cv2.namedWindow('Tapster Demo', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Tapster Demo', 1000, 1700)

        timer_start = time.perf_counter()
        done = False
        while(done == False):
            # Capture frame-by-frame
            ret, frame = cap.read()
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            original_frame = frame.copy()

            # Make it easier to process
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            ret,thresh = cv2.threshold(blurred,90,255,cv2.THRESH_BINARY_INV)
            edged = cv2.Canny(thresh, 30, 200)

            contours = cv2.findContours(edged, cv2.RETR_EXTERNAL,
        	    cv2.CHAIN_APPROX_SIMPLE)
            contours = contours[0]

            squares = []
            squares_contours = []
            for cnt in contours:
                approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)

                if len(approx) == 4:

                    # Ignore small features
                    area = cv2.contourArea(cnt)
                    if area <= 100:
                        continue

                    rect = getRect(approx)

                    # Skip to next contour if not squarish
                    if not squarish(rect):
                        continue

                    # Deskew the square
                    SIZE = 200
                    refPoints = np.float32([[0,0],[SIZE,0],[SIZE,SIZE],[0,SIZE]])
                    transformation = cv2.getPerspectiveTransform(rect, refPoints)
                    dst = cv2.warpPerspective(original_frame,transformation,(SIZE,SIZE))
                    squares.append(dst)
                    squares_contours.append(cnt)

                    drawCorners(frame, rect)


            #print ("Number of shapes: %s" % len(squares))
            for i, square in enumerate(squares):
                squares[i] = exposure.rescale_intensity(squares[i], out_range = (0, 255))

                # Find shape within contour
                squares_img_float32 = np.float32(squares[i])
                shape_gray = cv2.cvtColor(squares_img_float32, cv2.COLOR_BGR2GRAY)
                #shape = exposure.rescale_intensity(shape_gray, out_range = (0, 255))
                shape = cv2.GaussianBlur(shape_gray, (5, 5), 0)
                ret,shape = cv2.threshold(shape, 90, 255, cv2.THRESH_BINARY_INV)

                shape = shape.astype(np.uint8)
                shape_contours = cv2.findContours(shape, cv2.RETR_LIST,
                	    cv2.CHAIN_APPROX_SIMPLE)
                shape_contours = shape_contours[0]
                #print ("  Sub-shapes: %s" % len(shape_contours))
                for shape_contour in shape_contours:
                    shape_approx = cv2.approxPolyDP(shape_contour,0.2*cv2.arcLength(shape_contour,True),True)
                    #print ("  Number of sides: %s" % len(shape_approx))

                    # Look for Triangle
                    if len(shape_approx) == 3:
                        timer_stop = time.perf_counter()
                        #print ("  Triangle")
                        print("  Found image!")
                        drawLabel(frame, squares_contours[i], 'OK!')
                        cv2.drawContours(squares[i],[shape_contour],0,(0,255,0),-1)
                        done = True
                        print("  Elapsed time:", timer_stop - timer_start)
                        break


            # Display the resulting frame
            cv2.imshow('Tapster Demo',frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    while(True):
        # Display the resulting frame
        cv2.imshow('Tapster Demo',frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    cap.release()
    cv2.destroyAllWindows()

