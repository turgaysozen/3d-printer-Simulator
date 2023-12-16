import json
from flask import Flask, render_template, request
from flask_socketio import SocketIO

from printer import Printer

app = Flask(__name__)
socketio = SocketIO(app)

printer = Printer()

connected_clients = set()

timer_running = False


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect')
def handle_connect():
    print('client connected',request.sid)
    remove_stale_clients(request.sid)
    connected_clients.add(request.sid)
    send_one_time_status_command()


@socketio.on('disconnect')
def handle_disconnect():
    print('client disconnected', request.sid)
    connected_clients.remove(request.sid)
    

def remove_stale_clients(current_sid):
    """ Remove stale connections for the same client """
    for sid in connected_clients.copy():
        if sid != current_sid and not socketio.server.manager.is_connected(sid, namespace='/'):
            connected_clients.remove(sid)


@socketio.on('control_printer')
def control_printer(data):
    """ Control printer realtime by client command """
    global timer_running
    command = data['command']
    if command == 'pause':
        printer.pause_printer()
        timer_running = False
        send_one_time_status_command()
    elif command == 'continue':
        printer.continue_printer()
        if not timer_running:
            timer_running = True
            socketio.start_background_task(send_printer_data)
    elif command == 'stop':
        printer.stop_printer()
        if printer.is_stopped:
            send_one_time_status_command()
    elif command == 'start':
        printer.start_printer()
        if not printer.is_paused or not printer.is_stopped:
            timer_running = True
            socketio.start_background_task(send_printer_data)
    elif command == 'finish':
        printer.mark_completed()
        timer_running = False
        send_one_time_status_command()


def send_printer_data():
    """ Send 3d printer realtime data by 1 sec. interval """
    while not printer.is_stopped and timer_running:
        printer.simulate_changes()
        printer_data = json.dumps(printer.get_printer_data())
        socketio.emit('printer_data', printer_data)
        socketio.sleep(1)


def send_one_time_status_command():
    """ Send the status command to update the client once """
    printer_data = printer.get_printer_data()
    printer_data['status'] = printer.status
    updated_printer_data = json.dumps(printer_data)
    socketio.emit('printer_data', updated_printer_data)


if __name__ == '__main__':
    socketio.run(app, debug=True)
