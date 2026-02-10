# Interval Timer App v2.0

A lightweight, feature-rich productivity timer designed for studying, working, or any task requiring focused work intervals and breaks. Track your sessions automatically with Excel logging and customizable alerts.

![Version](https://img.shields.io/badge/version-2.0-blue)
![Python](https://img.shields.io/badge/python-3.6+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

---

## 📋 Table of Contents

- [Features](#features)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Dependencies](#dependencies)
- [How to Use](#how-to-use)
- [Excel Log Format](#excel-log-format)
- [Creating an Executable](#creating-an-executable)
- [Configuration Files](#configuration-files)
- [Troubleshooting](#troubleshooting)
- [Performance Optimization](#performance-optimization)

---

## ✨ Features

### Core Functionality
- **Dual Timer Display**: Main clock (total runtime) and session timer (work/break)
- **Work/Break Cycles**: Automatic alternation between work intervals and break periods
- **Pause/Resume**: Pause your session and resume without losing time
- **Session Tracking**: Counts completed work intervals and breaks taken
- **Window Restoration**: Automatically brings app to foreground when intervals end

### Customization
- **Flexible Duration**: Set custom work and break durations (in seconds)
- **Separate Ringtones**: Different alert sounds for work end and break end
- **Adjustable Alert Duration**: Control how long each ringtone plays
- **Persistent Settings**: Remembers your ringtone paths and Excel file location

### Data Logging
- **Excel Integration**: Automatically logs all sessions to Excel
- **Detailed Analytics**: Tracks date, times, durations, and session counts
- **One-Click Access**: Open your study log directly from the app
- **Cumulative Statistics**: View total hours spent on work and breaks

### Performance
- **Lightweight**: ~10-15 MB RAM usage
- **Low CPU**: ~0.5-1% during operation
- **Optimized Audio**: Minimal latency with pre-loaded sounds
- **Efficient Updates**: Smart display refresh for reduced resource usage

---

## 💻 System Requirements

- **Operating System**: Windows 7/10/11, macOS 10.12+, or Linux
- **Python**: Version 3.6 or higher
- **RAM**: Minimum 50 MB available
- **Storage**: ~20 MB for application and dependencies
- **Audio**: Sound card and speakers/headphones for alerts

---

## 📥 Installation

### Step 1: Install Python
If you don't have Python installed:
- **Windows/Mac**: Download from [python.org](https://www.python.org/downloads/)
- **Linux**: Usually pre-installed, or use `sudo apt install python3`

### Step 2: Install Dependencies
Open your terminal/command prompt and run:

```bash
pip install pygame openpyxl
```

### Step 3: Download the App
Save the Python script as `interval_timer.py` in your preferred location.

### Step 4: Run the App
```bash
python interval_timer.py
```

Or on some systems:
```bash
python3 interval_timer.py
```

---

## 📦 Dependencies

### Required Packages

| Package | Version | Purpose |
|---------|---------|---------|
| **pygame** | 2.0.0+ | Audio playback and sound management |
| **openpyxl** | 3.0.0+ | Excel file creation and manipulation |

### Built-in Modules (No Installation Needed)
- `tkinter` - GUI framework (included with Python)
- `threading` - Multi-threading support
- `time` - Time tracking
- `datetime` - Date/time formatting
- `json` - Configuration file management
- `os` - File system operations
- `sys` - System-specific parameters

### Installation Commands

**Install all dependencies at once:**
```bash
pip install pygame openpyxl
```

**Install individually:**
```bash
pip install pygame
pip install openpyxl
```

**Upgrade existing packages:**
```bash
pip install --upgrade pygame openpyxl
```

**Check installed versions:**
```bash
pip show pygame openpyxl
```

---

## 🚀 How to Use

### First Time Setup

1. **Launch the application**
   ```bash
   python interval_timer.py
   ```

2. **Configure Session Settings** (Left panel)
   - Set session duration in seconds (e.g., 1500 = 25 minutes)
   - Set session ringtone duration (how long the alert plays)
   - Click "Upload Ringtone" to select your work completion sound

3. **Configure Break Settings** (Right panel)
   - Set break duration in seconds (e.g., 300 = 5 minutes)
   - Set break ringtone duration
   - Click "Upload Ringtone" to select your break completion sound

### Running a Session

1. **Click "Start"**
   - Main clock (blue) begins counting total runtime
   - Session timer starts counting work interval
   - "SESSION TIME" indicator appears in green

2. **During Work**
   - Focus on your task
   - Watch the countdown to know time remaining
   - App can be minimized - it will restore automatically

3. **Session Interval Ends**
   - App automatically comes to foreground
   - Session ringtone plays
   - Switches to "BREAK TIME" (orange)
   - Session interval counter increases

4. **During Break**
   - Take your rest
   - Break timer counts down
   - Ringtone will alert when break ends

5. **Break Ends**
   - Break ringtone plays
   - Automatically returns to "SESSION TIME"
   - Cycle continues indefinitely

6. **Using Pause/Resume**
   - Click "Pause" to temporarily stop timers
   - Click "Resume" to continue from where you paused
   - Main clock excludes paused time

7. **Click "End"**
   - Session data saves to Excel automatically
   - All timers reset to zero
   - Counters reset to zero
   - Ready for next session

### Viewing Your Data

- Click **"📊 Open Study Log"** button
- Excel file opens with all your sessions
- Analyze patterns, calculate totals, create charts

---

## 📊 Excel Log Format

Each session creates a new row with the following columns:

| Column | Description | Example | Format |
|--------|-------------|---------|--------|
| **Date** | Date of session | 2026-02-10 | YYYY-MM-DD |
| **Start_Time** | System time when started | 09:30:15 | HH:MM:SS |
| **End_Time** | System time when ended | 11:45:30 | HH:MM:SS |
| **Total_Run_Time** | Total session duration | 02:15:15 | HH:MM:SS |
| **Session** | Number of work intervals completed | 5 | Integer |
| **Session_Time** | Total time spent working | 02:05:00 | HH:MM:SS |
| **Break** | Number of breaks taken | 4 | Integer |
| **Break_Time** | Total time spent on breaks | 00:20:00 | HH:MM:SS |
| **Over_All_Session_Time** | Work time in hours | 2.08 | Number |
| **Over_All_Break_Time** | Break time in hours | 0.33 | Number |

### Excel Features

**The last two columns are in number format**, allowing you to:
- Use formulas: `=SUM(I:I)` for total work hours
- Calculate averages: `=AVERAGE(I:I)` for average session length
- Create charts and graphs for visualization
- Filter and sort your data

### Sample Data
```
Date       | Start_Time | End_Time | Total_Run_Time | Session | Session_Time | Break | Break_Time | Over_All_Session_Time | Over_All_Break_Time
2026-02-10 | 09:00:00   | 11:30:45 | 02:30:45       | 6       | 02:30:00     | 5     | 00:25:00   | 2.50                  | 0.42
2026-02-10 | 14:00:00   | 15:45:20 | 01:45:20       | 4       | 01:40:00     | 3     | 00:15:00   | 1.67                  | 0.25
2026-02-11 | 08:30:00   | 12:00:15 | 03:30:15       | 8       | 03:20:00     | 7     | 00:35:00   | 3.33                  | 0.58
```

---

## 📦 Creating an Executable

Convert the Python script to a standalone executable that runs without Python installed.

### Install PyInstaller
```bash
pip install pyinstaller
```

### Create Executable

**Windows:**
```bash
pyinstaller --onefile --windowed --name "IntervalTimer" --icon=timer_icon.ico interval_timer.py
```

**Mac/Linux:**
```bash
pyinstaller --onefile --windowed --name "IntervalTimer" interval_timer.py
```

### Find Your Executable
- Location: `dist/IntervalTimer.exe` (Windows) or `dist/IntervalTimer` (Mac/Linux)
- Size: ~10-15 MB
- No Python installation required on target machine

### Distribution
You can share this executable with anyone. They just need to:
1. Double-click to run
2. No dependencies required
3. Works immediately

---

## ⚙️ Configuration Files

The app creates configuration files in the same directory:

### `timer_config.json`
Stores your preferences:
```json
{
  "work_ringtone_path": "C:/Users/YourName/sounds/work_alert.wav",
  "break_ringtone_path": "C:/Users/YourName/sounds/break_alert.wav",
  "excel_path": "C:/Users/YourName/Documents/study_log.xlsx"
}
```

**What it remembers:**
- Path to session ringtone
- Path to break ringtone
- Path to Excel log file

**Manual editing:**
You can edit this file to change paths if files are moved.

### `study_log.xlsx`
Your session data (location chosen by you on first run).

---

## 🔧 Troubleshooting

### Common Issues

#### **1. App won't start**
**Error**: `ModuleNotFoundError: No module named 'pygame'`

**Solution**:
```bash
pip install pygame openpyxl
```

#### **2. No sound playing**
**Possible causes**:
- Audio file format not supported
- File path incorrect
- System volume muted

**Solutions**:
- Use WAV format (most reliable)
- Re-upload ringtone through the app
- Check system audio settings
- Try a different audio file

#### **3. Excel save error: "Permission denied"**
**Cause**: Excel file is currently open

**Solutions**:
- Close the Excel file
- Click "Yes" to retry in the popup dialog
- Or choose "No" and save to a different file

#### **4. Ringtone has delay**
**Solution**: Use WAV files instead of MP3
- WAV files have no decoding delay
- MP3 files can have 100-500ms startup delay

**Convert MP3 to WAV online**:
- CloudConvert: https://cloudconvert.com/mp3-to-wav
- Set to 22050 Hz, Mono for best performance

#### **5. High CPU usage**
**Normal usage**: 0.5-1% CPU
**If higher**: 
- Close other applications
- Use shorter audio files
- Restart the app

#### **6. App doesn't come to foreground**
**On some Linux systems**: Window managers may prevent automatic focus
**Solution**: Check for notification sounds instead

---

## ⚡ Performance Optimization

### For Best Performance

#### **Audio Files**
- **Format**: WAV (recommended)
- **Sample Rate**: 22050 Hz
- **Channels**: Mono (1 channel)
- **Duration**: 1-5 seconds
- **File Size**: Under 500 KB

#### **System Settings**
- Close unnecessary background apps
- Keep Excel file closed while timer runs
- Use SSD storage for faster Excel saves

#### **Memory Usage**
- Idle: ~8-12 MB
- Running: ~10-15 MB
- Per session: No memory leak (stays constant)

#### **CPU Usage**
- Idle: ~0.1-0.3%
- Running: ~0.5-1%
- During alert: ~2-3% (brief spike)

### Converting Audio for Optimal Performance

**Online (No software needed)**:
1. Go to https://cloudconvert.com/mp3-to-wav
2. Upload your file
3. Optional settings:
   - Sample Rate: 22050 Hz
   - Audio Channels: Mono
4. Convert and download

**Using Audacity (Free software)**:
1. Download Audacity from https://www.audacityteam.org/
2. Open your audio file
3. File → Export → Export as WAV
4. Settings: 22050 Hz, Mono
5. Save

---

## 🎯 Usage Tips

### Recommended Settings

**Pomodoro Technique** (Classic):
- Session Duration: 1500 seconds (25 minutes)
- Break Duration: 300 seconds (5 minutes)

**Long Study Sessions**:
- Session Duration: 3000 seconds (50 minutes)
- Break Duration: 600 seconds (10 minutes)

**Short Sprints**:
- Session Duration: 900 seconds (15 minutes)
- Break Duration: 180 seconds (3 minutes)

### Best Practices

1. **Choose distinct ringtones**
   - Energetic sound for work end (you earned a break!)
   - Calm sound for break end (back to focus)

2. **Keep Excel closed**
   - Only open to view data
   - Close before starting new sessions

3. **Test your settings**
   - Try a short session first (60s work, 30s break)
   - Verify ringtones play correctly
   - Check Excel logging works

4. **Regular backups**
   - Your `study_log.xlsx` contains valuable data
   - Backup weekly to cloud storage

---

## 📝 Version History

### v2.0 (Current)
- Side-by-side settings layout
- Excel logging with detailed analytics
- Separate ringtones for work and breaks
- Auto-restore from minimized state
- Number format for hour columns in Excel
- Pause/Resume functionality
- Main clock runs during transitions
- Reset counters and timers on End

### v1.0
- Basic interval timer
- Single ringtone
- Work/break cycles
- Simple GUI

---

## 📄 License

This project is open source and available under the MIT License.

---

## 🤝 Support

If you encounter any issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Verify all [Dependencies](#dependencies) are installed
3. Ensure audio files are in WAV format
4. Check that Excel file is closed before saving

---

## 🎓 About

This app was designed to help students, programmers, and professionals maintain focus through structured work intervals and breaks. Based on proven productivity techniques like the Pomodoro Technique, it combines time management with automatic session logging for long-term pattern analysis.

**Happy studying! 📚✨**
