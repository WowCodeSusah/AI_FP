# ------ File / Folder Functions ------ #
# Get all the files within the directory
def getAllFiles(dir):
    import os
    # Get the list of all files and directories
    dir_list = os.listdir(dir)
    # Returns all files
    return dir_list

# Create the folder for the input from videos
import os
def create_folder(folder_location, foldername):
    full_location = folder_location + '/' + foldername
    try: 
        if not os.path.exists(full_location): 
            os.makedirs(full_location) 
    except OSError:
        print('Error: Creating directory') 
    
    return full_location

# Delete all items in input and output files
def delete_all():
    folder_input = getAllFiles('input')
    folder_output = getAllFiles('output')
    for input_folder_name in folder_input:
        input_folder = getAllFiles('input/' + input_folder_name)
        for input_file in input_folder:
            os.remove('input/'+ input_folder_name + '/' + input_file)
        os.rmdir('input/' + input_folder_name)
    for output_folder_name in folder_output:
        output_folder = getAllFiles( 'output/' + output_folder_name)
        for output_file in output_folder:
            os.remove('output/' + output_folder_name + '/' + output_file)
        os.rmdir('output/' + output_folder_name)

# ------ Video Functions ------ #
# Extracting frames from videos (For videos with 3s duration and 30 fps)
import cv2
def frameExtraction(file_Location, output_location , frame_rate = 10):
    video = cv2.VideoCapture(file_Location)
    
    currentframe = 0
    increaseFrameRate = 30 / frame_rate

    while(True):  
        ret,frame = video.read() 
        if ret: 
            if currentframe % increaseFrameRate == 0 or currentframe == 0:
                name = './'+ output_location +'/frame' + str(currentframe) + '.jpg'
                print ('Creating...' + name) 
                cv2.imwrite(name, frame)  
            currentframe += 1
        else: 
            break

    video.release() 
    cv2.destroyAllWindows() 

# ------ CSV Functions ------ #
# [id = int, video_name = string, frame_name = string, body_data = body data, shot = boolean, injury / defects = boolean]
# body_data = ?

# Create data with csv files
import csv
def create_csv(csvName):
    try:
        csv_path = str(csvName) + '.csv'
        with open(csv_path, mode='w', newline='') as file:
            writer = csv.writer(file)
    except:
        print('Create CSV Error')
    
# Append New Data to csv
def append_csv(csvFile, data):
    field_names = ['folderName', 'fileName'
                   ,'NOSE_x', 'NOSE_y', 'NOSE_v'
                   ,'LEFT_EYE_INNER_x', 'LEFT_EYE_INNER_y', 'LEFT_EYE_INNER_v'
                   ,'LEFT_EYE_x', 'LEFT_EYE_y','LEFT_EYE_v'
                   ,'LEFT_EYE_OUTER_x', 'LEFT_EYE_OUTER_y', 'LEFT_EYE_OUTER_v'
                   ,'RIGHT_EYE_INNER_x', 'RIGHT_EYE_INNER_y', 'RIGHT_EYE_INNER_v' 
                   ,'RIGHT_EYE_x', 'RIGHT_EYE_y', 'RIGHT_EYE_v'
                   ,'RIGHT_EYE_OUTER_x', 'RIGHT_EYE_OUTER_y', 'RIGHT_EYE_OUTER_v'
                   ,'LEFT_EAR_x', 'LEFT_EAR_y','LEFT_EAR_v'
                   ,'RIGHT_EAR_x', 'RIGHT_EAR_y', 'RIGHT_EAR_v'
                   ,'MOUTH_LEFT_x', 'MOUTH_LEFT_y', 'MOUTH_LEFT_v'
                   ,'MOUTH_RIGHT_x', 'MOUTH_RIGHT_y','MOUTH_RIGHT_v'
                   ,'LEFT_SHOULDER_x', 'LEFT_SHOULDER_y', 'LEFT_SHOULDER_v'
                   ,'RIGHT_SHOULDER_x', 'RIGHT_SHOULDER_y', 'RIGHT_SHOULDER_v'
                   ,'LEFT_ELBOW_x', 'LEFT_ELBOW_y', 'LEFT_ELBOW_v'
                   ,'RIGHT_ELBOW_x', 'RIGHT_ELBOW_y', 'RIGHT_ELBOW_v'
                   ,'LEFT_WRIST_x', 'LEFT_WRIST_y','LEFT_WRIST_v'
                   ,'RIGHT_WRIST_x','RIGHT_WRIST_y','RIGHT_WRIST_v'
                   ,'LEFT_PINKY_x','LEFT_PINKY_y','LEFT_PINKY_v'
                   ,'RIGHT_PINKY_x', 'RIGHT_PINKY_y', 'RIGHT_PINKY_v'
                   ,'LEFT_INDEX_x', 'LEFT_INDEX_y', 'LEFT_INDEX_v'
                   ,'RIGHT_INDEX_x', 'RIGHT_INDEX_y', 'RIGHT_INDEX_v'
                   ,'LEFT_THUMB_x', 'LEFT_THUMB_y', 'LEFT_THUMB_v'
                   ,'RIGHT_THUMB_x', 'RIGHT_THUMB_y', 'RIGHT_THUMB_v'
                   ,'LEFT_HIP_x', 'LEFT_HIP_y', 'LEFT_HIP_v'
                   ,'RIGHT_HIP_x', 'RIGHT_HIP_y', 'RIGHT_HIP_v'
                   ,'LEFT_KNEE_x', 'LEFT_KNEE_y', 'LEFT_KNEE_v'
                   ,'RIGHT_KNEE_x', 'RIGHT_KNEE_y', 'RIGHT_KNEE_v'
                   ,'LEFT_ANKLE_x','LEFT_ANKLE_y','LEFT_ANKLE_v'
                   ,'RIGHT_ANKLE_x','RIGHT_ANKLE_y','RIGHT_ANKLE_v'
                   ,'LEFT_HEEL_x','LEFT_HEEL_y','LEFT_HEEL_v'
                   ,'RIGHT_HEEL_x','RIGHT_HEEL_y','RIGHT_HEEL_v'
                   ,'LEFT_FOOT_INDEX_x','LEFT_FOOT_INDEX_y','LEFT_FOOT_INDEX_v'
                   ,'RIGHT_FOOT_INDEX_x','RIGHT_FOOT_INDEX_y','RIGHT_FOOT_INDEX_v' 
                   ,'shot']
    
    with open(csvFile, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames = field_names) 
        writer.writeheader() 
        writer.writerows([data])