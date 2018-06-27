# import the necessary packages
import argparse
import imutils
import cv2

def showimg(img):
    # cv2.namedWindow("image",1)#窗口能变化
    cv2.resizeWindow("image", 10, 10)
    # cv2.resizeWindow("enhanced",100, 100)
    cv2.imshow('image', img)
    k = cv2.waitKey(0)
    if k == 27:  # 如果输入ESC退出
        cv2.destroyAllWindows()


# construct the argument parse and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required=True,
#                 help="path to the input image")
# args = vars(ap.parse_args())

# load the image, convert it to grayscale, blur it slightly,
# and threshold it
# image = cv2.imread(args["image"])

#load the image
img = cv2.imread('diff.png')
#convert it to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# showimg(gray)


#blur it slightly 模糊处理
blurred = cv2.GaussianBlur(gray, (19,19), 0)
#threshold 二值化处理
thresh = cv2.threshold(blurred, 250, 255, cv2.THRESH_BINARY_INV)[1]
#将阈值设置为250，阈值类型为cv2.THRESH_BINARY_inv（黑白色反转） ，则灰度在大于50的像素其值将设置为255，其它像素设置为0
#show it
# out=cv2.THRESH_BINARY_INV(thresh)
# showimg(thresh)


# find contours in the thresholded image
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
# loop over the contours
for c in cnts:
    # compute the center of the contour
    M = cv2.moments(c)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    # draw the contour and center of the shape on the image
    cv2.drawContours(img, [c], -1, (0, 255, 0), 2)
    #画中心点
    cv2.circle(img, (cX, cY), 7, (0, 0, 0), -1)
    #画轮廓
    cv2.putText(img, "center", (cX - 20, cY - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

    # show the image
    cv2.imshow("Image", img)
    cv2.waitKey(0)