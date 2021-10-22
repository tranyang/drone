from djitellopy import Tello
import time
import cv2 
from threading import Thread

drone = Tello()
drone.connect()

print(drone.get_battery())
# keepRecording = True
drone.streamon()
frame_read = drone.get_frame_read()
# def videoRecorder():
# # create a VideoWrite object, recoring to ./video.avi
#     height, width, _ = frame_read.frame.shape
#     video = cv2.VideoWriter('video.avi', cv2.VideoWriter_fourcc(*'XVID'), 30, (width, height))

#     while keepRecording:
#         video.write(frame_read.frame)
#         time.sleep(1 / 30)
#     video.release()
# recorder = Thread(target=videoRecorder)
# recorder.start()

def videoStreaming():
    while True:
        img = frame_read.frame
        cv2.imshow("Tello View", img)
        # key = cv2.waitKey(1) & 0xff
        # if cv2.waitKey(1) & drone.get_height() == 0:
        #     break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
stream = Thread(target=videoStreaming)
stream.start

drone.takeoff()
time.sleep(8)
drone.land()

drone.streamoff()
# keepRecording = False
stream.join()
# recorder.join()
cv2.destroyWindow('Tello View')
cv2.destroyAllWindows()




# drone = Tello()
# drone.connect()

# keepRecording = True
# drone.streamon()
# frame_read = drone.get_frame_read()

# def videoRecorder():
#     # create a VideoWrite object, recoring to ./video.avi
#     height, width, _ = frame_read.frame.shape
#     video = cv2.VideoWriter('video.avi', cv2.VideoWriter_fourcc(*'XVID'), 30, (width, height))

#     while keepRecording:
#         video.write(frame_read.frame)
#         time.sleep(1 / 30)

#     video.release()

# # we need to run the recorder in a seperate thread, otherwise blocking options
# #  would prevent frames from getting added to the video
# recorder = Thread(target=videoRecorder)
# recorder.start()


# # print(drone.query_wifi_signal_noise_ratio())
# print(drone.get_battery())

# time.sleep(2)

# time.sleep(1)
# keepRecording = False
# recorder.join()
# print(drone.get_battery())
