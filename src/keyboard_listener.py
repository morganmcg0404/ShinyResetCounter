from pynput import keyboard

def start_listener(counter_instance):
    def on_release(key):
        try:
            if key.char == '1':
                counter_instance.increment()
        except AttributeError:
            pass

    listener = keyboard.Listener(on_release=on_release)  # Changed from on_press to on_release
    listener.start()
    print("Listener started. Press '1' to increment counter.")
    listener.join()