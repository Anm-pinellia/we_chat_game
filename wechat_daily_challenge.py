import os
from PIL import Image
import cv2
from PIL import ImageChops
import matplotlib.pyplot as plt
import numpy as np

def pull_screenshot(phone=True):
    #Connect to phone
    if phone:
        os.system('adb shell screencap -p /sdcard/findTheDiff.png')
        os.system('adb pull /sdcard/findTheDiff.png .')
    img=cv2.imread('findTheDiff.png')
    # 闯关模式
    # crop_img1=img[165:980,210:1040]#截取范围高度（上：下） 宽度（左：右）
    # crop_img2=img[1025:1840,210:1040]
    #个人挑战模式 将图片完全对齐避免误差
    crop_img1=img[100:920,200:1025]#截取范围高度（上：下） 宽度（左：右）
    crop_img2=img[1000:1820,200:1025]
    cv2.imwrite('img1.png',crop_img1)
    cv2.imwrite('img2.png',crop_img2)
    img1=Image.open('img1.png')
    img2=Image.open('img2.png')
    #两张图片的绝对值，相同像素减去
    out=ImageChops.difference(img1,img2)
    #图片反色，恢复为正常色彩
    out_normal=ImageChops.invert(out)
    out_normal.save('diff.png')
    out_invert=ImageChops.invert(out_normal)
    # out_invert.save('nor_inver.png')
    return out_normal

def on_click(event):
    click_count = 0
    ix,iy=event.xdata,event.ydata
    coords=[(int(ix)+214,int(iy)+168)]#从小方块坐标转换到屏幕坐标
    print('now=',coords)
    click_count+=1
    if click_count>0:
        click_count=0
        press(coords)

def press(coords):
    ix = coords[0][0]
    iy = coords[0][1]
    cmd = 'adb shell input tap {x1} {y1} '.format(x1=ix, y1=iy)
    os.system(cmd)
    

def main():
    while True:
        inp=input('是否更新图片(默认更新,输入n或N不更新)')
        if inp=='n' or inp=='N':
            break
        fig = plt.figure()
        img = np.array(pull_screenshot(False))
        plt.imshow(img, animated=True)
        fig.canvas.mpl_connect('button_press_event',on_click)
        plt.show()
if __name__=="__main__":
    # while True:
    #     pull_screenshot()
    #     a=input('next')
    #     if a=='n':
    #         break
    main()
    





    


