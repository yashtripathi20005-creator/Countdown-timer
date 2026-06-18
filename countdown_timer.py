"""
Countdown Timer to a Special Date
A simple GUI application that counts down to a special date
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import time
import threading
import json
import os
from tkinter import font as tkfont

class CountdownTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("🎉 Countdown Timer to Special Date")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        # Set default special date (Christmas 2026)
        self.special_date = datetime(2026, 12, 25, 0, 0, 0)
        self.running = False
        self.paused = False
        self.timer_thread = None
        
        # Colors and styling
        self.colors = {
            'bg': '#1a1a2e',
            'fg': '#e94560',
            'accent': '#0f3460',
            'text': '#ffffff',
            'success': '#2ecc71'
        }
        
        self.root.configure(bg=self.colors['bg'])
        
        # Load saved date if exists
        self.load_saved_date()
        
        self.setup_ui()
        self.update_display()
    
    def setup_ui(self):
        """Set up the user interface"""
        
        # Custom fonts
        title_font = tkfont.Font(family="Helvetica", size=24, weight="bold")
        time_font = tkfont.Font(family="Helvetica", size=48, weight="bold")
        label_font = tkfont.Font(family="Helvetica", size=12)
        
        # Title
        title_label = tk.Label(
            self.root,
            text="🎯 Countdown to Special Date",
            font=title_font,
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        title_label.pack(pady=20)
        
        # Frame for time display
        time_frame = tk.Frame(self.root, bg=self.colors['bg'])
        time_frame.pack(pady=20)
        
        # Time display
        self.time_vars = {
            'days': tk.StringVar(value="00"),
            'hours': tk.StringVar(value="00"),
            'minutes': tk.StringVar(value="00"),
            'seconds': tk.StringVar(value="00")
        }
        
        time_labels = ['Days', 'Hours', 'Minutes', 'Seconds']
        for i, (key, label_text) in enumerate(zip(self.time_vars.keys(), time_labels)):
            # Container for each time unit
            container = tk.Frame(time_frame, bg=self.colors['bg'])
            container.grid(row=0, column=i, padx=10)
            
            # Time value
            time_label = tk.Label(
                container,
                textvariable=self.time_vars[key],
                font=time_font,
                bg=self.colors['bg'],
                fg=self.colors['fg']
            )
            time_label.pack()
            
            # Time unit label
            unit_label = tk.Label(
                container,
                text=label_text,
                font=label_font,
                bg=self.colors['bg'],
                fg=self.colors['text']
            )
            unit_label.pack()
        
        # Separator
        separator = ttk.Separator(self.root, orient='horizontal')
        separator.pack(fill='x', padx=50, pady=20)
        
        # Control buttons frame
        button_frame = tk.Frame(self.root, bg=self.colors['bg'])
        button_frame.pack(pady=10)
        
        # Control buttons
        self.start_button = tk.Button(
            button_frame,
            text="▶ Start",
            command=self.start_timer,
            bg=self.colors['accent'],
            fg=self.colors['text'],
            font=label_font,
            width=10,
            height=2,
            relief='raised'
        )
        self.start_button.grid(row=0, column=0, padx=5)
        
        self.pause_button = tk.Button(
            button_frame,
            text="⏸ Pause",
            command=self.pause_timer,
            bg=self.colors['accent'],
            fg=self.colors['text'],
            font=label_font,
            width=10,
            height=2,
            relief='raised',
            state='disabled'
        )
        self.pause_button.grid(row=0, column=1, padx=5)
        
        self.reset_button = tk.Button(
            button_frame,
            text="🔄 Reset",
            command=self.reset_timer,
            bg=self.colors['accent'],
            fg=self.colors['text'],
            font=label_font,
            width=10,
            height=2,
            relief='raised'
        )
        self.reset_button.grid(row=0, column=2, padx=5)
        
        # Settings button
        self.settings_button = tk.Button(
            button_frame,
            text="⚙️ Settings",
            command=self.open_settings,
            bg=self.colors['accent'],
            fg=self.colors['text'],
            font=label_font,
            width=10,
            height=2,
            relief='raised'
        )
        self.settings_button.grid(row=0, column=3, padx=5)
        
        # Status label
        self.status_label = tk.Label(
            self.root,
            text="⏳ Ready to countdown!",
            font=label_font,
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        self.status_label.pack(pady=20)
        
        # Special date info
        self.date_info = tk.Label(
            self.root,
            text=f"Target Date: {self.special_date.strftime('%B %d, %Y at %I:%M %p')}",
            font=('Helvetica', 10),
            bg=self.colors['bg'],
            fg='#888888'
        )
        self.date_info.pack(pady=5)
    
    def update_display(self):
        """Update the countdown display"""
        if self.running and not self.paused:
            now = datetime.now()
            time_left = self.special_date - now
            
            if time_left.total_seconds() <= 0:
                self.timer_completed()
                return
            
            # Extract days, hours, minutes, seconds
            days = time_left.days
            hours, remainder = divmod(time_left.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            # Update display
            self.time_vars['days'].set(f"{days:02d}")
            self.time_vars['hours'].set(f"{hours:02d}")
            self.time_vars['minutes'].set(f"{minutes:02d}")
            self.time_vars['seconds'].set(f"{seconds:02d}")
            
            # Update status
            self.status_label.config(
                text=f"⏳ Time remaining: {days} days, {hours:02d}:{minutes:02d}:{seconds:02d}",
                fg=self.colors['text']
            )
            
            # Schedule next update
            self.root.after(1000, self.update_display)
    
    def timer_completed(self):
        """Handle timer completion"""
        self.running = False
        self.paused = False
        self.start_button.config(state='normal', text='▶ Start')
        self.pause_button.config(state='disabled', text='⏸ Pause')
        
        self.time_vars['days'].set("00")
        self.time_vars['hours'].set("00")
        self.time_vars['minutes'].set("00")
        self.time_vars['seconds'].set("00")
        
        self.status_label.config(
            text="🎉 HAPPY SPECIAL DAY! 🎉",
            fg=self.colors['success']
        )
        
        # Show popup
        messagebox.showinfo(
            "Countdown Complete! 🎉",
            f"The special date has arrived!\n\n{self.special_date.strftime('%B %d, %Y')}\n\n🎊 Congratulations! 🎊"
        )
    
    def start_timer(self):
        """Start the countdown timer"""
        if self.running and self.paused:
            # Resume from pause
            self.paused = False
            self.status_label.config(text="▶ Countdown resumed", fg=self.colors['text'])
            self.start_button.config(text='▶ Resume')
            self.pause_button.config(state='normal', text='⏸ Pause')
            self.update_display()
            return
        
        # Check if target date is in the past
        if datetime.now() >= self.special_date:
            messagebox.showwarning(
                "Warning",
                "The special date has already passed!\nPlease set a future date in Settings."
            )
            return
        
        self.running = True
        self.paused = False
        self.start_button.config(state='normal', text='▶ Running')
        self.pause_button.config(state='normal', text='⏸ Pause')
        self.status_label.config(text="⏳ Countdown started!", fg=self.colors['text'])
        self.update_display()
    
    def pause_timer(self):
        """Pause the countdown timer"""
        if self.running and not self.paused:
            self.paused = True
            self.start_button.config(text='▶ Resume')
            self.pause_button.config(state='disabled')
            self.status_label.config(text="⏸ Countdown paused", fg='#f39c12')
    
    def reset_timer(self):
        """Reset the countdown timer"""
        self.running = False
        self.paused = False
        self.start_button.config(state='normal', text='▶ Start')
        self.pause_button.config(state='disabled', text='⏸ Pause')
        
        self.time_vars['days'].set("00")
        self.time_vars['hours'].set("00")
        self.time_vars['minutes'].set("00")
        self.time_vars['seconds'].set("00")
        
        self.status_label.config(text="🔄 Timer reset", fg=self.colors['text'])
    
    def open_settings(self):
        """Open settings window"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("⚙️ Settings")
        settings_window.geometry("400x350")
        settings_window.configure(bg=self.colors['bg'])
        settings_window.resizable(False, False)
        
        # Title
        title = tk.Label(
            settings_window,
            text="Set Special Date",
            font=('Helvetica', 18, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        title.pack(pady=20)
        
        # Date inputs
        input_frame = tk.Frame(settings_window, bg=self.colors['bg'])
        input_frame.pack(pady=20)
        
        # Year
        tk.Label(input_frame, text="Year:", bg=self.colors['bg'], fg=self.colors['text']).grid(row=0, column=0, pady=5, padx=10)
        year_var = tk.StringVar(value=str(self.special_date.year))
        year_entry = tk.Entry(input_frame, textvariable=year_var, width=10)
        year_entry.grid(row=0, column=1, pady=5)
        
        # Month
        tk.Label(input_frame, text="Month (1-12):", bg=self.colors['bg'], fg=self.colors['text']).grid(row=1, column=0, pady=5, padx=10)
        month_var = tk.StringVar(value=str(self.special_date.month))
        month_entry = tk.Entry(input_frame, textvariable=month_var, width=10)
        month_entry.grid(row=1, column=1, pady=5)
        
        # Day
        tk.Label(input_frame, text="Day (1-31):", bg=self.colors['bg'], fg=self.colors['text']).grid(row=2, column=0, pady=5, padx=10)
        day_var = tk.StringVar(value=str(self.special_date.day))
        day_entry = tk.Entry(input_frame, textvariable=day_var, width=10)
        day_entry.grid(row=2, column=1, pady=5)
        
        # Hour
        tk.Label(input_frame, text="Hour (0-23):", bg=self.colors['bg'], fg=self.colors['text']).grid(row=3, column=0, pady=5, padx=10)
        hour_var = tk.StringVar(value=str(self.special_date.hour))
        hour_entry = tk.Entry(input_frame, textvariable=hour_var, width=10)
        hour_entry.grid(row=3, column=1, pady=5)
        
        # Minute
        tk.Label(input_frame, text="Minute (0-59):", bg=self.colors['bg'], fg=self.colors['text']).grid(row=4, column=0, pady=5, padx=10)
        minute_var = tk.StringVar(value=str(self.special_date.minute))
        minute_entry = tk.Entry(input_frame, textvariable=minute_var, width=10)
        minute_entry.grid(row=4, column=1, pady=5)
        
        # Quick date buttons
        quick_frame = tk.Frame(settings_window, bg=self.colors['bg'])
        quick_frame.pack(pady=10)
        
        def set_quick_date(year, month, day):
            year_var.set(str(year))
            month_var.set(str(month))
            day_var.set(str(day))
            hour_var.set("0")
            minute_var.set("0")
        
        tk.Label(quick_frame, text="Quick Presets:", bg=self.colors['bg'], fg=self.colors['text']).pack()
        
        presets_frame = tk.Frame(quick_frame, bg=self.colors['bg'])
        presets_frame.pack(pady=5)
        
        tk.Button(
            presets_frame,
            text="New Year",
            command=lambda: set_quick_date(2026, 1, 1),
            bg=self.colors['accent'],
            fg=self.colors['text']
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            presets_frame,
            text="Christmas",
            command=lambda: set_quick_date(2026, 12, 25),
            bg=self.colors['accent'],
            fg=self.colors['text']
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            presets_frame,
            text="Valentine's",
            command=lambda: set_quick_date(2026, 2, 14),
            bg=self.colors['accent'],
            fg=self.colors['text']
        ).pack(side=tk.LEFT, padx=5)
        
        # Save button
        def save_settings():
            try:
                year = int(year_var.get())
                month = int(month_var.get())
                day = int(day_var.get())
                hour = int(hour_var.get())
                minute = int(minute_var.get())
                
                # Validate date
                new_date = datetime(year, month, day, hour, minute)
                
                if new_date < datetime.now():
                    response = messagebox.askyesno(
                        "Warning",
                        "This date is in the past. Are you sure you want to set it?",
                        icon='warning'
                    )
                    if not response:
                        return
                
                self.special_date = new_date
                self.save_special_date()
                self.date_info.config(
                    text=f"Target Date: {self.special_date.strftime('%B %d, %Y at %I:%M %p')}"
                )
                self.reset_timer()
                messagebox.showinfo("Success", "Special date updated successfully!")
                settings_window.destroy()
                
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for all fields!")
            except Exception as e:
                messagebox.showerror("Error", f"Invalid date: {str(e)}")
        
        save_button = tk.Button(
            settings_window,
            text="💾 Save Date",
            command=save_settings,
            bg=self.colors['fg'],
            fg=self.colors['text'],
            font=('Helvetica', 12, 'bold'),
            height=2,
            width=15
        )
        save_button.pack(pady=20)
    
    def save_special_date(self):
        """Save the special date to a file"""
        data = {
            'year': self.special_date.year,
            'month': self.special_date.month,
            'day': self.special_date.day,
            'hour': self.special_date.hour,
            'minute': self.special_date.minute
        }
        with open('special_date.json', 'w') as f:
            json.dump(data, f)
    
    def load_saved_date(self):
        """Load the special date from a file"""
        try:
            if os.path.exists('special_date.json'):
                with open('special_date.json', 'r') as f:
                    data = json.load(f)
                    self.special_date = datetime(
                        data['year'],
                        data['month'],
                        data['day'],
                        data['hour'],
                        data['minute']
                    )
        except Exception:
            # If loading fails, keep the default date
            pass

def main():
    root = tk.Tk()
    app = CountdownTimer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
