import cv2
import time

Image1 = "Image1.jpg"

print 'Image' ,',' ,'Density' ,',' ,'Number'

xLoop = 1
yLoop = 1
zCount = 0
while yLoop < 400:
    while xLoop < 400:
        Image2 = "Image"
        Image2 += '%d' % xLoop
        Image2 += ".jpg"
        #time.sleep(15)

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
        #cv2.imshow('Differnt_RGB', Difresult)

        GrayDifresult = cv2.cvtColor(Difresult, cv2.COLOR_RGB2GRAY)
        #cv2.imshow('Differnt_GrayScale', GrayDifresult)

        #retva, threshold2 = cv2.threshold(GrayDifresult, 125, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        #cv2.imshow('Differnt_BlackAndWhite', threshold2)

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

        #print Dens
        #print i

        Dens = (Dens * 100.00) / i
        Number = Dens / 2

        #if (zCount > 10):
        if (Dens <2):
            print Image1, Image2, ',', '%.3f' % Dens, '%', ',', '%d' % Number
            Image1 = Image2
        if (Dens > 30):
            Number = 0
            print Image1, Image2, ',', '%.3f' % Dens, '%', ',', '%d' % Number
            Image1 = Image2
        if (Dens % 2 > 0):
            Dens2 = Dens + 1
            Number = Dens2 / 2
        if (Dens >= 2):
            if (Dens <= 30):
                if (Dens >= 10):
                    Number = Number / 2
                print Image1, Image2, ',', '%.3f' % Dens, '%', ',', '%d' % Number
        #zCount = 0

        #print 'x = %d' %xLoop, 'z = %d \n' %zCount
        xLoop += 1
        zCount += 1

    yLoop += 1

cv2.waitKey(0)
cv2.destroyAllWindows()
