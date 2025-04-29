import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import subprocess
import threading
import re
import json


class FFmpegCompressorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Compressor")
        self.root.resizable(False, False)
        self.root.grid_columnconfigure(1, weight=1)

        # Variables
        self.input_file = tk.StringVar()
        self.output_file = tk.StringVar()
        self.crf_value = tk.StringVar(value="23")
        self.output_dir = tk.StringVar()
        self.speed_multiplier = tk.StringVar(value="1.0")
        self.remove_audio = tk.BooleanVar(value=False)
        self.start_time = tk.StringVar()
        self.end_time = tk.StringVar()
        self.process = None
        self.total_duration = 0
        self.is_compressing = False

        # Group 1: Input/Output
        tk.Label(root, text="Input Video:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        tk.Entry(root, textvariable=self.input_file, width=50).grid(row=0, column=1, padx=10, pady=5)
        tk.Button(root, text="Browse", command=self.browse_input, width=10).grid(row=0, column=2, padx=10, pady=5)

        tk.Label(root, text="Output Directory:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        tk.Entry(root, textvariable=self.output_dir, width=50).grid(row=1, column=1, padx=10, pady=5)
        tk.Button(root, text="Browse", command=self.browse_output_dir, width=10).grid(row=1, column=2, padx=10, pady=5)

        tk.Label(root, text="Output File Name:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        tk.Entry(root, textvariable=self.output_file, width=50).grid(row=2, column=1, padx=10, pady=5)

        # Separator 1
        ttk.Separator(root, orient="horizontal").grid(row=3, column=0, columnspan=4, padx=(10, 10), pady=10, sticky="ew")

        # Container Frame for Group 2 and Group 3 (side-by-side)
        container_frame = tk.Frame(root)
        container_frame.grid(row=4, column=0, columnspan=4, padx=10, pady=5, sticky="ew")
        container_frame.grid_columnconfigure(0, weight=1)
        container_frame.grid_columnconfigure(2, weight=1)
        container_frame.grid_rowconfigure(0, weight=1)

        # Left Frame: Group 2 (Compression Settings)
        left_frame = tk.Frame(container_frame)
        left_frame.grid(row=0, column=0, sticky="nsew")
        left_frame.grid_columnconfigure(1, weight=1)
        for i in range(3):
            left_frame.grid_rowconfigure(i, weight=1)
        tk.Label(left_frame, text="CRF Value (lower value leads to higher quality):").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        tk.Entry(left_frame, textvariable=self.crf_value, width=10).grid(row=0, column=1, padx=10, pady=5, sticky="w")
        tk.Label(left_frame, text="Speed Multiplier (e.g., 1.0, 2.0):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        tk.Entry(left_frame, textvariable=self.speed_multiplier, width=10).grid(row=1, column=1, padx=10, pady=5, sticky="w")
        tk.Checkbutton(left_frame, text="Remove Audio", variable=self.remove_audio).grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        # Vertical Separator
        ttk.Separator(container_frame, orient="vertical").grid(row=0, column=1, padx=10, sticky="ns")

        # Right Frame: Group 3 (Clipping)
        right_frame = tk.Frame(container_frame)
        right_frame.grid(row=0, column=2, sticky="nsew")
        right_frame.grid_columnconfigure(1, weight=1)
        tk.Label(right_frame, text="Start Time (HH:MM:SS):").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        tk.Entry(right_frame, textvariable=self.start_time, width=10).grid(row=0, column=1, padx=10, pady=5, sticky="w")
        tk.Label(right_frame, text="End Time (HH:MM:SS):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        tk.Entry(right_frame, textvariable=self.end_time, width=10).grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Separator 2
        ttk.Separator(root, orient="horizontal").grid(row=5, column=0, columnspan=4, padx=(10, 10), pady=10, sticky="ew")

        # Group 4: Controls and Output
        self.status_label = tk.Label(root, text="Please press the Compress button to start compressing the video", fg="blue")
        self.status_label.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        self.compress_button = tk.Button(root, text="Compress", command=self.start_compression, width=10)
        self.compress_button.grid(row=6, column=2, padx=10, pady=5, sticky="w")

        self.cancel_button = tk.Button(root, text="Cancel", command=self.cancel_compression, state="disabled", width=10)
        self.cancel_button.grid(row=7, column=2, padx=10, pady=5, sticky="w")

        self.progress = ttk.Progressbar(root, mode="determinate")
        self.progress.grid(row=7, column=0, columnspan=2, padx=(10, 10), pady=5, sticky="ew")

        self.log_text = tk.Text(root, height=10, state="disabled")
        self.log_text.grid(row=8, column=0, columnspan=3, padx=(10, 10), pady=5, sticky="ew")
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.log_text.yview)
        scrollbar.grid(row=8, column=3, sticky="ns")
        self.log_text.configure(yscrollcommand=scrollbar.set)

    def parse_time(self, time_str):
        """Convert HH:MM:SS to seconds, return None if invalid."""
        if not time_str:
            return None
        if not re.match(r"^\d{2}:\d{2}:\d{2}$", time_str):
            return None
        try:
            hours, minutes, seconds = map(int, time_str.split(":"))
            if minutes >= 60 or seconds >= 60:
                return None
            return hours * 3600 + minutes * 60 + seconds
        except ValueError:
            return None

    def browse_input(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mkv *.mov")])
        if file_path:
            self.input_file.set(file_path)
            input_filename = os.path.basename(file_path)
            default_output = os.path.splitext(input_filename)[0] + "_compress.mp4"
            self.output_file.set(default_output)
            self.output_dir.set(os.path.dirname(file_path))
            self.total_duration = self.get_video_duration(file_path)

    def browse_output_dir(self):
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.output_dir.set(dir_path)

    def validate_inputs(self):
        if not os.path.exists(self.input_file.get()):
            messagebox.showerror("Error", "Input file does not exist!")
            return False
        if not os.path.isdir(self.output_dir.get()):
            messagebox.showerror("Error", "Output directory does not exist!")
            return False
        if not self.output_file.get():
            messagebox.showerror("Error", "Please provide an output file name!")
            return False
        try:
            crf = int(self.crf_value.get())
            if not 0 <= crf <= 51:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "CRF value must be a number between 0 and 51!")
            return False
        try:
            speed = float(self.speed_multiplier.get())
            if speed <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Speed multiplier must be a positive number!")
            return False

        # Validate start and end times
        start_secs = self.parse_time(self.start_time.get())
        end_secs = self.parse_time(self.end_time.get())
        if self.start_time.get() and start_secs is None:
            messagebox.showerror("Error", "Start time must be in HH:MM:SS format!")
            return False
        if self.end_time.get() and end_secs is None:
            messagebox.showerror("Error", "End time must be in HH:MM:SS format!")
            return False
        if start_secs is not None and end_secs is not None:
            if start_secs >= end_secs:
                messagebox.showerror("Error", "Start time must be less than end time!")
                return False
            if self.total_duration > 0 and end_secs > self.total_duration:
                messagebox.showerror("Error", "End time exceeds video duration!")
                return False
        elif start_secs is not None and self.end_time.get():
            messagebox.showerror("Error", "Invalid end time format!")
            return False
        elif end_secs is not None and self.start_time.get():
            messagebox.showerror("Error", "Invalid start time format!")
            return False
        return True

    def get_video_duration(self, file_path):
        try:
            cmd = [
                "ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "json", file_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            data = json.loads(result.stdout)
            return float(data["format"]["duration"])
        except (subprocess.CalledProcessError, FileNotFoundError, KeyError):
            messagebox.showwarning("Warning", "Could not determine video duration. Progress bar may not work.")
            return 0

    def parse_ffmpeg_time(self, time_str):
        parts = time_str.split(":")
        seconds = 0
        if len(parts) == 3:
            seconds = int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
        elif len(parts) == 2:
            seconds = int(parts[0]) * 60 + float(parts[1])
        return seconds

    def update_log(self, text):
        self.log_text.configure(state="normal")
        self.log_text.insert(tk.END, text)
        self.log_text.see(tk.END)
        self.log_text.configure(state="disabled")

    def compress_video(self):
        output_path = os.path.join(self.output_dir.get(), self.output_file.get())
        ffmpeg_cmd = ["ffmpeg", "-y"]

        # Add clipping parameters if provided
        start_secs = self.parse_time(self.start_time.get())
        end_secs = self.parse_time(self.end_time.get())
        if start_secs is not None:
            ffmpeg_cmd.extend(["-ss", self.start_time.get()])
        if end_secs is not None:
            ffmpeg_cmd.extend(["-to", self.end_time.get()])

        ffmpeg_cmd.extend(["-i", self.input_file.get(), "-c:v", "libx264", "-preset", "veryslow", "-crf", self.crf_value.get()])

        # Add speed multiplier
        speed = float(self.speed_multiplier.get())
        if speed != 1.0:
            ffmpeg_cmd.extend(["-vf", f"setpts=PTS/{speed}"])

        # Handle audio
        if self.remove_audio.get():
            ffmpeg_cmd.append("-an")
        else:
            if speed != 1.0:
                ffmpeg_cmd.extend(["-filter:a", f"atempo={speed}"])
            else:
                ffmpeg_cmd.extend(["-c:a", "copy"])

        # Ensure correct duration
        ffmpeg_cmd.extend(["-shortest", output_path])

        # Adjust duration for progress bar
        if start_secs is not None and end_secs is not None:
            adjusted_duration = (end_secs - start_secs) / speed if speed > 0 else 0
        else:
            adjusted_duration = self.total_duration / speed if self.total_duration > 0 and speed > 0 else 0

        try:
            self.process = subprocess.Popen(
                ffmpeg_cmd, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='replace'
            )
            self.is_compressing = True

            time_regex = re.compile(r"time=(\d{2}:\d{2}:\d{2}\.\d{2})")
            while self.process.poll() is None:
                line = self.process.stderr.readline()
                if line:
                    self.root.after(0, lambda t=line: self.update_log(t))
                match = time_regex.search(line)
                if match and adjusted_duration > 0:
                    current_time = self.parse_ffmpeg_time(match.group(1))
                    progress = min((current_time / adjusted_duration) * 100, 100)
                    self.root.after(0, lambda: [
                        self.progress.config(value=progress),
                        self.status_label.config(text=f"Progress: {int(progress)}%", fg="blue")
                    ])

            if not self.is_compressing:
                self.root.after(0, lambda: [
                    self.status_label.config(text="Compression canceled!", fg="orange"),
                    self.progress.config(value=0),
                    self.compress_button.config(state="normal"),
                    self.cancel_button.config(state="disabled"),
                    self.update_log("Compression canceled.\n"),
                    self.status_label.config(text="Please press the Compress button to start compressing the video", fg="blue")
                ])
                return

            if self.process.returncode == 0:
                self.root.after(0, lambda: [
                    self.status_label.config(text="Compression completed!", fg="green"),
                    messagebox.showinfo("Success", f"Video compressed successfully!\nOutput saved to: {output_path}"),
                    self.progress.config(value=100),
                    self.compress_button.config(state="normal"),
                    self.cancel_button.config(state="disabled"),
                    self.update_log("Compression completed successfully.\n"),
                    self.status_label.config(text="Please press the Compress button to start compressing the video", fg="blue")
                ])
            else:
                error_output = self.process.stderr.read()
                self.root.after(0, lambda: [
                    self.status_label.config(text="Compression failed!", fg="red"),
                    messagebox.showerror("Error", f"FFmpeg error: {error_output}"),
                    self.progress.config(value=0),
                    self.compress_button.config(state="normal"),
                    self.cancel_button.config(state="disabled"),
                    self.update_log(f"Error: {error_output}\n"),
                    self.status_label.config(text="Please press the Compress button to start compressing the video", fg="blue")
                ])

        except FileNotFoundError:
            self.root.after(0, lambda: [
                self.status_label.config(text="FFmpeg not found!", fg="red"),
                messagebox.showerror("Error", "FFmpeg not found. Please ensure FFmpeg is installed and added to PATH."),
                self.progress.config(value=0),
                self.compress_button.config(state="normal"),
                self.cancel_button.config(state="disabled"),
                self.update_log("FFmpeg not found.\n"),
                self.status_label.config(text="Please press the Compress button to start compressing the video", fg="blue")
            ])
        finally:
            self.is_compressing = False
            self.process = None

    def start_compression(self):
        if not self.validate_inputs():
            return
        output_path = os.path.join(self.output_dir.get(), self.output_file.get())
        if os.path.exists(output_path):
            if not messagebox.askyesno("File Exists", f"The file {output_path} already exists. Overwrite?"):
                self.status_label.config(text="Compression aborted by user.", fg="orange")
                self.status_label.config(text="Please press the Compress button to start compressing the video", fg="blue")
                return
        self.log_text.configure(state="normal")
        self.log_text.delete(1.0, tk.END)
        self.log_text.configure(state="disabled")
        self.compress_button.config(state="disabled")
        self.cancel_button.config(state="normal")
        self.status_label.config(text="Progress: 0%", fg="blue")
        self.progress.config(value=0)
        threading.Thread(target=self.compress_video, daemon=True).start()

    def cancel_compression(self):
        if self.process and self.is_compressing:
            self.is_compressing = False
            self.process.terminate()
            try:
                self.process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.process.kill()


if __name__ == "__main__":
    root = tk.Tk()
    app = FFmpegCompressorApp(root)
    root.mainloop()
