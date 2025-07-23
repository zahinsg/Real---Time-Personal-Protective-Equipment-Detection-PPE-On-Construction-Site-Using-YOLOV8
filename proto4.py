import tkinter as tk
from tkinter import Label, Button, filedialog
from PIL import Image, ImageTk
from ultralytics import YOLO
import torch
import cv2
import threading
import time
import requests

class PPEApp:
    def __init__(self, window):
        self.window = window
        self.window.title("PPE Detection System")
        self.window.attributes("-fullscreen", True)

        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"[INFO] Using device: {self.device}")

        self.model_path = r"C:\Users\User\Desktop\SEM 6\CSP650\FYP PROJECT\DATASET\runs\detect\train17\weights\best.pt"
        self.model = YOLO(self.model_path).to(self.device)

        # Telegram bot setup
        self.bot_token = '7655625126:AAHlQwuAOhqncVLUt-SfPClIR3P3u2u01F8'
        self.chat_id = '6115477619'
        self.required_classes = {"face-mask", "gloves", "helmet", "shoes", "safety-vest"}
        self.last_missing_time = None
        self.delay_seconds = 20

        # Canvas
        self.canvas_width = int(self.screen_width * 0.85)
        self.canvas_height = int(self.screen_height * 0.75)
        self.canvas = tk.Canvas(window, width=self.canvas_width, height=self.canvas_height, bg="black", highlightthickness=5)
        self.canvas.place(relx=0.5, rely=0.55, anchor="center")
        self.image_container = self.canvas.create_image(0, 0, anchor="nw")

        # Labels
        self.alert_label = Label(window, text="Detection Status: Not Started", font=("Arial", 18, "bold"), fg="red", bg="white")
        self.alert_label.place(relx=0.5, rely=0.05, anchor="n")

        self.missing_label = Label(window, text="", font=("Arial", 16), fg="red", bg="white")
        self.missing_label.place(relx=0.5, rely=0.15, anchor="n")

        # Control buttons
        self.button_frame = tk.Frame(window, bg="white")
        self.button_frame.place(relx=0.5, rely=0.1, anchor="n")

        Button(self.button_frame, text="Upload Image", width=16, command=self.upload_image).pack(side="left", padx=10)
        self.start_btn = Button(self.button_frame, text="Start Detection", width=16, command=self.start_camera)
        self.start_btn.pack(side="left", padx=10)
        self.stop_btn = Button(self.button_frame, text="Stop Detection", width=16, command=self.stop_camera)
        self.stop_btn.pack(side="left", padx=10)

        self.cap = None
        self.running = False

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        if not file_path:
            return
        self.alert_label.config(text="Processing Image...", fg="blue")
        threading.Thread(target=self.process_image, args=(file_path,), daemon=True).start()

    def process_image(self, file_path):
        img = cv2.imread(file_path)
        results = self.model.predict(img, imgsz=640, conf=0.3, device=self.device)
        annotated = results[0].plot()
        self.window.after(0, lambda: self.display_image(annotated))
        self.window.after(0, lambda: self.alert_label.config(text="Image Detection Complete", fg="green"))

    def start_camera(self):
        if self.running:
            return
        self.cap = cv2.VideoCapture(0)
        self.running = True
        threading.Thread(target=self.update_camera_feed, daemon=True).start()

    def stop_camera(self):
        self.running = False
        if self.cap:
            self.cap.release()
        self.alert_label.config(text="Detection Stopped", fg="red")
        self.missing_label.config(text="", fg="red")

    def update_camera_feed(self):
        prev_time = time.time()
        while self.running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            results = self.model.predict(frame, imgsz=640, conf=0.3, device=self.device)
            names = self.model.names
            detected_classes = set([names[int(cls)] for cls in results[0].boxes.cls])

            missing = self.required_classes - detected_classes
            current_time = time.time()

            if missing:
                if self.last_missing_time is None:
                    self.last_missing_time = current_time
                elif current_time - self.last_missing_time >= self.delay_seconds:
                    self.send_telegram_alert(frame, missing)
                    self.last_missing_time = current_time  # Reset timer for next alert

                status_text = f"⚠️ Missing: {', '.join(missing)}"
                status_color = "red"
            else:
                self.last_missing_time = None
                status_text = "✅ All Required PPE Present"
                status_color = "green"

            self.window.after(0, lambda: self.missing_label.config(text=status_text, fg=status_color))

            annotated = results[0].plot()
            now = time.time()
            fps = 1 / (now - prev_time)
            prev_time = now
            self.window.after(0, lambda ann=annotated, f=fps: self.display_camera_frame(ann, f))

        if self.cap:
            self.cap.release()

    def display_camera_frame(self, frame, fps):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_rgb = cv2.resize(frame_rgb, (self.canvas_width, self.canvas_height))
        image = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=image)
        self.canvas.itemconfig(self.image_container, image=imgtk)
        self.canvas.image = imgtk
        self.alert_label.config(text=f"Detection Started | FPS: {fps:.2f}", fg="green")

    def display_image(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_rgb = cv2.resize(frame_rgb, (self.canvas_width, self.canvas_height))
        image = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=image)
        self.canvas.itemconfig(self.image_container, image=imgtk)
        self.canvas.image = imgtk

    def send_telegram_alert(self, image, missing_items):
        msg = f"🚨 PPE Missing Alert!\nMissing: {', '.join(missing_items)}"
        filename = "ppe_alert.jpg"
        cv2.imwrite(filename, image)
        with open(filename, 'rb') as photo:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendPhoto"
            files = {'photo': photo}
            data = {'chat_id': self.chat_id, 'caption': msg}
            response = requests.post(url, files=files, data=data)
            print(f"[INFO] Telegram alert sent. Response: {response.status_code}")

    def on_close(self):
        self.stop_camera()
        self.window.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PPEApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))
    root.mainloop()
