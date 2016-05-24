import os

import cv2
import numpy as np
from PIL import Image
from tesserwrap import Tesseract
from skimage.measure import compare_ssim as ssim

temp_count = 1
train_box = 0
train_box_logo = 1
temp_img = None


def denoise_info(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    # kernel = np.ones((2, 2), np.uint8)
    # thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
    thresh = gray
    return thresh

def gray_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray


def compare_to_box_info(img):
    global train_box, train_box_logo
    box_serial = get_box_serials()
    path = '../fig_sample/box_info_final/'+box_serial[train_box]+'.'+str(train_box_logo)+'.jpg'
    temp_img = cv2.imread(path)
    if temp_img is not None:
        temp_img = gray_image(temp_img)
        img2 = cv2.resize(temp_img, (30, 30))
        s = ssim(img, img2)
    else:
        s = 0
    return s

def compare_to_last_info(img):
    global temp_img
    if temp_img is not None:
        s = ssim(img, temp_img)
    else:
        s = 0
    temp_img = img
    return s


def resize(image, factor=0.5):
    image = cv2.resize(image, (0, 0), fx=factor, fy=factor)
    return image


def ocr(info):
    cv2.imwrite('../fig/info.jpg', info)
    img = Image.open('../fig/info.jpg')
    tr = Tesseract(datadir='../tessdata', lang='eng')
    text = tr.ocr_image(img)
    print(text)


def save_training_info_image(img, count=1):
    global temp_count, train_box, train_box_logo
    if (count != 1) & (temp_count < count):
        temp_count = count
    s1 = compare_to_last_info(img)
    s2 = compare_to_box_info(img)
    box_serial_list = get_box_serials()
    path = '../info/'+box_serial_list[train_box]

    if (s1 < 0.8) & (temp_count <= 100) & (s2 != 0):
        if not os.path.exists(path):
            os.mkdir(path)
        cv2.imwrite(path+'/'+str(train_box_logo)+'.'+str(temp_count).zfill(3)+'.jpg', img)
        print(str(temp_count)+'   '+str(s2))
        temp_count += 1
    elif (s2 == 0):
        print('No example info images')


def get_keyboard():
    flag = False
    global train_box, train_box_logo, temp_count
    k = cv2.waitKey(10) & 0xFF
    if k == 27:
        flag = True
        return flag
    elif k == ord('b'):
        if train_box <= 3:
            train_box += 1
            train_box_logo = 1
            temp_count = 1
        elif train_box >= 4:
            train_box = 0
    elif k == ord('o'):
        if train_box_logo <= 5:
            train_box_logo += 1
            temp_count = 1
        else:
            train_box_logo = 1
    return flag


def put_text(img):
    global train_box, train_box_logo
    box_serial = get_box_serials()
    string = 'box: ' + box_serial[train_box] + ' orient: ' + str(train_box_logo)
    cv2.putText(img, string, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
    return img


def write_ssim():
    global ssim_list, train_box
    path = '../info/box' + str(train_box)
    with open(path + '/ssim_value.txt', 'w+') as f:
        for i in range(1, len(ssim_list)-1):
            f.writelines(["%s\n" % str(ssim_list[i])])


def get_box_serials():
    path = '../info/info.txt'
    with open(path) as f:
        list1 = f.read()
        line = list1.split('\n')
    return line

def listdir_no_hidden(path):
    list1 = []
    for f in os.listdir(path):
        if not f.startswith('.'):
            list1.append(f)
    return list1