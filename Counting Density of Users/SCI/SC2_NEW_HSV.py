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

        imhsv1 = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
        imhsv2 = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
        HSVDifresult = cv2.cvtColor(Difresult, cv2.COLOR_BGR2HSV)

        h1, s1, v1 = cv2.split(imhsv1)
        h2, s2, v2 = cv2.split(imhsv2)
        h3, s3, v3 = cv2.split(HSVDifresult)

        high, width = h1.shape

        i = 0
        j = 0
        for x in xrange(high):
            for y in range(width):
                i = h1[x, y]
                j = h2[x, y]
                if (i < j):
                    h3[x, y] = 0
                else:
                    h3[x, y] = (i - j)

        i = 0
        j = 0
        for x in xrange(high):
            for y in range(width):
                i = s1[x, y]
                j = s2[x, y]
                if (i < j):
                    s3[x, y] = 0
                else:
                    s3[x, y] = (i - j)

        i = 0
        j = 0
        for x in xrange(high):
            for y in range(width):
                i = v1[x, y]
                j = v2[x, y]
                if (i < j):
                    v3[x, y] = 0
                else:
                    v3[x, y] = (i - j)

        img1 = cv2.merge((h1, s1, v1))
        img2 = cv2.merge((h2, s2, v2))
        Difresult = cv2.merge((h3, s3, v3))

        Difresult = cv2.cvtColor(Difresult, cv2.COLOR_HSV2BGR)
        GrayDifresult = cv2.cvtColor(Difresult, cv2.COLOR_BGR2GRAY)

        #retva, threshold2 = cv2.threshold(GrayDifresult, 125, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        threshold2 = GrayDifresult
        Thresh = 0
        for x in xrange(high):
            for y in range(width):
                Thresh = GrayDifresult[x, y]
                if (Thresh < 10):
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

        # print Dens
        # print i

        #Dens = Dens * 100
        #Dens = Dens / i

        #Number = Dens / 2.677

       ## if (Dens < 2.677):
            ##print Image1, Image2, ',', '%.3f' % Dens, '%', ',', '%d' % Number
            ##Image1 = Image2
        ##if (Dens > 15):
            ##Number = 0
            ##print Image1, Image2, ',', '%.3f' % Dens, '%', ',', '%d' % Number
            ##Image1 = Image2
        ##if (Dens >= 2.677):
            ##if (Dens <= 15):
                ##print Image1, Image2, ',', '%.3f' % Dens, '%', ',', '%d' % Number
        Dens = (Dens * 100.00) / i
        Number = Dens / 2.5

        if (Dens < 2.5):
            print Image1, Image2, ',', '%.3f' % Dens, '%', ',', '%d' % Number
            Image1 = Image2
        if (Dens > 46):
            Number = 0
            print Image1, Image2, ',', '%.3f' % Dens, '%', ',', '%d' % Number
            Image1 = Image2
        if (Dens >= 2.5):
            if (Dens <= 46):
                if (Dens >= 10):
                    Number = Number / 2.5
                print Image1, Image2, ',', '%.3f' % Dens, '%', ',', '%d' % Number
        ##if (Dens >= 2.677):
            ##if (Dens <= 15):
                ##print Image1, Image2, ',', '%.3f' % Dens, '%', ',', '%d' % Number
        #if (Dens >= 20):
            #if (Dens <= 26):
                #print Image1, Image2, ',', '%.3f' % Dens, '%', ',', '%d' % Number
        #if (Dens >= 0):
            #if (Dens <= 1):
                #Number = 0
                #print Image1, Image2, ',', '%.3f' % Dens, '%', ',', '%d' % Number
                #Image1 = Image2
        #if (Dens > 1):
            #if (Dens <= 20):
                #Number = 0
                #print Image1, Image2, ',', '%.3f' % Dens, '%', ',', '%d' % Number
                #Image1 = Image2
        #if (Dens > 26):
            #Number = 0
            #print Image1, Image2, ',', '%.3f' % Dens, '%', ',', '%d' % Number
            #Image1 = Image2
        #zCount = 0

        #print 'x = %d' %xLoop, 'z = %d \n' %zCount
        xLoop += 1
        zCount += 1

    yLoop += 1

cv2.waitKey(0)
cv2.destroyAllWindows()
