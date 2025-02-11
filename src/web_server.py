from flask import Flask, jsonify
from flask_socketio import SocketIO
from threading import Thread

app = Flask(__name__)
socketio = SocketIO(app)
counter_instance = None
is_paused = False

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
                    const pauseBtn = document.getElementById('pauseBtn');
                    const setCountBtn = document.getElementById('setCountBtn');
                    const setCountInput = document.getElementById('setCountInput');
                    let isPaused = false;

                    socket.on('update_count', (data) => {{
                        document.getElementById('count').textContent = data.count;
                    }});

                    socket.on('pause_status', (data) => {{
                        isPaused = data.is_paused;
                        pauseBtn.textContent = isPaused ? 'Resume' : 'Pause';
                        pauseBtn.className = isPaused ? 'button paused' : 'button';
                    }});

                    pauseBtn.addEventListener('click', () => {{
                        socket.emit('toggle_pause');
                    }});

                    setCountBtn.addEventListener('click', () => {{
                        const newCount = setCountInput.value;
                        if (newCount !== '') {{
                            socket.emit('set_count', {{ count: newCount }});
                            setCountInput.value = '';
                        }}
                    }});

                    setCountInput.addEventListener('keypress', (e) => {{
                        if (e.key === 'Enter') {{
                            setCountBtn.click();
                        }}
                    }});
                    resetBtn.addEventListener('click', () => {{
                        socket.emit('reset_count');
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
                .button {{
                    background-color: #1a73e8;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                    margin-top: 1rem;
                    cursor: pointer;
                    font-size: 1rem;
                }}
                .button:hover {{
                    background-color: #1557b0;
                }}
                .button.paused {{
                    background-color: #dc3545;
                }}
                .button.paused:hover {{
                    background-color: #bb2d3b;
                }}
                .input-group {{
                    margin-top: 1.5rem;
                    display: flex;
                    gap: 0.5rem;
                    justify-content: center;
                }}
                .number-input {{
                    padding: 8px;
                    border: 1px solid #dadce0;
                    border-radius: 5px;
                    font-size: 1rem;
                    width: 120px;
                }}
                .button.secondary {{
                    background-color: #5f6368;
                    margin-top: 0;
                }}
                .button.secondary:hover {{
                    background-color: #4a4d51;
                }}
                .button.secondary:hover {{
                    background-color: #4a4d51;
                }}
                .button.warning {{
                    background-color: #f9a825;
                    margin-left: 0.5rem;
                }}
                .button.warning:hover {{
                    background-color: #f57f17;
                }}
            </style>
        </head>
        <body>
            <div class="counter-card">
                <h1>Reset Counter</h1>
                <div id="count" class="count">{count}</div>
                <div class="subtitle">Press '1' to increment counter</div>
                <button id="pauseBtn" class="button">Pause</button>
                <button id="resetBtn" class="button warning">Reset</button>
                <div class="input-group">
                    <input type="number" id="setCountInput" min="0" class="number-input" placeholder="Enter number">
                    <button id="setCountBtn" class="button secondary">Set Count</button>
                </div>
            </div>
        </body>
    </html>
    """

def emit_update():
    socketio.emit('update_count', {'count': counter_instance.get_count()})

@socketio.on('set_count')
def handle_set_count(data):
    try:
        new_count = int(data['count'])
        if new_count >= 0:
            counter_instance.count = new_count
            emit_update()
    except (ValueError, TypeError):
        pass

@socketio.on('reset_count')
def handle_reset():
    counter_instance.count = 0
    emit_update()

@socketio.on('toggle_pause')
def handle_toggle_pause():
    global is_paused
    is_paused = not is_paused
    socketio.emit('pause_status', {'is_paused': is_paused})

def start_web_server(counter):
    global counter_instance
    counter_instance = counter
    # Monkey patch the counter's increment method to emit updates
    original_increment = counter.increment
    def new_increment():
        if not is_paused:
            original_increment()
            emit_update()
    counter.increment = new_increment
    socketio.run(app, host='127.0.0.1', port=5000)

def run_server_thread(counter):
    server_thread = Thread(target=start_web_server, args=(counter,))
    server_thread.daemon = True
    server_thread.start()