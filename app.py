from djitellopy import Tello
import time
import cv2 
from threading import Thread
from flask import Flask, request, render_template , Response
from flask_cors import CORS
from flask_socketio import SocketIO
import base64

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

@app.route("/")
def index():
    return render_template('index.html')

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
    
# def new():
#     drone = Tello()
#     drone.connect()
#     drone.streamon()
#     frame_read = drone.get_frame_read()
#     while True:
#         img = frame_read.frame
#         imgencode = cv2.imencode('.jpg', img)[1]
#         stringData=imgencode.tostring()
#         yield (b'--frame\r\n'
#             b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')
# @app.route('/calc')
# def calc():
#     return Response(new(),mimetype='multipart/x-mixed-replace; boundary=frame')

@socketio.on('check')
def gen(json):
    drone = Tello()
    drone.connect()
    drone.streamon()
    frame_read = drone.get_frame_read()
    while True:
        img = frame_read.frame
        new_img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
        imgencode = cv2.imencode('.jpg', new_img)[1].tobytes()
        Data = base64.encodebytes(imgencode).decode('utf-8')
        message(Data)
        socketio.sleep(0)

def message(json, methods=['GET','POST']):
	# print("Recieved message")
	socketio.emit('image', json )

# @socketio.on('stream_on')
# def stream_on():
#     print( 'connected to server' )
#     drone = Tello()
#     drone.connect()
#     drone.streamon()
#     frame_read = drone.get_frame_read()
#     while True:
#         img = frame_read.frame
#         imgencode = cv2.imencode('.jpg', img)[1]
        
#         Data = base64.b64encode(imgencode).decode('utf-8')
#         b64_src = 'data:image/jpg;base64,'
#         stringData = b64_src + Data
#         socketio.emit('response_back', stringData)
#     drone.streamoff()

if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000)
    # app.run(host='127.0.0.1', port=5000, threaded=True)
# @socketio.on( 'stream_off' )
# def stream_off( ):
#     print( 'disconnected, stream is off' )