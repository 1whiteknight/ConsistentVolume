import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

APP_NAME = "ConsistentVolume"

class App:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        self.input_file = tk.StringVar()
        self.output_dir = tk.StringVar()

        self.build_ui()

    def build_ui(self):
        tk.Label(self.root, text="Audio Normalizer (ffmpeg loudnorm)", font=("Arial", 14)).pack(pady=10)

        # Input file
        frame_input = tk.Frame(self.root)
        frame_input.pack(pady=10, fill="x", padx=20)

        tk.Label(frame_input, text="Datei auswählen:").pack(anchor="w")
        tk.Entry(frame_input, textvariable=self.input_file).pack(side="left", fill="x", expand=True)
        tk.Button(frame_input, text="Durchsuchen", command=self.select_file).pack(side="right", padx=5)

        # Output folder
        frame_output = tk.Frame(self.root)
        frame_output.pack(pady=10, fill="x", padx=20)

        tk.Label(frame_output, text="Speicherort:").pack(anchor="w")
        tk.Entry(frame_output, textvariable=self.output_dir).pack(side="left", fill="x", expand=True)
        tk.Button(frame_output, text="Durchsuchen", command=self.select_folder).pack(side="right", padx=5)

        # Execute button
        tk.Button(self.root, text="Ausführen", command=self.run_ffmpeg, height=2, bg="#4CAF50", fg="white").pack(pady=20)

        # Status
        self.status = tk.Label(self.root, text="Bereit", fg="blue")
        self.status.pack(pady=10)

    def select_file(self):
        file = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav *.ogg")])
        if file:
            self.input_file.set(file)

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_dir.set(folder)

    def run_ffmpeg(self):
        input_path = self.input_file.get()
        output_path = self.output_dir.get()

        if not input_path or not os.path.isfile(input_path):
            messagebox.showerror("Fehler", "Bitte eine gültige Datei auswählen.")
            return

        if not output_path or not os.path.isdir(output_path):
            messagebox.showerror("Fehler", "Bitte einen gültigen Speicherort auswählen.")
            return

        filename = os.path.basename(input_path)
        name, ext = os.path.splitext(filename)
        output_file = os.path.join(output_path, f"norm_{name}.mp3")

        command = [
            "ffmpeg",
            "-y",
            "-i", input_path,
            "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
            output_file
        ]

        try:
            self.status.config(text="Verarbeitung läuft...", fg="orange")
            self.root.update()

            subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            self.status.config(text="Fertig: Datei gespeichert", fg="green")
            messagebox.showinfo("Erfolg", f"Datei gespeichert:\n{output_file}")

        except FileNotFoundError:
            messagebox.showerror("Fehler", "ffmpeg wurde nicht gefunden! Bitte installieren oder PATH setzen.")
        except Exception as e:
            messagebox.showerror("Fehler", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
