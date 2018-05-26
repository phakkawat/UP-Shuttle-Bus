import cv2
import microgear.client as microgear
import logging
import time

#cap = cv2.VideoCapture(0)

gearkey = "qreO9hEcW1LVV1e"
gearsecret =  "Y1UslNEFEbt1UhpT2AtR46n7L"
appid = "PYthontest"
microgear.create(gearkey, gearsecret, appid, {'debugmode': True})

def connection():
    logging.info("Now I am connected with netpie")

def subscription(topic, message):
    logging.info(topic + " " + message)

def disconnect():
    logging.info("disconnected")

microgear.setalias("StatusMonitorEN")
microgear.on_connect = connection
microgear.on_message = subscription
microgear.on_disconnect = disconnect
microgear.subscribe("/Dens/1")
microgear.connect()

Image1 = "Image1.jpg"

print 'Image' ,',' 'Number'

xLoop = 1
yLoop = 1
zCount = 0
while yLoop < 400:
    while xLoop < 400:

        Image2 = "Image"
        Image2 += '%d' % xLoop
        Image2 += '.jpg'
        #rpg, img = cap.read()
        #cv2.imwrite(Image2, img)

        img1 = cv2.imread(Image1, cv2.IMREAD_COLOR)
        img1 = cv2.resize(img1, (400, 240), interpolation=cv2.INTER_CUBIC)
        img2 = cv2.imread(Image2, cv2.IMREAD_COLOR)
        img2 = cv2.resize(img2, (400, 240), interpolation=cv2.INTER_CUBIC)
        Difresult = cv2.imread('white1.jpg', cv2.IMREAD_COLOR)
        Difresult = cv2.resize(Difresult, (400, 240), interpolation=cv2.INTER_CUBIC)

        B1, G1, R1 = cv2.split(img1)
        B2, G2, R2 = cv2.split(img2)
        B3, G3, R3 = cv2.split(Difresult)

        high, width = R1.shape

        i = 0
        j = 0
        for x in xrange(high):
            for y in range(width):
                i = R1[x, y]
                j = R2[x, y]
                if (i < j):
                    R3[x, y] = (j - i)
                else:
                    R3[x, y] = (i - j)

        i = 0
        j = 0
        for x in xrange(high):
            for y in range(width):
                i = G1[x, y]
                j = G2[x, y]
                if (i < j):
                    G3[x, y] = (j - i)
                else:
                    G3[x, y] = (i - j)

        i = 0
        j = 0
        for x in xrange(high):
            for y in range(width):
                i = B1[x, y]
                j = B2[x, y]
                if (i < j):
                    B3[x, y] = (j - i)
                else:
                    B3[x, y] = (i - j)

        Difresult = cv2.merge((B3, G3, R3))

        GrayDifresult = cv2.cvtColor(Difresult, cv2.COLOR_RGB2GRAY)

        threshold2 = GrayDifresult
        Thresh = 0
        for x in xrange(high):
            for y in range(width):
                Thresh = GrayDifresult[x, y]
                if (Thresh < 40):
                    threshold2[x, y] = 0
                else:
                    threshold2[x, y] = 255

        high, width = threshold2.shape

        i = 0
        Dens = 0
        for x in xrange(high):
            for y in range(width):
                Dens = Dens + threshold2[x, y]
        i = high * width
        Dens = Dens / 255

        Dens = (Dens * 100.00) / i
        Number = Dens / 2

        if (Dens % 2 > 0):
            Dens2 = Dens + 1
            NumberN = Dens2 / 2
            if (Dens < 2):
                NumberN = 0
                print Image1, Image2, ',', '%d' % NumberN
                Image1 = Image2
            if (Dens > 50):
                NumberN = 0
                print Image1, Image2, ',', '%d' % NumberN
                Image1 = Image2
        else :
            if (Dens < 2):
                NumberN = 0
                print Image1, Image2, ',',  '%d' % NumberN
                Image1 = Image2
            if (Dens > 50):
                NumberN = 0
                print Image1, Image2, ',',',', '%d' % NumberN
                Image1 = Image2
        if (Dens >= 2):
            if (Dens <= 50):
                if (Dens >= 20):
                    NumberN = Number / 2
                print Image1, Image2, ',', ',', '%d' % NumberN
        if (NumberN < 1):
            microgear.chat("HTMLMonitorEN", "/0")
            print 0
        if (NumberN >= 1):
            if (NumberN < 4):
                microgear.chat("HTMLMonitorEN", "/1")
                print 1
        if (NumberN >= 4):
            if (NumberN < 8):
                microgear.chat("HTMLMonitorEN", "/2")
                print 2
        if (NumberN >= 8):
            microgear.chat("HTMLMonitorEN", "/3")
            print 3
        xLoop += 1
        zCount += 1

        time.sleep(15)

    yLoop += 1

cap.release()
cv2.waitKey(0)
cv2.destroyAllWindows()