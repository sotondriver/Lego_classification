import cv2
from PIL import Image
from tesserwrap import Tesseract
from Lego.Lego import Lego
from Lego.imgPreprocessing import LogoAffinePos


<<<<<<< HEAD
VWIDTH = 640
VHIGH = 480
cap = cv2.VideoCapture(0)
ret = cap.set(3, VWIDTH)
ret = cap.set(4, VHIGH)

while 1:
    _, frame = cap.read()

    imgH,imgW, _ = frame.shape

    l = Lego(frame)
    logo_box = l.get_logo_box()
    info = l.get_information_part()

    cv2.drawContours(frame, [logo_box], -1, (0, 255, 0), 2)

    if l._has_information:
        cv2.imshow('info', info)
        cv2.imwrite('info.jpg',info)
        img = Image.open('info.jpg')
        tr = Tesseract(datadir='../tessdata', lang='eng')
        text = tr.ocr_image(img)
        print(text)
    # if l._has_rotated_image:
    #     img = l._rotated_image
    #     img[l._logo_center_y:l._logo_center_y+3, l._logo_center_x:l._logo_center_x+3, :] = [255, 255, 255]
    #     cv2.imshow('rotate', img)
    # if l._has_potential_logo:
    #     cv2.imshow('logo', l.get_logo_image())

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()
=======
def resize(image, factor=0.5):
    image = cv2.resize(image, (0, 0), fx=factor, fy=factor)
    return image


def ocr(info):
    info = resize(info, 0.5)
    cv2.imshow('info', info)
    cv2.imwrite('info.jpg', info)
    img = Image.open('info.jpg')
    tr = Tesseract(datadir='../tessdata', lang='eng')
    text = tr.ocr_image(img)
    return text


def initial_lyu_class():
    imgPATH = '../fig/'
    logoTp = cv2.imread(imgPATH + 'purelogo256.png')
    lyu = LogoAffinePos(logoTp, featureObject=cv2.AKAZE_create(), matcherObject=cv2.BFMatcher(),
                        matchMethod='knnMatch')
    return lyu

def initial_li_class(image):
     li = Lego(image)
     return li

def get_affined_image(lyu, image):
    logoContourPts, cPts, affinedcPts, affinedImg, rtnFlag = lyu.rcvAffinedAll(image)
    cv2.drawContours(image, [logoContourPts], -1, (0, 255, 0), 2)
    if (rtnFlag is True):
        affined = affinedImg
        affined = resize(affined, 0.3)
        cv2.imshow('affined', affined)
        cv2.moveWindow('affined',int(1280*0.35),int(720*0.35))

def get_rotated_image(li):
    if li._has_rotated_image:
        rotated = li.get_rotated_image()
        rotated = resize(rotated, 0.3)
        cv2.imshow('rotate', rotated)
        cv2.moveWindow('rotate',int(1280*0.35),0)


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    lyu = initial_lyu_class()
    while 1:
        _, frame = cap.read()

        li = initial_li_class(frame.copy())
        get_rotated_image(li)
        # info = li.get_information_part()
        # text = ocr(info)
        try:
            get_affined_image(lyu, frame.copy())
        except:
            pass

        logo_box = li.get_logo_box()
        cv2.drawContours(frame, [logo_box], -1, (0, 255, 0), 2)
        frame = resize(frame, 0.3)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
>>>>>>> dev
