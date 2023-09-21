import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from translator import PDFTranslator
from pdf2image import convert_from_path
from PIL import Image, ImageTk

class PDFRenderer:
    def __init__(self, canvas, page_label):
        self.canvas = canvas
        self.page_label = page_label
        self.images = []
        self.current_page = 0
        self.image = None

    def update_page_label(self):
        self.page_label.config(text=f"{self.current_page + 1}/{len(self.images)}")

    def load_pdf(self, file_path):
        self.images = convert_from_path(file_path, dpi=300)
        self.current_page = 0
        self.update_page_label()
        return self._display_current_page()

    def next_page(self):
        if self.current_page < len(self.images) - 1:
            self.current_page += 1
            self.update_page_label()
            return self._display_current_page()

    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_page_label()
            return self._display_current_page()

    def _display_current_page(self):
        image = self.images[self.current_page]
        width, height = image.size
        if width > 1000:
            ratio = 1000.0 / width
            width = 1000
            height = int(height * ratio)
            image = image.resize((width, height))

        self.image = ImageTk.PhotoImage(image)
        self.canvas.config(width=width, height=height)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)
        
        return width, height

class FormatNotifier:
    def __init__(self, combobox):
        self.combobox = combobox

    def check_format(self):
        selected_format = self.combobox.get()
        if selected_format == "PDF":
            messagebox.showinfo("提示", "PDF是Pro版本的功能，欢迎付费升级成Pro版本，尽享无尽PDF乐趣")
            self.combobox.set("Markdown")

class AITranslatorGUI(tk.Tk):
    def __init__(self, model):
        super().__init__()
        
        
        self.title("PDF and Markdown Viewer")
        self.translator = PDFTranslator(model)
        self.language = "中文"

        # Top Panel
        self.top_frame = ttk.Frame(self)
        self.top_frame.pack(pady=10)

        self.open_btn = ttk.Button(self.top_frame, text="打开", command=self.open_pdf)
        self.open_btn.pack(side=tk.LEFT, padx=5)

        self.prev_page_btn = ttk.Button(self.top_frame, text="上一页", command=self.prev_page)
        self.prev_page_btn.pack(side=tk.LEFT, padx=5)

        self.page_label = ttk.Label(self.top_frame, text="0/0")
        self.page_label.pack(side=tk.LEFT, padx=5)

        self.next_page_btn = ttk.Button(self.top_frame, text="下一页", command=self.next_page)
        self.next_page_btn.pack(side=tk.LEFT, padx=5)

        self.language_combobox = ttk.Combobox(self.top_frame, values=["中文", "日文","法文"], state='readonly')
        self.language_combobox.set("中文")
        self.language_combobox.pack(side=tk.LEFT, padx=10)
        self.language_combobox.bind("<<ComboboxSelected>>", self.on_language_change)

        self.format_combobox = ttk.Combobox(self.top_frame, values=["Markdown", "PDF"], state='readonly')
        self.format_combobox.set("Markdown")
        self.format_combobox.pack(side=tk.LEFT, padx=10)
        self.format_notifier = FormatNotifier(self.format_combobox)
        self.format_combobox.bind("<<ComboboxSelected>>", lambda e: self.format_notifier.check_format())

        self.translate_btn = ttk.Button(self.top_frame, text="翻译", command=self.translate_text)
        self.translate_btn.pack(side=tk.LEFT, padx=10)
        
        self.save_btn = ttk.Button(self.top_frame, text="保存", command=self.save_markdown)
        self.save_btn.pack(side=tk.LEFT, padx=5)


        # Bottom Panel
        self.bottom_frame = ttk.Frame(self)
        self.bottom_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Left Panel for PDF
        self.pdf_canvas = tk.Canvas(self.bottom_frame)
        self.pdf_canvas.pack(side=tk.LEFT, fill=tk.BOTH, padx=10)
        self.pdf_renderer = PDFRenderer(self.pdf_canvas, self.page_label)

        # Right Panel for Markdown
        self.markdown_text = tk.Text(self.bottom_frame, wrap=tk.WORD)
        self.markdown_text.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10)

    def open_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if not file_path:
            return
        
        self.file_path = file_path

        width, height = self.pdf_renderer.load_pdf(file_path)
        self.markdown_text.config(width=width, height=height)
        self.geometry(f"{2 * width}x{height + 100}")

    def prev_page(self):
        width, height = self.pdf_renderer.previous_page()
        self.markdown_text.config(width=width, height=height)
        self.geometry(f"{2 * width}x{height + 100}")

    def next_page(self):
        width, height = self.pdf_renderer.next_page()
        self.markdown_text.config(width=width, height=height)
        self.geometry(f"{2 * width}x{height + 100}")

    def save_markdown(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".md", filetypes=[("Markdown files", "*.md")])
        if not file_path:
            return
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(self.markdown_text.get(1.0, tk.END))

    def translate_text(self):
        translated_text = self.translator.translate_pdf_to_string(self.file_path, "markdown",target_language = self.language)
        self.markdown_text.delete(1.0, tk.END)
        self.markdown_text.insert(tk.END, translated_text)
        
    def on_language_change(self, event):
        self.language = self.language_combobox.get()

if __name__ == "__main__":
    app = AITranslatorGUI()
    app.mainloop()
