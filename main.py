################################################
# Name: Sadiye Ceran                           #
# PROJECT: SODA CAP DETECTION                  #
################################################


from detection import detection
from utils import file_operation
import cv2

  

config_file_name = "config.conf"
image_file_type = "png"

if __name__ == "__main__":

    print("Detection is start...")

    version, debug, dataset_path, output_path = file_operation.read_config_file(config_file_name)
  
    image_file_names = file_operation.get_all_file_names_in_folder(dataset_path, image_file_type)

    no = 1
    for data in image_file_names:
        
        print("Processing image is: [", data, "]") 

        img = cv2.imread(data,1)

        image = detection.img_resize(img)
        src = image.copy()
        #cv2.imshow("original", image)

        blur = detection.gray_blur(image) 
        #cv2.imshow("blurred image", blur)
 
        edge = detection.autoCanny(blur) 
        #cv2.imshow("edge detection", edge)

        labeled_img = detection.morphological_operations(edge)
        #cv2.imshow("labelled", labeled_img)

        fill = detection.flood_fill(labeled_img)

        detected_img = detection.hough_circle(fill, src) 

        output = output_path + str(no) + "." + image_file_type
        
        print("Detected image", no, "is saving...")
        cv2.imwrite(output, detected_img)

        cv2.waitKey(0)
        no += 1   
    
    print("Detection is done.")
