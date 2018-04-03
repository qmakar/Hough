import cv2
import numpy as np

# img = cv2.imread('img/9.png')
img = cv2.imread('img/111.jpg')

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
gray = cv2.bitwise_not(gray)
# gray = copy.deepcopy(img)
ret,gray = cv2.threshold(gray,55,255,cv2.THRESH_BINARY)
cv2.imwrite('gray.jpg', gray)

lines = cv2.HoughLinesP(gray,0.1,np.pi/180/10,20,minLineLength=20,maxLineGap=5)

print len(lines)
print lines
list_lines = []

for i in range(len(lines)):
	for x1,y1,x2,y2 in lines[i]:
		points = [(x1,y1)]
		cv2.line(img,(x1,y1),(x2,y2),(0,0,255),1)

		horizontal_line = abs(x2-x1) > abs(y1-y2) 
		vertical_line = abs(x2-x1) < abs(y1-y2)
		if (horizontal_line == vertical_line):
			continue


		# Find max connectionComponent in one row\col
		# Go down/right
		is_connected = True 
		i = 0
		while(is_connected):
			is_connected = False
			for j in range(-1,2):
				pix = gray[y1+j*horizontal_line+i*vertical_line][x1+i*horizontal_line+j*vertical_line]
				if pix:
					points.append((x1+i*horizontal_line+j*vertical_line,y1+j*horizontal_line+i*vertical_line))
					is_connected = True
					break

			i += 1
			if (not is_connected):
				break

		# Go up/left
		is_connected = True
		i = -1
		while(is_connected):
			is_connected = False
			for j in range(-1,2):
				pix = gray[y1+j*horizontal_line+i*vertical_line][x1+i*horizontal_line+j*vertical_line]
				if pix:
					points.insert(0,(x1+i*horizontal_line+j*vertical_line,y1+j*horizontal_line+i*vertical_line))
					is_connected = True
					break

			i -= 1
			if (not is_connected):
				break

		if (len(points)) > 100: # We want long lines
			list_lines.append(points)

print len(list_lines)

for lines in list_lines:
	cv2.line(img,lines[0],lines[-1],(0,255,0),1)

cv2.imwrite('gray_lines.jpg', img) # image with GREEN lines where are GOOD lines and RED -- ALL founded lines



for line in list_lines:
	cv2.line(gray,line[0],line[-1],(0),3) # draw black lines where they are white (delete line)
	
cv2.imwrite('gray_res.jpg', gray)




# dilated = cv2.dilate(img1, np.ones((3, 1)))
# img1 = cv2.bitwise_not(dilated)

# cv2.imwrite('dilated.jpg', img1)
# img_line = np.ones(gray.shape,np.uint8)*0    #LineIterator
# cv2.line(img_line,(x1,y1),(x2,y2),(255,255,255),1)
# # pixelpoints = np.transpose(np.nonzero(img_line))
# pixelpoints = cv2.findNonZero(img_line)
		



