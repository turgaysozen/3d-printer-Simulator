import json
import socketio
from printer import Printer
from flask import render_template, Flask
from flask_socketio import SocketIO

PORT = 5000
HOST = 'localhost'

app = Flask(__name__)
socketio = SocketIO(app)

printer = Printer()


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect')
def handle_connect():
    print('client connected')
    

@socketio.on('control_printer')
def control_printer(data):
    command = data['command']
    if command == 'pause':
        printer.pause_printer()
    elif command == 'continue':
        printer.continue_printer()
    elif command == 'stop':
        printer.stop_printer()
    elif command == 'start':
        printer.start_printer()
        # emit_printer_data(1)
        
        
# @socketio.on('increase_timer_speed')
# def increase_timer_speed(data):
#     factor = data['factor']
#     new_interval = 1 / factor
#     emit_printer_data(new_interval)
        
        
def emit_printer_data(interval=1):
    while True:
        printer.simulate_changes()
        printer_data = json.dumps(printer.get_printer_data())
        socketio.emit('printer_data', printer_data)
        socketio.sleep(interval)
    

if __name__ == '__main__':
    socketio.start_background_task(emit_printer_data)
    socketio.run(app, host=HOST, port=PORT, debug=True)
