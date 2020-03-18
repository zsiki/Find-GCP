import cv2

aruco = cv2.aruco

d = aruco.Dictionary_create(32, 3)  # aruco 3x3 dictionary
for i in range(32):
    marker = aruco.drawMarker(d, i, 256)  # create marker
    # create image from marker
    cv2.imwrite('dict_3x3/3x3_{}.png'.format(i), marker)
