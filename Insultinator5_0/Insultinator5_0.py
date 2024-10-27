from customtkinter import *
import customtkinter
import keyboard
from time import sleep
from threading import Thread
import os
import json
import insultinator_backend  # Import the Rust module
from insultinator_backend import send_text_to_chat

# ++++++++++++++++++++++++++++++ Creating Window ++++++++++++++++++++++++++++++++++++++
app = CTk()
app.title("Insultinator 4.0")
app.geometry("300x430")
app.resizable(False, False)
app.configure(bg="363636")

# +++++++++++++++++++++++++++++ Creating Tabs +++++++++++++++++++++++++++++++++++++++++
tab_view = customtkinter.CTkTabview(app, width=300, height=430)
tab_view.place(x=0, y=0)

tab_view.add("start")
tab_view.add("options")

# ++++++++++++++++++++++++++++++ Option Functions +++++++++++++++++++++++++++++++++++++

# Function to update the insult option menu
def update_insult_option_menu():
    global selection_option_menu
    insult_files = get_insult_files()
    insult_names = list(insult_files.keys())
    selection_option_menu.destroy()  # Destroy the existing option menu
    selection_option_menu = CTkOptionMenu(master=selection_frame, values=insult_names,
                                          fg_color="#67583b",
                                          dropdown_fg_color="#67583b",
                                          button_color="#67583b",
                                          button_hover_color="#9b8458")  # Recreate the option menu with new values
    select_label.pack_forget()  # Remove the old option menu label
    select_label.pack(anchor="n", expand=True, pady=10, padx=30)  # Repack the label to ensure it appears above the new option menu
    selection_option_menu.pack(anchor="n", expand=True, padx=30, pady=10)  # Pack the new option menu

def slider_event(value):
    print(value)

# Function to save data to a JSON file
def save_data_to_json(filename, data):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file)

# Function to load data from a JSON file
def load_data_from_json(filename):
    try:
        with open(filename, 'r') as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        return {}  # Return an empty dictionary if the file doesn't exist

# ++++++++++++++++++++++++++++++++ Option Tab +++++++++++++++++++++++++++++++++++++++++

option_frame = CTkFrame(tab_view.tab("options"), fg_color="#E8175D", border_color="#f48bae", border_width=2)
option_frame.grid(row=0, column=1, columnspan=3, padx=35, pady=30)

# ++++++++++++++++ Options Widgets ++++++++++++++++++++
spacer_label = CTkLabel(option_frame, text="")
spacer_label2 = CTkLabel(option_frame, text="")
spacer_label3 = CTkLabel(option_frame, text="")

option_label_hotkey = CTkLabel(master=option_frame, text="Insert hotkey")
option_hotkey = CTkEntry(master=option_frame)

option_label_chat = CTkLabel(master=option_frame, text="Select chat key")
option_chat_key = CTkEntry(master=option_frame)

option_label_slider = CTkLabel(master=option_frame, text="Select input speed")
option_slider = customtkinter.CTkSlider(option_frame, from_=0.01, to=0.11, number_of_steps=10)

option_button_save = CTkButton(master=option_frame, fg_color="#4258D0", text="Save")

option_label_hotkey.grid(row=0, column=1, columnspan=3, padx=10, pady=5)
option_hotkey.grid(row=1, column=1, columnspan=3, padx=10, pady=5)

spacer_label.grid(row=2, column=0, columnspan=3, padx=10)

option_label_chat.grid(row=3, column=1, columnspan=3, padx=10, pady=5)
option_chat_key.grid(row=4, column=1, columnspan=3, padx=10)

spacer_label2.grid(row=5, column=0, columnspan=3, padx=10)

option_label_slider.grid(row=6, column=1, columnspan=3, padx=10, pady=5)
option_slider.grid(row=7, column=1, columnspan=3, padx=5, pady=5)

spacer_label3.grid(row=8, column=1)

option_button_save.grid(row=9, column=1, columnspan=3, padx=10, pady=5)

# ++++++++++++++++++ Options Save +++++++++++++++++++++

# Function to save data when button is clicked
def save_data():
    data = {
        "hotkey": option_hotkey.get(),
        "chat_key": option_chat_key.get(),
        "slider_value": option_slider.get()
    }
    filename = "settings.json"
    if os.path.exists(filename):
        os.remove(filename)  # Remove the existing file
    save_data_to_json(filename, data)

option_button_save.configure(command=save_data)

# Load data when the program starts
saved_data = load_data_from_json("settings.json")
option_hotkey.insert(0, saved_data.get("hotkey", ""))
option_chat_key.insert(0, saved_data.get("chat_key", ""))
option_slider.set(saved_data.get("slider_value", 0.5))

# +++++++++++++++++++++++++++++++ Start Functions +++++++++++++++++++++++++++++++++++++

# Function to get insult files from insults folder
def get_insult_files():
    insult_files = {}
    insults_folder = "insults"
    if not os.path.exists(insults_folder):
        os.makedirs(insults_folder)
    for file in os.listdir(insults_folder):
        if file.endswith(".txt"):
            insult_name = os.path.splitext(file)[0]
            insult_files[insult_name] = os.path.join(insults_folder, file)
    return insult_files

# Modified output function to dynamically read insult files
def send_insults(insult):
    Thread(target=send_insults_thread, args=(insult,)).start()

def send_insults_thread(insult):
    try:
        chat_key = option_chat_key.get()
        insult_files = get_insult_files()
        insult_file = insult_files.get(insult)
        if insult_file is None:
            print("Insult file not found.")
            return
        
        with open(insult_file, "r") as file:
            message = file.read()
        
        delay = option_slider.get()
        send_text_to_chat(message, chat_key, delay)  # Call Rust function
        print("all done")

    except Exception as e:
        print(f"Error sending insults: {e}")

# Function to handle insult selection change
def on_insult_selection_change(event):
    insult = selection_option_menu.get()
    send_insults(insult)

# Hotkey listener thread management
hotkey_thread = None

# Modified check_hotkey function with cleanup
def check_hotkey():
    hotkey = option_hotkey.get()
    insult = selection_option_menu.get()

    # Define the function to send the insult
    def on_hotkey_pressed():
        if activation_switch.get() == 1:
            print("Hotkey detected")
            send_insults(insult)

    # Add a hotkey listener that triggers on each press
    keyboard.add_hotkey(hotkey, on_hotkey_pressed)

    # Keep running while the switch is active
    while activation_switch.get() == 1:
        sleep(0.1)  # Small delay to prevent CPU overuse

    # Remove the hotkey listener when deactivated
    keyboard.remove_hotkey(hotkey)

# Start or restart hotkey listener when activation switch is on
def test():
    global hotkey_thread

    # Stop any existing hotkey listener thread before starting a new one
    if hotkey_thread is not None and hotkey_thread.is_alive():
        activation_switch.deselect()  # Reset the switch if it was left active
        return

    # Start a new hotkey listener thread if switch is activated
    if activation_switch.get() == 1:
        hotkey_thread = Thread(target=check_hotkey)
        hotkey_thread.daemon = True  # Ensure thread exits with the program
        hotkey_thread.start()

# +++++++++++++++++++++++++++++++++ Start Tab +++++++++++++++++++++++++++++++++++++++++

# +++++++++++++++ Selection Frame +++++++++++++++++++++
selection_frame = CTkFrame(tab_view.tab("start"), fg_color="#C7AD7F", border_color="#F5F5DD", border_width=2)
selection_frame.pack(padx=35, pady=30)

# +++++++++++++++ Selection Widgets +++++++++++++++++++
select_label = CTkLabel(master=selection_frame, text="Choose insult option", text_color="#000000")
selection_option_menu = CTkOptionMenu(master=selection_frame,
                                        fg_color="#67583b",
                                        dropdown_fg_color="#67583b",
                                        button_color="#67583b",
                                        button_hover_color="#9b8458")

select_label.pack(anchor="s", expand=True, pady=5, padx=30)
selection_option_menu.pack(anchor="s", expand=True, padx=30, pady=10)

# +++++++++++++++++ Start Frame +++++++++++++++++++++++
start_frame = CTkFrame(tab_view.tab("start"), fg_color="#474747", border_color="#A8A7A7", border_width=2)
start_frame.pack(padx=35, pady=30)

# +++++++++++++++++ Start Widgets +++++++++++++++++++++
activation_label = CTkLabel(master=start_frame, text="Activate to check for hotkey")
activation_switch = CTkSwitch(master=start_frame, fg_color="#808080", progress_color="#d0ced1", text="✓", command=test)

activation_label.pack(anchor="s", expand=True, padx=20, pady=10)
activation_switch.pack(anchor="e", expand=True, padx=30, pady=10)

# ++++++++++++++++++++++++++++++++++++ Run ++++++++++++++++++++++++++++++++++++++++++++
# Bind the selection change event to the insult option menu
selection_option_menu.bind("<<ComboboxSelected>>", on_insult_selection_change)

# Add this line to update the insult option menu when the application starts
update_insult_option_menu()

app.mainloop()
