import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import time
import os


class PresentationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Presentation Viewer")
        self.root.configure(bg="black")

        # Canvas para exibir imagens
        self.canvas = tk.Canvas(root, bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Botão para carregar o arquivo .presentation
        self.load_button = tk.Button(
            root,
            text="Load .presentation File",
            bg="black",
            fg="white",
            command=self.load_presentation_file
        )
        self.load_button.pack(pady=10)

        # Variáveis para controlar a apresentação
        self.image_files = []
        self.current_index = 0
        self.running = False

    def load_presentation_file(self):
        presentation_path = filedialog.askopenfilename(filetypes=[("Presentation Files", "*.presentation")])
        if not presentation_path:
            return

        try:
            # Ler o arquivo .presentation
            with open(presentation_path, "r") as file:
                self.image_files = [line.strip() for line in file.readlines()]

            # Validar os arquivos de imagem
            self.image_files = [f for f in self.image_files if os.path.exists(f) and f.lower().endswith(".bmp")]

            if not self.image_files:
                messagebox.showerror("Error", "No valid .bmp files found in the .presentation file.")
                return

            # Iniciar a apresentação
            self.current_index = 0
            self.running = True
            self.show_next_slide()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load .presentation file: {e}")

    def show_next_slide(self):
        if not self.running or self.current_index >= len(self.image_files):
            return

        image_path = self.image_files[self.current_index]

        try:
            # Carregar e exibir a imagem
            image = Image.open(image_path)
            photo = ImageTk.PhotoImage(image)
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            self.canvas.image = photo

            # Avançar para o próximo slide após 2 segundos
            self.current_index += 1
            self.root.after(2000, self.show_next_slide)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to display image: {e}")
            self.running = False


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('640x480')
    app = PresentationApp(root)
    root.mainloop()

