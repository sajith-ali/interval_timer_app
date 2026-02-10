import tkinter as tk
from tkinter import filedialog, messagebox
import time
import threading
import pygame
import os
import json
from datetime import datetime
import openpyxl
from openpyxl import Workbook
import sys

class IntervalTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Interval Timer v2.0")
        self.root.geometry("600x620")
        self.root.resizable(False, False)
        
        # Initialize pygame mixer with minimal CPU usage
        pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=2048)
        pygame.mixer.set_num_channels(1)
        
        self.running = False
        self.paused = False
        self.in_break = False
        self.pause_start_time = 0
        self.total_pause_duration = 0
        self.start_time = 0
        self.elapsed = 0
        self.main_elapsed = 0
        self.work_ringtone_path = None
        self.break_ringtone_path = None
        self.work_sound = None
        self.break_sound = None
        self.last_alert_time = 0
        self.interval_count = 0
        self.break_count = 0
        self.config_file = "timer_config.json"
        self.excel_path = None
        self.session_start_time = None
        self.session_end_time = None
        
        # Load saved ringtone path
        self.load_config()
        
        # Main Clock Display (Total Runtime)
        main_clock_frame = tk.Frame(root)
        main_clock_frame.pack(pady=5)
        tk.Label(main_clock_frame, text="Total Runtime:", font=("Arial", 10)).pack()
        self.main_clock_label = tk.Label(main_clock_frame, text="00:00:00:00", font=("Arial", 24, "bold"), fg="blue")
        self.main_clock_label.pack()
        
        # Timer Display (Interval/Break Timer)
        timer_frame = tk.Frame(root)
        timer_frame.pack(pady=5)
        self.mode_label = tk.Label(timer_frame, text="WORK TIME", font=("Arial", 12, "bold"), fg="green")
        self.mode_label.pack()
        self.timer_label = tk.Label(timer_frame, text="00:00:00:00", font=("Arial", 32, "bold"))
        self.timer_label.pack()
        
        # Counters Display
        counter_frame = tk.Frame(root)
        counter_frame.pack(pady=10)
        
        tk.Label(counter_frame, text="Work Intervals:", font=("Arial", 10)).grid(row=0, column=0, padx=10)
        self.interval_counter_label = tk.Label(counter_frame, text="0", font=("Arial", 16, "bold"), fg="green")
        self.interval_counter_label.grid(row=0, column=1, padx=10)
        
        tk.Label(counter_frame, text="Breaks Taken:", font=("Arial", 10)).grid(row=0, column=2, padx=10)
        self.break_counter_label = tk.Label(counter_frame, text="0", font=("Arial", 16, "bold"), fg="orange")
        self.break_counter_label.grid(row=0, column=3, padx=10)
        
        # Settings Frame
        settings_frame = tk.LabelFrame(root, text="Work Interval Settings", font=("Arial", 10, "bold"))
        settings_frame.pack(pady=5, padx=20, fill="x")
        
        # Interval Duration
        interval_frame = tk.Frame(settings_frame)
        interval_frame.pack(pady=3)
        tk.Label(interval_frame, text="Work Duration (sec):", font=("Arial", 9)).pack(side=tk.LEFT, padx=5)
        self.interval_entry = tk.Entry(interval_frame, width=8, font=("Arial", 9))
        self.interval_entry.insert(0, "1500")  # 25 minutes default
        self.interval_entry.pack(side=tk.LEFT, padx=5)
        
        # Work Ringtone Duration
        work_duration_frame = tk.Frame(settings_frame)
        work_duration_frame.pack(pady=3)
        tk.Label(work_duration_frame, text="Ringtone Duration (sec):", font=("Arial", 9)).pack(side=tk.LEFT, padx=5)
        self.work_ringtone_duration_entry = tk.Entry(work_duration_frame, width=8, font=("Arial", 9))
        self.work_ringtone_duration_entry.insert(0, "3")
        self.work_ringtone_duration_entry.pack(side=tk.LEFT, padx=5)
        
        # Work Ringtone Selection
        work_ringtone_frame = tk.Frame(settings_frame)
        work_ringtone_frame.pack(pady=3)
        self.work_ringtone_label = tk.Label(work_ringtone_frame, text="No work ringtone", font=("Arial", 9), fg="gray")
        self.work_ringtone_label.pack()
        self.work_browse_btn = tk.Button(work_ringtone_frame, text="Upload Work Ringtone", command=self.select_work_ringtone, font=("Arial", 9))
        self.work_browse_btn.pack(pady=2)
        
        # Break Settings Frame
        break_settings_frame = tk.LabelFrame(root, text="Break Time Settings", font=("Arial", 10, "bold"))
        break_settings_frame.pack(pady=5, padx=20, fill="x")
        
        # Break Duration
        break_frame = tk.Frame(break_settings_frame)
        break_frame.pack(pady=3)
        tk.Label(break_frame, text="Break Duration (sec):", font=("Arial", 9)).pack(side=tk.LEFT, padx=5)
        self.break_entry = tk.Entry(break_frame, width=8, font=("Arial", 9))
        self.break_entry.insert(0, "300")  # 5 minutes default
        self.break_entry.pack(side=tk.LEFT, padx=5)
        
        # Break Ringtone Duration
        break_duration_frame = tk.Frame(break_settings_frame)
        break_duration_frame.pack(pady=3)
        tk.Label(break_duration_frame, text="Ringtone Duration (sec):", font=("Arial", 9)).pack(side=tk.LEFT, padx=5)
        self.break_ringtone_duration_entry = tk.Entry(break_duration_frame, width=8, font=("Arial", 9))
        self.break_ringtone_duration_entry.insert(0, "3")
        self.break_ringtone_duration_entry.pack(side=tk.LEFT, padx=5)
        
        # Break Ringtone Selection
        break_ringtone_frame = tk.Frame(break_settings_frame)
        break_ringtone_frame.pack(pady=3)
        self.break_ringtone_label = tk.Label(break_ringtone_frame, text="No break ringtone", font=("Arial", 9), fg="gray")
        self.break_ringtone_label.pack()
        self.break_browse_btn = tk.Button(break_ringtone_frame, text="Upload Break Ringtone", command=self.select_break_ringtone, font=("Arial", 9))
        self.break_browse_btn.pack(pady=2)
        
        # Load saved ringtone if exists
        if self.work_ringtone_path and os.path.exists(self.work_ringtone_path):
            filename = os.path.basename(self.work_ringtone_path)
            self.work_ringtone_label.config(text=f"Loaded: {filename}", fg="green")
            try:
                self.work_sound = pygame.mixer.Sound(self.work_ringtone_path)
            except:
                self.work_ringtone_path = None
        
        if self.break_ringtone_path and os.path.exists(self.break_ringtone_path):
            filename = os.path.basename(self.break_ringtone_path)
            self.break_ringtone_label.config(text=f"Loaded: {filename}", fg="green")
            try:
                self.break_sound = pygame.mixer.Sound(self.break_ringtone_path)
            except:
                self.break_ringtone_path = None
        
        # Control Buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)
        
        self.start_btn = tk.Button(button_frame, text="Start", font=("Arial", 11, "bold"), 
                                   bg="#4CAF50", fg="white", width=7, command=self.start_timer)
        self.start_btn.grid(row=0, column=0, padx=4)
        
        self.pause_btn = tk.Button(button_frame, text="Pause", font=("Arial", 11, "bold"), 
                                   bg="#FF9800", fg="white", width=7, command=self.pause_timer, state=tk.DISABLED)
        self.pause_btn.grid(row=0, column=1, padx=4)
        
        self.resume_btn = tk.Button(button_frame, text="Resume", font=("Arial", 11, "bold"), 
                                    bg="#2196F3", fg="white", width=7, command=self.resume_timer, state=tk.DISABLED)
        self.resume_btn.grid(row=0, column=2, padx=4)
        
        self.end_btn = tk.Button(button_frame, text="End", font=("Arial", 11, "bold"), 
                                bg="#f44336", fg="white", width=7, command=self.end_timer, state=tk.DISABLED)
        self.end_btn.grid(row=0, column=3, padx=4)
        
        # Open Excel Button
        excel_button_frame = tk.Frame(root)
        excel_button_frame.pack(pady=5)
        
        self.open_excel_btn = tk.Button(excel_button_frame, text="📊 Open Study Log", font=("Arial", 10), 
                                        bg="#607D8B", fg="white", width=20, command=self.open_excel_file)
        self.open_excel_btn.pack()
        
        # Next Event Info
        self.next_event_label = tk.Label(root, text="", font=("Arial", 9), fg="blue")
        self.next_event_label.pack(pady=5)
    
    def load_config(self):
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.work_ringtone_path = config.get('work_ringtone_path')
                    self.break_ringtone_path = config.get('break_ringtone_path')
                    self.excel_path = config.get('excel_path')
        except:
            pass
    
    def save_config(self):
        try:
            config = {
                'work_ringtone_path': self.work_ringtone_path,
                'break_ringtone_path': self.break_ringtone_path,
                'excel_path': self.excel_path
            }
            with open(self.config_file, 'w') as f:
                json.dump(config, f)
        except:
            pass
    
    def select_work_ringtone(self):
        filepath = filedialog.askopenfilename(
            title="Select Work Ringtone",
            filetypes=[("Audio Files", "*.mp3 *.wav *.ogg"), ("All Files", "*.*")]
        )
        if filepath:
            self.work_ringtone_path = filepath
            filename = os.path.basename(filepath)
            self.work_ringtone_label.config(text=f"Selected: {filename}", fg="green")
            try:
                self.work_sound = pygame.mixer.Sound(filepath)
                self.save_config()
            except Exception as e:
                messagebox.showerror("Error", f"Could not load audio file: {e}")
                self.work_ringtone_path = None
                self.work_sound = None
    
    def select_break_ringtone(self):
        filepath = filedialog.askopenfilename(
            title="Select Break Ringtone",
            filetypes=[("Audio Files", "*.mp3 *.wav *.ogg"), ("All Files", "*.*")]
        )
        if filepath:
            self.break_ringtone_path = filepath
            filename = os.path.basename(filepath)
            self.break_ringtone_label.config(text=f"Selected: {filename}", fg="green")
            try:
                self.break_sound = pygame.mixer.Sound(filepath)
                self.save_config()
            except Exception as e:
                messagebox.showerror("Error", f"Could not load audio file: {e}")
                self.break_ringtone_path = None
                self.break_sound = None
    
    def start_timer(self):
        try:
            interval = float(self.interval_entry.get())
            break_time = float(self.break_entry.get())
            work_duration = float(self.work_ringtone_duration_entry.get())
            break_duration = float(self.break_ringtone_duration_entry.get())
            if interval <= 0 or break_time < 0 or work_duration <= 0 or break_duration <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid positive numbers.")
            return
        
        if not self.work_ringtone_path:
            messagebox.showwarning("No Work Ringtone", "Please select a work ringtone first.")
            return
        
        if not self.break_ringtone_path:
            messagebox.showwarning("No Break Ringtone", "Please select a break ringtone first.")
            return
        
        self.running = True
        self.paused = False
        self.in_break = False
        self.start_time = time.time()
        self.main_start_time = time.time()
        self.session_start_time = datetime.now()  # Record system time
        self.elapsed = 0
        self.main_elapsed = 0
        self.total_pause_duration = 0
        self.interval_duration = interval
        self.break_duration_time = break_time
        self.work_ringtone_duration = work_duration
        self.break_ringtone_duration = break_duration
        self.next_alert = interval
        self.interval_count = 0
        self.break_count = 0
        
        self.start_btn.config(state=tk.DISABLED)
        self.pause_btn.config(state=tk.NORMAL)
        self.resume_btn.config(state=tk.DISABLED)
        self.end_btn.config(state=tk.NORMAL)
        self.interval_entry.config(state=tk.DISABLED)
        self.break_entry.config(state=tk.DISABLED)
        self.work_ringtone_duration_entry.config(state=tk.DISABLED)
        self.break_ringtone_duration_entry.config(state=tk.DISABLED)
        self.work_browse_btn.config(state=tk.DISABLED)
        self.break_browse_btn.config(state=tk.DISABLED)
        
        threading.Thread(target=self.run_timer, daemon=True).start()
    
    def pause_timer(self):
        if self.running and not self.paused:
            self.paused = True
            self.pause_start_time = time.time()
            self.pause_btn.config(state=tk.DISABLED)
            self.resume_btn.config(state=tk.NORMAL)
            if self.work_sound:
                self.work_sound.stop()
            if self.break_sound:
                self.break_sound.stop()
    
    def resume_timer(self):
        if self.running and self.paused:
            self.paused = False
            pause_duration = time.time() - self.pause_start_time
            self.total_pause_duration += pause_duration
            self.pause_btn.config(state=tk.NORMAL)
            self.resume_btn.config(state=tk.DISABLED)
    
    def run_timer(self):
        last_update = 0
        while self.running:
            if not self.paused:
                current_time = time.time()
                self.main_elapsed = current_time - self.main_start_time - self.total_pause_duration
                self.elapsed = current_time - self.start_time - self.total_pause_duration
                
                # Check if current phase (work/break) is complete
                current_limit = self.break_duration_time if self.in_break else self.interval_duration
                
                if self.elapsed >= current_limit:
                    # Play ringtone
                    if current_time - self.last_alert_time > 0.5:
                        self.last_alert_time = current_time
                        
                        # Get ringtone duration for this phase
                        ringtone_wait_time = self.break_ringtone_duration if self.in_break else self.work_ringtone_duration
                        
                        # Play ringtone in separate thread
                        threading.Thread(target=self.play_ringtone, daemon=True).start()
                        
                        # Bring window to front and restore if minimized
                        self.root.deiconify()  # Restore if minimized
                        self.root.lift()  # Bring to front
                        self.root.attributes('-topmost', True)
                        self.root.focus_force()  # Force focus
                        self.root.after(100, lambda: self.root.attributes('-topmost', False))
                        
                        # Wait for ringtone duration while keeping main clock running
                        ringtone_end_time = current_time + ringtone_wait_time
                        while time.time() < ringtone_end_time and self.running and not self.paused:
                            # Update main clock during ringtone
                            self.main_elapsed = time.time() - self.main_start_time - self.total_pause_duration
                            self.update_main_clock()
                            time.sleep(0.1)
                        
                        self.last_alert_time = time.time()
                    
                    # Switch between work and break
                    if self.in_break:
                        # Break finished, start work interval
                        self.in_break = False
                        self.break_count += 1
                        self.mode_label.config(text="WORK TIME", fg="green")
                    else:
                        # Work finished, start break
                        self.in_break = True
                        self.interval_count += 1
                        self.mode_label.config(text="BREAK TIME", fg="orange")
                    
                    # Reset timer for next phase AFTER ringtone finished
                    self.start_time = time.time()
                    self.total_pause_duration = 0
                    self.elapsed = 0
                    
                    # Update counters
                    self.interval_counter_label.config(text=str(self.interval_count))
                    self.break_counter_label.config(text=str(self.break_count))
                
                # Update display
                if current_time - last_update >= 0.1:
                    self.update_display()
                    last_update = current_time
            
            time.sleep(0.05)
    
    def update_display(self):
        # Main clock (total runtime) - with milliseconds
        self.update_main_clock()
        
        # Current interval/break timer - without milliseconds
        hrs = int(self.elapsed // 3600)
        mins = int((self.elapsed % 3600) // 60)
        secs = int(self.elapsed % 60)
        time_str = f"{hrs:02d}:{mins:02d}:{secs:02d}"
        self.timer_label.config(text=time_str)
        
        # Time remaining
        current_limit = self.break_duration_time if self.in_break else self.interval_duration
        time_remaining = current_limit - self.elapsed
        if time_remaining > 0:
            mode_text = "break" if self.in_break else "work"
            self.next_event_label.config(text=f"Time until {mode_text} ends: {time_remaining:.1f}s")
    
    def update_main_clock(self):
        # Main clock update (with milliseconds)
        hrs_m = int(self.main_elapsed // 3600)
        mins_m = int((self.main_elapsed % 3600) // 60)
        secs_m = int(self.main_elapsed % 60)
        ms_m = int((self.main_elapsed % 1) * 100)
        main_time_str = f"{hrs_m:02d}:{mins_m:02d}:{secs_m:02d}:{ms_m:02d}"
        self.main_clock_label.config(text=main_time_str)
    
    def play_ringtone(self):
        # Play the appropriate ringtone based on current mode
        if self.in_break and self.break_sound:
            # Break just ended, play break ringtone
            try:
                self.break_sound.play()
                threading.Timer(self.break_ringtone_duration, lambda: self.break_sound.fadeout(100)).start()
            except:
                pass
        elif not self.in_break and self.work_sound:
            # Work just ended, play work ringtone
            try:
                self.work_sound.play()
                threading.Timer(self.work_ringtone_duration, lambda: self.work_sound.fadeout(100)).start()
            except:
                pass
    
    def end_timer(self):
        # Record session end time
        if self.running:
            self.session_end_time = datetime.now()
            self.save_session_to_excel()
        
        self.running = False
        self.paused = False
        if self.work_sound:
            self.work_sound.stop()
        if self.break_sound:
            self.break_sound.stop()
        self.start_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)
        self.resume_btn.config(state=tk.DISABLED)
        self.end_btn.config(state=tk.DISABLED)
        self.interval_entry.config(state=tk.NORMAL)
        self.break_entry.config(state=tk.NORMAL)
        self.work_ringtone_duration_entry.config(state=tk.NORMAL)
        self.break_ringtone_duration_entry.config(state=tk.NORMAL)
        self.work_browse_btn.config(state=tk.NORMAL)
        self.break_browse_btn.config(state=tk.NORMAL)
        self.next_event_label.config(text="")
        self.mode_label.config(text="READY", fg="black")
        
        # Reset counters and timers to zero
        self.interval_count = 0
        self.break_count = 0
        self.interval_counter_label.config(text="0")
        self.break_counter_label.config(text="0")
        
        # Reset all timers to zero
        self.elapsed = 0
        self.main_elapsed = 0
        self.timer_label.config(text="00:00:00")
        self.main_clock_label.config(text="00:00:00:00")
    
    def save_session_to_excel(self):
        try:
            # Check if excel path exists, if not ask user
            if not self.excel_path or not os.path.exists(os.path.dirname(self.excel_path) if os.path.dirname(self.excel_path) else '.'):
                save_path = filedialog.asksaveasfilename(
                    title="Save Study Log Excel File",
                    defaultextension=".xlsx",
                    filetypes=[("Excel Files", "*.xlsx"), ("All Files", "*.*")],
                    initialfile="study_log.xlsx"
                )
                if not save_path:
                    return  # User cancelled
                self.excel_path = save_path
                self.save_config()
            
            # Create or load workbook
            try:
                if os.path.exists(self.excel_path):
                    wb = openpyxl.load_workbook(self.excel_path)
                    ws = wb.active
                else:
                    wb = Workbook()
                    ws = wb.active
                    # Create headers
                    ws.append([
                        "Date", "Start_Time", "End_Time", "Total_Run_Time", 
                        "Session", "Session_Time", "Break", "Break_Time",
                        "Over_All_Session_Time", "Over_All_Break_Time"
                    ])
            except PermissionError:
                # File is open, ask user to choose different location
                response = messagebox.askyesno(
                    "File In Use",
                    f"The file is currently open:\n{self.excel_path}\n\n"
                    "Please close it and click 'Yes' to retry,\n"
                    "or click 'No' to save to a different file."
                )
                if response:
                    # Retry same file
                    return self.save_session_to_excel()
                else:
                    # Ask for new location
                    self.excel_path = None
                    return self.save_session_to_excel()
            
            # Calculate data
            date = self.session_start_time.strftime("%Y-%m-%d")
            start_time = self.session_start_time.strftime("%H:%M:%S")
            end_time = self.session_end_time.strftime("%H:%M:%S")
            total_run_time = self.format_time(self.main_elapsed)
            
            session_count = self.interval_count
            session_time = self.interval_count * self.interval_duration
            break_count = self.break_count
            break_time = self.break_count * self.break_duration_time
            
            overall_session_hours = session_time / 3600
            overall_break_hours = break_time / 3600
            
            # Append row
            ws.append([
                date,
                start_time,
                end_time,
                total_run_time,
                session_count,
                self.format_time(session_time),
                break_count,
                self.format_time(break_time),
                overall_session_hours,  # Number format
                overall_break_hours     # Number format
            ])
            
            # Save workbook
            try:
                wb.save(self.excel_path)
                messagebox.showinfo("Success", f"Session saved to:\n{self.excel_path}")
            except PermissionError:
                messagebox.showerror(
                    "Cannot Save",
                    f"The file is open in another program:\n{self.excel_path}\n\n"
                    "Please close it and try pressing 'End' again."
                )
                return  # Don't reset if save failed
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save session:\n{str(e)}")
            return  # Don't reset if save failed
    
    def open_excel_file(self):
        """Open the Excel file in the default application"""
        if self.excel_path and os.path.exists(self.excel_path):
            try:
                # Open file with default application
                if os.name == 'nt':  # Windows
                    os.startfile(self.excel_path)
                elif os.name == 'posix':  # macOS and Linux
                    import subprocess
                    if sys.platform == 'darwin':  # macOS
                        subprocess.call(('open', self.excel_path))
                    else:  # Linux
                        subprocess.call(('xdg-open', self.excel_path))
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file:\n{str(e)}")
        else:
            messagebox.showwarning("No File", "No study log file exists yet.\nComplete a session first!")
    
    def format_time(self, seconds):
        """Format seconds to HH:MM:SS"""
        hrs = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hrs:02d}:{mins:02d}:{secs:02d}"

if __name__ == "__main__":
    root = tk.Tk()
    app = IntervalTimer(root)
    root.mainloop()