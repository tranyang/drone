from djitellopy import Tello
import time
import cv2 
from threading import Thread
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route('/drone/takeoff', methods=['POST'])
def takeoff():
    drone = Tello()
    drone.connect()

    drone_batt = drone.get_battery()
    drone.takeoff()
    time.sleep(10)
    drone.land()

    msg = f'drone has {drone_batt} left'
    return (msg, 201)

@app.route('/batt')
def batt():
    drone = Tello()
    drone.connect()
    drone_batt = drone.get_battery()
    return str(drone_batt)
        
@app.route('/post', methods=['POST'])
def post_route():
    if request.method == 'POST':

        data = request.get_json()

        # print('Data Received: "{data}"'.format(data=data))
        print(data)
        drone = Tello()
        drone.connect()

        drone_batt = drone.get_battery()
        if drone_batt > 30:
            
            drone.takeoff()
            time.sleep(8)
            drone.move_up(50)
            time.sleep(2)

            for cmd in data["instructions"]:
                print(cmd)
                cm = int(cmd["dist"])
                deg = int(cmd["angle"])
                print(cm,deg)
                
                if cmd['angle'] == 0:
                    pass
                else:
                    drone.rotate_clockwise(deg)
                    
                if cmd['dist'] == 0 :
                    pass
                else:
                    drone.move_forward(cm)
            
            time.sleep(1)
            drone.rotate_clockwise(180)   
            for cmd in reversed(data["instructions"]):
                print(cmd)
                cm = int(cmd["dist"])
                deg = int(cmd["angle"])
                print(cm,deg)
                
                if cmd['dist'] == 0:
                    pass
                else:
                    drone.move_forward(cm)
                    
                if cmd['angle'] == 0:
                    pass
                else:
                    drone.rotate_counter_clockwise(deg)
                   
                
            drone.land()
        else:
            return "DRONE NOT ENOUGH JUICE.\n"
        return "Request Processed Successfully.\n"

@app.route('/stream', methods=['GET'])
def stream():
    drone = Tello()
    drone.connect()
    drone.streamon()
    frame_read = drone.get_frame_read()
    while True:
        img = frame_read.frame
        cv2.imshow("Tello View", img)
        # key = cv2.waitKey(1) & 0xff
        # if cv2.waitKey(1) & drone.get_height() == 0:
        #     break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    drone.streamoff()
    
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