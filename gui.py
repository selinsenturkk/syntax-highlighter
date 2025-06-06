import tkinter as tk
from lexer import tokenize
from parser import Parser

# Token tiplerine göre renkler
TOKEN_COLORS = {
    "KEYWORD": "blue",
    "IDENTIFIER": "purple",
    "NUMBER": "green",
    "OPERATOR": "red",
    "DELIMITER": "darkorange",
    "COMMENT": "gray",
}

class SyntaxHighlighterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Syntax Highlighter IDE")

        self.frame = tk.Frame(root)
        self.frame.pack(expand=True, fill="both")

        self.line_numbers = tk.Text(self.frame, width=4, padx=5, takefocus=0, border=0,
                                    background="#f0f0f0", state="disabled", font=("Consolas", 14))
        self.line_numbers.pack(side="left", fill="y")

        self.text = tk.Text(self.frame, font=("Consolas", 14), wrap="none", undo=True)
        self.text.pack(side="right", expand=True, fill="both")

        self.text.bind("<KeyRelease>", self.on_key_release)
        self.text.bind("<MouseWheel>", self.sync_scroll)
        self.text.bind("<Button-1>", self.sync_scroll)
        self.text.bind("<Return>", self.sync_scroll)
        self.text.bind("<BackSpace>", self.sync_scroll)
        self.text.bind("<Configure>", self.sync_scroll)
        self.text.bind("<Motion>", self.sync_scroll)
        self.text.bind("<ButtonRelease-1>", self.sync_scroll)
        self.text.bind("<MouseWheel>", self.sync_scroll)

        # Renkleri ayarla
        for token_type in TOKEN_COLORS:
            self.text.tag_config(token_type, foreground=TOKEN_COLORS[token_type])
        self.text.tag_config("ERROR_LINE", background="mistyrose")

        self.update_line_numbers()

    def sync_scroll(self, event=None):
        self.update_line_numbers()

    def update_line_numbers(self):
        self.line_numbers.config(state="normal")
        self.line_numbers.delete("1.0", tk.END)

        line_count = int(self.text.index("end-1c").split(".")[0])
        line_numbers_str = "\n".join(str(i) for i in range(1, line_count + 1))
        self.line_numbers.insert("1.0", line_numbers_str)
        self.line_numbers.config(state="disabled")

    def on_key_release(self, event=None):
        code = self.text.get("1.0", tk.END)
        self.update_line_numbers()
        self.highlight(code)

        tokens = tokenize(code)
        parser = Parser(tokens)
        if parser.parse():
            self.root.title("Syntax Highlighter IDE - Geçerli Sözdizimi")
            self.text.tag_remove("ERROR_LINE", "1.0", tk.END)
        else:
            self.root.title("Syntax Highlighter IDE - Hatali Sözdizimi")
            line = parser.error_line
            if line is not None:
                self.highlight_error_line(line)

    def highlight(self, code):
        for tag in list(TOKEN_COLORS.keys()) + ["ERROR_LINE"]:
            self.text.tag_remove(tag, "1.0", tk.END)

        tokens = tokenize(code)
        for token_type, value, pos, line, col in tokens:
            start = f"1.0 + {pos} chars"
            end = f"1.0 + {pos + len(value)} chars"
            if token_type in TOKEN_COLORS:
                self.text.tag_add(token_type, start, end)

    def highlight_error_line(self, line_number):
        self.text.tag_remove("ERROR_LINE", "1.0", tk.END)
        try:
            start = f"{line_number}.0"
            end = f"{line_number}.end"
            self.text.tag_add("ERROR_LINE", start, end)
        except Exception as e:
            print(f"Hata satirinda isaretleme sorunu: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SyntaxHighlighterApp(root)
    root.mainloop() 