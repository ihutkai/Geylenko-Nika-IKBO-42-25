"""Графический интерфейс эмулятора UNIX-оболочки, этап 1."""

import tkinter as tk
from tkinter import scrolledtext
from pathlib import Path

from config import load_settings
from shell import execute
from startup import run_startup


class ShellWindow:
    """Окно с историей диалога и строкой ввода команд."""

    def __init__(self, root: tk.Tk, vfs_name: str = "demo-vfs"):
        self.root = root
        root.title(f"Эмулятор оболочки — VFS: {vfs_name}")
        root.geometry("800x480")
        self.output = scrolledtext.ScrolledText(
            root, state="disabled", font=("Consolas", 12),
            background="#18212b", foreground="#e6edf3", wrap="word",
        )
        self.output.pack(fill="both", expand=True, padx=10, pady=10)
        row = tk.Frame(root)
        row.pack(fill="x", padx=10, pady=(0, 10))
        tk.Label(row, text="$", font=("Consolas", 12)).pack(side="left")
        self.entry = tk.Entry(row, font=("Consolas", 12))
        self.entry.pack(side="left", fill="x", expand=True)
        self.entry.bind("<Return>", self.submit)
        self.entry.focus_set()
        self.write("Этап 2. Команды: ls [путь], cd [путь], exit.")

    def write(self, text: str) -> None:
        """Добавить текст в защищённую от редактирования историю."""
        self.output.configure(state="normal")
        self.output.insert("end", text + "\n")
        self.output.configure(state="disabled")
        self.output.see("end")

    def submit(self, event=None) -> None:
        """Показать введённую команду и результат её выполнения."""
        line = self.entry.get()
        self.entry.delete(0, "end")
        self.write(f"$ {line}")
        result = execute(line)
        if result.text:
            self.write(result.text)
        if result.should_exit:
            self.root.destroy()


def main() -> None:
    """Создать окно и запустить цикл событий Tkinter."""
    settings = load_settings()
    root = tk.Tk()
    window = ShellWindow(root, Path(settings.vfs_path).name)
    for name, value in vars(settings).items():
        message = f"Настройка {name} = {value!r}"
        print(message)
        window.write(message)
    if settings.startup_script:
        def start_script():
            if run_startup(settings.startup_script, window.write):
                root.destroy()
        root.after(100, start_script)
    root.mainloop()


if __name__ == "__main__":
    main()
