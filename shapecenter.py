# import the necessary packages
import argparse
import imutils
import cv2
import os
from PIL import Image
import cv2
from PIL import ImageChops

def press(x,y):
    ix = x+200
    iy = y+1040
    cmd = 'adb shell input tap {x1} {y1} '.format(x1=ix, y1=iy)
    os.system(cmd)

def showimg(img):
    # cv2.namedWindow("image",1)#窗口能变化
    cv2.resizeWindow("image", 10, 10)
    # cv2.resizeWindow("enhanced",100, 100)
    cv2.imshow('image', img)
    k = cv2.waitKey(0)
    if k == 27:  # 如果输入ESC退出
        cv2.destroyAllWindows()

def pull_screenshot(phone=True):
    # Connect to phone
    if phone:
        os.system('adb shell screencap -p /sdcard/findTheDiff.png')
        os.system('adb pull /sdcard/findTheDiff.png .')
    img = cv2.imread('findTheDiff.png')
    # 闯关模式
    # crop_img1=img[165:980,210:1040]#截取范围高度（上：下） 宽度（左：右）
    # crop_img2=img[1025:1840,210:1040]
    # 个人挑战模式 将图片完全对齐避免误差
    # 个人挑战取消右上角透明菜单
    # crop_img1 = img[140:920, 200:1025]  # 截取范围高度（上：下） 宽度（左：右）
    # crop_img2 = img[1040:1820, 200:1025]
    crop_img1 = img[140:920, 200:1025]  # 截取范围高度（上：下） 宽度（左：右）
    crop_img2 = img[1040:1820, 200:1025]
    cv2.imwrite('img1.png', crop_img1)
    cv2.imwrite('img2.png', crop_img2)
    img1 = Image.open('img1.png')
    img2 = Image.open('img2.png')
    # 两张图片的绝对值，相同像素减去
    out = ImageChops.difference(img1, img2)
    # 图片反色，恢复为正常色彩
    out_normal = ImageChops.invert(out)
    out_normal.save('diff.png')
    out_invert = ImageChops.invert(out_normal)
    out_invert.save('nor_inver.png')
    # return out_normal
# construct the argument parse and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required=True,
#                 help="path to the input image")
# args = vars(ap.parse_args())

# load the image, convert it to grayscale, blur it slightly,
# and threshold it
# image = cv2.imread(args["image"])


def main():
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

        # draw the contour and center of the shape on the image 绿色轮廓
        cv2.drawContours(img, [c], -1, (0, 255, 0), 2)
        #画中心点(0, 0, 0)黑色
        cv2.circle(img, (cX, cY), 7, (0, 0, 0), -1)
        # cv2.imshow("Image", img)

        print('center point:',cX,cY)
        # 点击屏幕
        # press(cX,cY)
        #画出轮廓
        # cv2.putText(img, "center", (cX - 20, cY - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        # # show the image
        cv2.imshow("Image", img)
        cv2.waitKey(0)

if __name__ == '__main__':
    pull_screenshot()
    main()


