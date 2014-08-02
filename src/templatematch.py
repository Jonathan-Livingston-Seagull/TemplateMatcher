'''
Created on Aug 1, 2014

@author: seagull
'''


import numpy as np
import argparse
import cv2


def onmouse(event, x, y, flags, param):
    '''
    call back method to be called whenever left mouse click occurs. Extract the region of interest in first image 
    find matching pattern in the second image 
    '''    
    if event == cv2.EVENT_LBUTTONUP:
        #Exception case check
        if x > w1 or y > h1:
            print('please select region in the first image')
        else:    
            region_pixel_w1 = 10
            region_pixel_h1 = 10
            if x + region_pixel_w1 > w1:
                region_pixel_w1 = w1 - x
            if y + region_pixel_h1 > h1:
                region_pixel_h1 = h1- y
            region_pixel_w2 = 10
            region_pixel_h2 = 10
            if x - region_pixel_w2 < 0:
                region_pixel_w2 = x
            if y - region_pixel_h2 < 0:
                region_pixel_h2 = y
            
            # extract region of interest    
            template = combined[y-region_pixel_h2:y+region_pixel_h1,x-region_pixel_w2:x+region_pixel_w1]
            w, h = template.shape[::-1]
            method = cv2.TM_CCORR_NORMED
            # match the template
            res = cv2.matchTemplate(second,template,method)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            
            # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
            if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                top_left = min_loc
            else:
                top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)
            
            cv2.rectangle(combined,(top_left[0]+w1,top_left[1]), (bottom_right[0]+w1,bottom_right[1]), 255, 2)
            cv2.imshow('combined',combined)
            cv2.waitKey(0)
            


if __name__ == '__main__':
    

    parser = argparse.ArgumentParser(description='Find matching pattern between two images on mouse click')
    
    
    parser.add_argument('-p1','--path1',required=True,
                        help='Full path of image 1 ')
    
    parser.add_argument('-p2','--path2',required=True,
                        help='Full path of image 2 ')
     
    args = parser.parse_args()
    
    img_path1 = args.path1
    img_path2 = args.path2  

    # read two images              
    first = cv2.imread(img_path1,0)
    first = cv2.resize(first,(500,300)) 
    second = cv2.imread(img_path2,0)
    second = cv2.resize(second,(500,300))
     
    h1, w1 = first.shape[:2]
    h2, w2 = second.shape[:2]
    
    # combine two images to show them side by side
    combined = np.zeros((max(h1, h2), w1+w2), np.uint8)
    combined[:h1, :w1] = first
    combined[:h2, w1:w1+w2] = second
       
    cv2.namedWindow("combined",1)
    cv2.setMouseCallback("combined", onmouse)
    cv2.imshow('combined',combined)
    if (cv2.waitKey() & 255) == 27:
        cv2.destroyAllWindows()

