#Version 1.30 - Optimized for Low CPU and Memory Usage
import tkinter as tk
from tkinter import filedialog, messagebox
import time
import threading
import pygame
import os

class IntervalTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Interval Timer")
        self.root.geometry("500x350")
        self.root.resizable(False, False)
        
        # Initialize pygame mixer with minimal CPU usage
        pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=2048)
        pygame.mixer.set_num_channels(1)  # Only need 1 audio channel
        
        self.running = False
        self.paused = False
        self.pause_start_time = 0
        self.total_pause_duration = 0
        self.start_time = 0
        self.elapsed = 0
        self.ringtone_path = None
        self.sound = None  # Pre-loaded sound
        self.last_alert_time = 0
        
        # Timer Display
        self.timer_label = tk.Label(root, text="00:00:00:00", font=("Arial", 36, "bold"))
        self.timer_label.pack(pady=20)
        
        # Interval Duration Setting
        interval_frame = tk.Frame(root)
        interval_frame.pack(pady=5)
        
        tk.Label(interval_frame, text="Alert Interval (seconds):", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.interval_entry = tk.Entry(interval_frame, width=10, font=("Arial", 10))
        self.interval_entry.insert(0, "60")
        self.interval_entry.pack(side=tk.LEFT, padx=5)
        
        # Ringtone Duration Setting
        duration_frame = tk.Frame(root)
        duration_frame.pack(pady=5)
        
        tk.Label(duration_frame, text="Ringtone Duration (seconds):", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.duration_entry = tk.Entry(duration_frame, width=10, font=("Arial", 10))
        self.duration_entry.insert(0, "3")
        self.duration_entry.pack(side=tk.LEFT, padx=5)
        
        # Ringtone Selection
        ringtone_frame = tk.Frame(root)
        ringtone_frame.pack(pady=10)
        
        self.ringtone_label = tk.Label(ringtone_frame, text="No ringtone selected", font=("Arial", 9), fg="gray")
        self.ringtone_label.pack()
        
        self.browse_btn = tk.Button(ringtone_frame, text="Upload Ringtone", command=self.select_ringtone)
        self.browse_btn.pack(pady=5)
        
        # Control Buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=20)
        
        self.start_btn = tk.Button(button_frame, text="Start", font=("Arial", 12, "bold"), 
                                   bg="#4CAF50", fg="white", width=8, command=self.start_timer)
        self.start_btn.grid(row=0, column=0, padx=5)
        
        self.pause_btn = tk.Button(button_frame, text="Pause", font=("Arial", 12, "bold"), 
                                   bg="#FF9800", fg="white", width=8, command=self.pause_timer, state=tk.DISABLED)
        self.pause_btn.grid(row=0, column=1, padx=5)
        
        self.resume_btn = tk.Button(button_frame, text="Resume", font=("Arial", 12, "bold"), 
                                    bg="#2196F3", fg="white", width=8, command=self.resume_timer, state=tk.DISABLED)
        self.resume_btn.grid(row=0, column=2, padx=5)
        
        self.end_btn = tk.Button(button_frame, text="End", font=("Arial", 12, "bold"), 
                                bg="#f44336", fg="white", width=8, command=self.end_timer, state=tk.DISABLED)
        self.end_btn.grid(row=0, column=3, padx=5)
        
        # Next Alert Info
        self.next_alert_label = tk.Label(root, text="", font=("Arial", 9), fg="blue")
        self.next_alert_label.pack(pady=10)
        
    def select_ringtone(self):
        filepath = filedialog.askopenfilename(
            title="Select Ringtone",
            filetypes=[("Audio Files", "*.mp3 *.wav *.ogg"), ("All Files", "*.*")]
        )
        if filepath:
            self.ringtone_path = filepath
            filename = os.path.basename(filepath)
            self.ringtone_label.config(text=f"Selected: {filename}", fg="green")
            # Pre-load the sound to avoid delay
            try:
                self.sound = pygame.mixer.Sound(filepath)
            except Exception as e:
                messagebox.showerror("Error", f"Could not load audio file: {e}")
                self.ringtone_path = None
                self.sound = None
    
    def start_timer(self):
        try:
            interval = float(self.interval_entry.get())
            duration = float(self.duration_entry.get())
            if interval <= 0 or duration <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid positive numbers for interval and duration.")
            return
        
        if not self.ringtone_path:
            messagebox.showwarning("No Ringtone", "Please select a ringtone first.")
            return
        
        self.running = True
        self.paused = False
        self.start_time = time.time()
        self.elapsed = 0
        self.total_pause_duration = 0
        self.interval = interval
        self.ringtone_duration = duration
        self.next_alert = interval
        
        self.start_btn.config(state=tk.DISABLED)
        self.pause_btn.config(state=tk.NORMAL)
        self.resume_btn.config(state=tk.DISABLED)
        self.end_btn.config(state=tk.NORMAL)
        self.interval_entry.config(state=tk.DISABLED)
        self.duration_entry.config(state=tk.DISABLED)
        self.browse_btn.config(state=tk.DISABLED)
        
        threading.Thread(target=self.run_timer, daemon=True).start()
    
    def pause_timer(self):
        if self.running and not self.paused:
            self.paused = True
            self.pause_start_time = time.time()
            self.pause_btn.config(state=tk.DISABLED)
            self.resume_btn.config(state=tk.NORMAL)
            if self.sound:
                self.sound.stop()
    
    def resume_timer(self):
        if self.running and self.paused:
            self.paused = False
            # Add the pause duration to total
            self.total_pause_duration += time.time() - self.pause_start_time
            self.pause_btn.config(state=tk.NORMAL)
            self.resume_btn.config(state=tk.DISABLED)
    
    def run_timer(self):
        last_update = 0
        while self.running:
            if not self.paused:
                current_time = time.time()
                self.elapsed = current_time - self.start_time - self.total_pause_duration
                
                # Check if it's time to play ringtone (with precise timing)
                if self.elapsed >= self.next_alert and (current_time - self.last_alert_time) > 0.5:
                    self.last_alert_time = current_time
                    threading.Thread(target=self.play_ringtone, daemon=True).start()
                    self.next_alert += self.interval
                
                # Update display only 10 times per second to reduce CPU
                if current_time - last_update >= 0.1:
                    self.update_display()
                    last_update = current_time
            
            time.sleep(0.05)  # 50ms sleep reduces CPU significantly
    
    def update_display(self):
        hrs = int(self.elapsed // 3600)
        mins = int((self.elapsed % 3600) // 60)
        secs = int(self.elapsed % 60)
        ms = int((self.elapsed % 1) * 100)
        
        time_str = f"{hrs:02d}:{mins:02d}:{secs:02d}:{ms:02d}"
        self.timer_label.config(text=time_str)
        
        time_to_next = self.next_alert - self.elapsed
        if time_to_next > 0:
            self.next_alert_label.config(text=f"Next alert in: {time_to_next:.1f}s")
    
    def play_ringtone(self):
        if self.sound:
            try:
                # Play without volume adjustment to save CPU
                self.sound.play()
                # Stop after duration
                threading.Timer(self.ringtone_duration, lambda: self.sound.fadeout(100)).start()
            except Exception as e:
                pass  # Silent error handling to save memory
    
    def end_timer(self):
        self.running = False
        self.paused = False
        if self.sound:
            self.sound.stop()  # Stop any playing ringtone
        self.start_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)
        self.resume_btn.config(state=tk.DISABLED)
        self.end_btn.config(state=tk.DISABLED)
        self.interval_entry.config(state=tk.NORMAL)
        self.duration_entry.config(state=tk.NORMAL)
        self.browse_btn.config(state=tk.NORMAL)
        self.next_alert_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = IntervalTimer(root)
    root.mainloop()