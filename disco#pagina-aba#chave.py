import random
import hashlib
import tkinter as tk
from tkinter import ttk

class KeyGenerationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulação de Geração de Chaves Privadas")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        self.generate_button = ttk.Button(root, text="Gerar Chaves Privadas", command=self.generate_private_keys)
        self.generate_button.pack()

        self.generated_keys = []
        self.keys_per_line = 40
        self.lines_per_page = 16
        self.keys_drawn = 0
        self.label = None  # Rótulo para exibir a chave privada
        self.pages = []  # Lista para armazenar as páginas

    def generate_private_keys(self):
        lower_limit = int("2000000000000000", 16)
        upper_limit = int("3FFFFFFFFFFFFFFF", 16)
        num_keys = self.keys_per_line * self.lines_per_page

        page_frame = ttk.Frame(self.notebook)
        self.pages.append(page_frame)  # Adiciona a página à lista
        self.notebook.add(page_frame, text=f"Página {len(self.pages)}")

        for _ in range(num_keys):
            private_key = hex(random.randint(lower_limit, upper_limit))[2:].zfill(64)
            self.generated_keys.append(private_key)
            self.draw_key(page_frame, private_key)
            self.keys_drawn += 1
            self.root.update()

            if self.keys_drawn >= self.keys_per_line * self.lines_per_page:
                self.keys_drawn = 0
                return

    def hash_to_color(self, sha256_hash):
        r = int(sha256_hash[:2], 16)
        g = int(sha256_hash[2:4], 16)
        b = int(sha256_hash[4:6], 16)
        return "#{:02x}{:02x}{:02x}".format(r, g, b)

    def show_key_info(self, event, private_key):
        if self.label:
            self.label.destroy()  # Destruir rótulo anterior, se existir

        block = event.widget
        current_page = self.pages[self.notebook.index(self.notebook.select())]  # Página atual
        label = tk.Label(current_page, text=private_key, bg="white", relief="solid")
        label.place(x=block.winfo_x(), y=block.winfo_y() + block.winfo_height() + 2)
        self.label = label

    def draw_key(self, page_frame, key):
        sha256_hash = hashlib.sha256(bytes.fromhex(key)).hexdigest()
        block_color = self.hash_to_color(sha256_hash)

        block_width = 20
        block_height = 20
        x = len(page_frame.winfo_children()) % self.keys_per_line * (block_width + 2)
        y = (len(page_frame.winfo_children()) // self.keys_per_line) * (block_height + 2)

        block = tk.Canvas(page_frame, width=block_width, height=block_height)
        block.create_rectangle(0, 0, block_width, block_height, fill=block_color)
        block.place(x=x, y=y)
        block.bind("<Enter>", lambda event, key=key: self.show_key_info(event, key))

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyGenerationApp(root)
    root.geometry("900x600")
    root.mainloop()
