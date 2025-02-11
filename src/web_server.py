from flask import Flask
from flask_socketio import SocketIO
from threading import Thread

app = Flask(__name__)
socketio = SocketIO(app)
counter_instance = None

@app.route('/')
def home():
    count = counter_instance.get_count() if counter_instance else 0
    return f"""
    <html>
        <head>
            <title>Shiny Reset Counter</title>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
            <script>
                document.addEventListener('DOMContentLoaded', () => {{
                    const socket = io();
                    socket.on('update_count', (data) => {{
                        document.getElementById('count').textContent = data.count;
                    }});
                }});
            </script>
            <style>
                body {{
                    font-family: 'Arial', sans-serif;
                    background-color: #f0f2f5;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }}
                .counter-card {{
                    background-color: white;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    padding: 2rem 4rem;
                    text-align: center;
                }}
                h1 {{
                    color: #1a73e8;
                    font-size: 2.5rem;
                    margin-bottom: 0.5rem;
                }}
                .count {{
                    font-size: 4rem;
                    font-weight: bold;
                    color: #202124;
                }}
                .subtitle {{
                    color: #5f6368;
                    font-size: 1rem;
                    margin-top: 1rem;
                }}
            </style>
        </head>
        <body>
            <div class="counter-card">
                <h1>Reset Counter</h1>
                <div id="count" class="count">{count}</div>
                <div class="subtitle">Press '1' to increment counter</div>
            </div>
        </body>
    </html>
    """

def emit_update():
    socketio.emit('update_count', {'count': counter_instance.get_count()})

def start_web_server(counter):
    global counter_instance
    counter_instance = counter
    # Monkey patch the counter's increment method to emit updates
    original_increment = counter.increment
    def new_increment():
        original_increment()
        emit_update()
    counter.increment = new_increment
    socketio.run(app, host='127.0.0.1', port=5000)

def run_server_thread(counter):
    server_thread = Thread(target=start_web_server, args=(counter,))
    server_thread.daemon = True
    server_thread.start()