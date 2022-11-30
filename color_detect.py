import cv2
import numpy as np
from exif import Image


def affected_region(img_path):
    result = ''
    color = ''
    img=cv2.imread(img_path)

    hsvFrame = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    kernal = np.ones((5, 5), "uint8")

    # for brown color
    brown_lower = np.array([100, 80, 2], np.uint8)
    brown_upper = np.array([120, 255, 255], np.uint8)
    brown_mask = cv2.inRange(hsvFrame, brown_lower, brown_upper)
    brown_mask = cv2.dilate(brown_mask, kernal)
    # for green color
    green_lower = np.array([25, 52, 72], np.uint8)
    green_upper = np.array([70, 255,255], np.uint8)
    green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)
    green_mask = cv2.dilate(green_mask, kernal)
    # for yellow color
    yellow_lower = np.array([70,50,90], np.uint8)
    yellow_upper = np.array([102,255,255], np.uint8)
    yellow_mask = cv2.inRange(hsvFrame, yellow_lower, yellow_upper)
    yellow_mask = cv2.dilate(yellow_mask, kernal)
   
    def calcPercentage(msk): 
        ''' 
        returns the percentage of color in a binary image 
        ''' 
        height, width = msk.shape[:2] 
        num_pixels = height * width 
        count_brown = cv2.countNonZero(msk) 
        color_prec = (count_brown/num_pixels) * 100 
        color_prec = round(color_prec,2) 
        return color_prec 

    green_perc = calcPercentage(green_mask)
    yellow_perc = calcPercentage(yellow_mask)
    brown_perc = calcPercentage(brown_mask)

    print(green_perc, yellow_perc, brown_perc)
    
    result_green = cv2.bitwise_and(img, img, mask=green_mask)
    result_yellow = cv2.bitwise_and(img, img, mask=yellow_mask)
    result_brown = cv2.bitwise_and(img, img, mask=brown_mask)
    blank_result = ''
    blank_perc = ''
    if green_perc >30:
        color = 'green'
        return result_green, color, green_perc

    elif yellow_perc > 30  and green_perc < 30:
        color = 'yellow'
        return result_yellow, color, yellow_perc

    elif brown_perc >30:
        color = 'brown'
        return result_brown, color, brown_perc
    
    else:
        color = 'unknow'
        return blank_result, color, blank_perc
    
def get_date_taken(filename):
    with open(filename, "rb") as palm_1_file:
        palm_1_image = Image(palm_1_file)
    images = [palm_1_image]
    for index, image in enumerate(images):
        print(f"Date/time taken - Image {index}")
    print("-------------------------")
    try:
        time_stamp = (f"{image.datetime_original}.{image.subsec_time_original} {image.get('offset_time', '')}\n")
    except:
        time_stamp = "no timestamp found"
    return time_stamp

def detect_category(input_file):
    plant_status = ''
    action = ''
    inf_img, color, perc =  affected_region(input_file)
    time_stamp = get_date_taken(input_file)

    if color == 'green':
        plant_status = 'healthy'
        action = "plant status is good and healthy,"
    elif color == "yellow":
        plant_status = 'unhealthy'
        action = "improper watering, need to water regularly,"
    elif color == "brown":
        plant_status = 'deceased'
        action = "plant is deceased less chancess to recover."
    else :
        color = 'unknown'
        plant_status = 'not a plant'
        action = "please try with another image."

    return color, plant_status, action, time_stamp



if __name__ == "__main__":
    pass
    # img_path = r"C:\Users\sarwa\Desktop\image_category\images\1669191739-healthy-plant.jpg"
    # output_name = 'InfraBl.jpg'
    # color, plant_status, action, time_taken =  detect_category(img_path)
   
    # print(color, plant_status, action, time_taken)

 