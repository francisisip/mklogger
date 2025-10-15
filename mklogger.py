from pynput import keyboard, mouse
from datetime import datetime
import threading

class ActivityLogger:
    def __init__(self, log_file='activity_log.txt'):
        self.log_file = log_file
        self.is_logging = False
        self.left_click_count = 0
        self.right_click_count = 0
        self.backspace_count = 0
        self.file_handle = None
        
    def log_event(self, event):
        """Log an event with timestamp"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        log_entry = f"[{timestamp}] {event}"
        print(log_entry)
        if self.file_handle:
            self.file_handle.write(log_entry + '\n')
            self.file_handle.flush()
    
    def start_logging(self):
        """Start logging session"""
        if not self.is_logging:
            self.is_logging = True
            self.left_click_count = 0
            self.right_click_count = 0
            self.backspace_count = 0 
            self.file_handle = open(self.log_file, 'a')
            self.log_event("=== LOGGING STARTED ===")
            print("Logging started. Press F9 to stop.")
    
    def stop_logging(self):
        """Stop logging session"""
        if self.is_logging:
            self.log_event(f"Left clicks: {self.left_click_count}")
            self.log_event(f"Right clicks: {self.right_click_count}")
            self.log_event(f"Backspaces: {self.backspace_count}")
            self.log_event("=== LOGGING STOPPED ===\n")
            self.is_logging = False
            if self.file_handle:
                self.file_handle.close()
                self.file_handle = None
            print("Logging stopped.")
    
    def on_key_press(self, key):
        """Handle key press events"""
        try:
            # Start logging with F8 key
            if key == keyboard.Key.f8:
                self.start_logging()
                return
            
            # Stop logging with F9 key
            if key == keyboard.Key.f9:
                self.stop_logging()
                return
            
            if self.is_logging:
                if key == keyboard.Key.backspace:
                    self.backspace_count += 1

                try:
                    # For regular character keys
                    key_name = key.char
                except AttributeError:
                    # For special keys
                    key_name = str(key).replace('Key.', '')
                
                self.log_event(f"Key pressed: {key_name}")
        
        except Exception as e:
            print(f"Error in key press handler: {e}")
    
    def on_click(self, x, y, button, pressed):
        """Handle mouse click events"""
        if pressed and self.is_logging:
            if button == mouse.Button.left:
                self.left_click_count += 1
                self.log_event("Mouse click: LEFT")
            elif button == mouse.Button.right:
                self.right_click_count += 1
                self.log_event("Mouse click: RIGHT")
    
    def run(self):
        """Start the logger"""
        print("Activity Logger started!")
        print("Press F8 to start logging")
        print("Press F9 to stop logging")
        
        # Create listeners
        keyboard_listener = keyboard.Listener(on_press=self.on_key_press)
        mouse_listener = mouse.Listener(on_click=self.on_click)
        
        # Start listeners
        keyboard_listener.start()
        mouse_listener.start()
        
        # Keep the program running
        try:
            keyboard_listener.join()
        except KeyboardInterrupt:
            print("\nExiting...")
            self.stop_logging()

if __name__ == "__main__":
    logger = ActivityLogger()
    logger.run()