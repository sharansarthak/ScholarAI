# Python program to save a 
# video using OpenCV 


import cv2 


# Create an object to read 
# from camera 
video = cv2.VideoCapture(0) 

# We need to check if camera 
# is opened previously or not 
if (video.isOpened() == False): 
    print("Error reading video file") 

# We need to set resolutions. 
# so, convert them from float to integer. 
frame_width = int(video.get(3)) 
frame_height = int(video.get(4)) 

size = (frame_width, frame_height) 

# VideoWriter object to create a video file
result = cv2.VideoWriter('filename.mp4',  # Change the file extension to '.mp4'
                        cv2.VideoWriter_fourcc(*'mp4v'),  # Use 'mp4v' codec for MP4 format
                        10, size)
    
while(True): 
    print("True")
    ret, frame = video.read() 

    if ret == True: 

        # Write the frame into the 
        # file 'filename.avi' 
        result.write(frame) 

        # Display the frame 
        # saved in the file 
        cv2.imshow('Frame', frame) 

        # Press S on keyboard 
        # to stop the process 
        if cv2.waitKey(1) & 0xFF == ord('s'): 
            break

    # Break the loop 
    else: 
        break

# When everything done, release 
# the video capture and video 
# write objects 
video.release() 
result.release() 
    
# Closes all the frames 
cv2.destroyAllWindows() 

print("The video was successfully saved") 