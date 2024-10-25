from customtkinter import *
import customtkinter
import os
import json
import insultinator_backend  # Rust backend module
from tkinter import filedialog

# Initialize Window
app = CTk()
app.title("Insultinator 4.0")
app.geometry("300x500")
app.resizable(False, False)

# Settings JSON file path
SETTINGS_FILE = "settings.json"

# Load or initialize settings
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as file:
            return json.load(file)
    return {"hotkey": "", "chat_key": "", "delay": 0.05}

# Save settings to JSON file
def save_settings():
    settings = {
        "hotkey": hotkey_entry.get(),
        "chat_key": chatkey_entry.get(),
        "delay": delay_slider.get()
    }
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file)

# Load insults from the selected file
def load_insult_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        insult_file_label.configure(text=os.path.basename(file_path))
        with open(file_path, "r") as file:
            return file.read()
    return ""

# Send insults using Rust backend
def send_insults():
    text = load_insult_file()
    if text:
        settings = load_settings()
        insultinator_backend.send_text_to_chat(
            text, 
            settings["chat_key"], 
            settings["delay"]
        )

# Tab setup
tabview = CTkTabview(app, width=300, height=500)
tabview.pack(pady=10)
tabview.add("Start")
tabview.add("Settings")

# Start tab for insult file selection and sending
start_frame = CTkFrame(tabview.tab("Start"))
start_frame.pack(pady=20)

insult_file_label = CTkLabel(start_frame, text="No file selected", fg_color="grey")
insult_file_label.pack(pady=5)

file_button = CTkButton(start_frame, text="Select Insult File", command=load_insult_file)
file_button.pack(pady=5)

send_button = CTkButton(start_frame, text="Send Insults", command=send_insults)
send_button.pack(pady=5)

# Settings tab
settings = load_settings()

settings_frame = CTkFrame(tabview.tab("Settings"))
settings_frame.pack(pady=20)

hotkey_label = CTkLabel(settings_frame, text="Hotkey")
hotkey_label.pack(pady=5)
hotkey_entry = CTkEntry(settings_frame)
hotkey_entry.insert(0, settings["hotkey"])
hotkey_entry.pack(pady=5)

chatkey_label = CTkLabel(settings_frame, text="Chat Key")
chatkey_label.pack(pady=5)
chatkey_entry = CTkEntry(settings_frame)
chatkey_entry.insert(0, settings["chat_key"])
chatkey_entry.pack(pady=5)

delay_label = CTkLabel(settings_frame, text="Input Delay")
delay_label.pack(pady=5)
delay_slider = CTkSlider(settings_frame, from_=0.01, to=0.1, number_of_steps=10)
delay_slider.set(settings["delay"])
delay_slider.pack(pady=5)

save_button = CTkButton(settings_frame, text="Save Settings", command=save_settings)
save_button.pack(pady=10)

app.mainloop()
