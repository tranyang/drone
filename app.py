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
    me = Tello()
    me.connect()

    drone_batt = me.get_battery()
    me.takeoff()
    # me.move_forward(20)
    time.sleep(10)
    # me.rotate_counter_clockwise(360)
    # time.sleep(5)
    # me.move_left(20)
    me.land()

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

# me = Tello()
# me.connect()

# keepRecording = True
# me.streamon()
# frame_read = me.get_frame_read()

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


# # print(me.query_wifi_signal_noise_ratio())
# print(me.get_battery())

# me.takeoff()
# # me.move_forward(20)
# time.sleep(2)
# me.rotate_counter_clockwise(360)
# time.sleep(2)
# # me.move_left(20)
# me.land()
# time.sleep(1)
# keepRecording = False
# recorder.join()
# print(me.get_battery())