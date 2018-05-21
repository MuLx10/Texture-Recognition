import numpy as np
import cv2
def getSobel (channel):

    sobelx = cv2.Sobel(channel, cv2.CV_16S, 1, 0, borderType=cv2.BORDER_REPLICATE)
    sobely = cv2.Sobel(channel, cv2.CV_16S, 0, 1, borderType=cv2.BORDER_REPLICATE)
    sobel = np.hypot(sobelx, sobely)

    return sobel;

def findSignificantContours (img, sobel_8u):
    #image= cv2.findContours(sobel_8u, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #print(len(image))
    try:
        _,contours, heirarchy = cv2.findContours(sobel_8u, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    except:
        contours, heirarchy = cv2.findContours(sobel_8u, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Find level 1 contours
    level1 = []
    for i, tupl in enumerate(heirarchy[0]):
        # Each array is in format (Next, Prev, First child, Parent)
        # Filter the ones without parent
        if tupl[3] == -1:
            tupl = np.insert(tupl, 0, [i])
            level1.append(tupl)

    # From among them, find the contours with large surface area.
    significant = []
    tooSmall = sobel_8u.size * 5 / 100 # If contour isn't covering 5% of total area of image then it probably is too small
    for tupl in level1:
        contour = contours[tupl[0]];
        area = cv2.contourArea(contour)
        if area > tooSmall:
            cv2.drawContours(img, [contour], 0, (0,255,0),2)
            significant.append([contour, area])

    significant.sort(key=lambda x: x[1])
    return [x[0] for x in significant];

def segment (path):
    image = cv2.imread(path)
    img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    blurred = cv2.GaussianBlur(img, (5, 5), 0) # Remove noise

    # Edge operator
    sobel = np.max( np.array([ getSobel(blurred[:,:, 0]), getSobel(blurred[:,:, 1]), getSobel(blurred[:,:, 2]) ]), axis=0 )

    # Noise reduction trick, from http://sourceforge.net/p/octave/image/ci/default/tree/inst/edge.m#l182
    mean = np.mean(sobel)

    # Zero any values less than mean. This reduces a lot of noise.
    sobel[sobel <= mean] = 0;
    sobel[sobel > 255] = 255;

    # cv2.imwrite('edge.jpg', sobel);

    sobel_8u = np.asarray(sobel, np.uint8)

    # Find contours
    img2 = img.copy()
    significant = findSignificantContours(img, sobel_8u)

    # Mask
    mask = sobel.copy()
    mask[mask > 0] = 0
    cv2.fillPoly(mask, significant, 255)
    # Invert mask
    mask = np.logical_not(mask)

    #Finally remove the background

    # fname = path.split('/')[-1]
    bgr = cv2.cvtColor(img2, cv2.COLOR_HSV2BGR)
    bgr[mask] = 255;
    print("bgr done")
    cv2.imwrite(path, bgr);
    return bgr
    # print (path)
if __name__ == '__main__':
    import sys
    name = sys.argv[1]
    # print("in Bg_removal")
    # print(name)
    # image = cv2.imread(name)
    img = segment(name)
    cv2.imwrite(name.split('.')[0]+'_g_.jpg', img);
    # print("out Bg_removal")
