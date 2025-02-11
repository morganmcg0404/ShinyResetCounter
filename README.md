# README.md

# Shiny Reset Counter

A real-time counter application that tracks keyboard presses and displays the count through a web interface. Perfect for tracking shiny hunting attempts in Pokemon games or similar repetitive counting needs.

## Features

- Background keyboard monitoring that works even when the application is not in focus
- Real-time web interface showing the current count
- WebSocket-based updates for instant counter display
- Clean, modern web UI
- Runs locally and securely

## Requirements

- Python 3.x
- Dependencies (installed via requirements.txt):
  - `pynput==1.7.6` - For keyboard input monitoring
  - `flask==3.0.0` - Web server framework
  - `flask-socketio==5.3.6` - Real-time WebSocket communication

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd background-counter
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Start the application:
   ```
   python src/main.py
   ```

2. The application will:

- Start a keyboard listener in the background
- Launch a web server at http://127.0.0.1:5000
- Begin monitoring for the '1' key press

3. Access the counter interface:

- Open your web browser and navigate to http://127.0.0.1:5000
- The webpage will automatically update whenever the counter increments

## License

This project is licensed under the MIT License.