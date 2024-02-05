import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ExifTags
import os
import json

# Laden der Benutzerdaten aus einer Konfigurationsdatei
def load_user_credentials():
    with open("user_credentials.json", "r") as file:
        return json.load(file)

# Funktion zum Quadratischmachen der Bilder
def adjust_image_size(directory):
    output_directory = os.path.join(directory, "adjusted_images")
    os.makedirs(output_directory, exist_ok=True)
    
    for file in os.listdir(directory):
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(directory, file)
            output_path = os.path.join(output_directory, file)
            
            with Image.open(image_path) as img:
                width, height = img.size
                new_size = max(width, height, 800)
                new_img = Image.new("RGB", (new_size, new_size), "white")
                new_img.paste(img, ((new_size - width) // 2, (new_size - height) // 2))
                new_img.save(output_path, "JPEG", quality=95)

# Hauptfenster
def main_window():
    window = tk.Tk()
    window.title("Bildbearbeitungsprogramm")
    window.geometry("800x600")

    def select_directory():
        directory = filedialog.askdirectory()
        if directory:
            adjust_image_size(directory)
            messagebox.showinfo("Erfolg", "Bilder wurden bearbeitet.")

    tk.Button(window, text="Ordner wählen und bearbeiten", command=select_directory).pack()
    window.mainloop()

# Anmeldefenster
def show_login_window(users):
    def attempt_login():
        user = users.get(username.get())
        if user and user == password.get():
            main_window()
            login_win.destroy()
        else:
            messagebox.showwarning("Fehler", "Falscher Benutzername oder Passwort")

    login_win = tk.Tk()
    login_win.title("Login")

    tk.Label(login_win, text="Benutzername:").pack()
    username = tk.Entry(login_win)
    username.pack()

    tk.Label(login_win, text="Passwort:").pack()
    password = tk.Entry(login_win, show="*")
    password.pack()

    tk.Button(login_win, text="Login", command=attempt_login).pack()
    login_win.mainloop()

# Start des Programms
if __name__ == "__main__":
    user_credentials = load_user_credentials()
    show_login_window(user_credentials)