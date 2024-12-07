import helper
import pose

# main running function
def main(csvName):
    helper.create_csv(csvName)
    # Sets all the videos into input folder
    video_files = helper.getAllFiles('videos')
    for video in video_files:
        folder_name = helper.create_folder('input', str(video.replace('.mp4' , '')) + ' frames')
        helper.frameExtraction('videos/' + video, folder_name)

    # Does all the outputs
    Input_folder = helper.getAllFiles('input')

    for folder in Input_folder:
        frames = helper.getAllFiles('input/' + folder)
        output_folder = helper.create_folder('output', folder + '_output')
        for frame in frames:
            frameLocation = folder + '/' + frame
            frameName = frame
            poseDict = pose.run(frameLocation, frameName, output_folder)
            helper.append_csv(csvName + '.csv', poseDict)


# main testing function
def test():
    return False

# Delete all input and output folders
helper.delete_all()

# Runs the main function
# main('test1')
