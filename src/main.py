def main():
    from counter import Counter
    from keyboard_listener import start_listener
    from web_server import run_server_thread

    counter = Counter()
    run_server_thread(counter)  # Start web server in background
    start_listener(counter)     # Start keyboard listener

if __name__ == "__main__":
    main()