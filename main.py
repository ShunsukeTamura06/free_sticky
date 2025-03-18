import tkinter as tk
from tkinter import messagebox, simpledialog, colorchooser
import json
import os
from datetime import datetime

class StickyNote(tk.Toplevel):
    def __init__(self, master, note_id=None, text="", x=None, y=None, color="#FFFF99"):
        super().__init__(master)
        self.master = master
        self.note_id = note_id or datetime.now().strftime("%Y%m%d%H%M%S")
        self.title("付箋")
        
        # ウィンドウの設定
        self.geometry("200x200")
        self.config(bg=color)
        self.attributes("-topmost", True)
        self.resizable(True, True)
        
        # 位置の設定（指定がなければランダムに配置）
        if x is not None and y is not None:
            self.geometry(f"+{x}+{y}")
        
        # メニューバーの設定
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)
        
        # 操作メニュー
        self.action_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="操作", menu=self.action_menu)
        self.action_menu.add_command(label="色の変更", command=self.change_color)
        self.action_menu.add_command(label="削除", command=self.delete_note)
        
        # テキストエリアの設定
        self.text_area = tk.Text(self, wrap=tk.WORD, bg=color, relief=tk.FLAT, 
                                font=("メイリオ", 10))
        self.text_area.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        self.text_area.insert(tk.END, text)
        
        # イベントバインド
        self.bind("<FocusOut>", self.save_on_focus_out)
        self.bind("<Control-s>", self.save_note)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # ドラッグの設定
        self.bind("<Button-1>", self.start_drag)
        self.bind("<B1-Motion>", self.on_drag)
        
        self.drag_start_x = 0
        self.drag_start_y = 0

    def start_drag(self, event):
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def on_drag(self, event):
        x = self.winfo_x() + (event.x - self.drag_start_x)
        y = self.winfo_y() + (event.y - self.drag_start_y)
        self.geometry(f"+{x}+{y}")

    def change_color(self):
        color = colorchooser.askcolor(initialcolor=self.cget("bg"))[1]
        if color:
            self.config(bg=color)
            self.text_area.config(bg=color)
            self.save_note()

    def get_note_data(self):
        return {
            "id": self.note_id,
            "text": self.text_area.get("1.0", tk.END).strip(),
            "x": self.winfo_x(),
            "y": self.winfo_y(),
            "color": self.cget("bg")
        }

    def save_on_focus_out(self, event=None):
        self.save_note()

    def save_note(self, event=None):
        self.master.save_notes()
        return "break"  # イベントの伝播を停止

    def delete_note(self):
        if messagebox.askyesno("確認", "この付箋を削除しますか？"):
            self.master.notes.remove(self)
            self.master.save_notes()
            self.destroy()

    def on_close(self):
        self.save_note()
        self.destroy()


class StickyNoteApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("付箋アプリ")
        self.geometry("200x100")
        
        # 設定
        self.notes = []
        self.notes_file = "sticky_notes.json"
        
        # ボタン
        self.new_note_button = tk.Button(self, text="新しい付箋", command=self.create_new_note)
        self.new_note_button.pack(pady=10)
        
        self.exit_button = tk.Button(self, text="終了", command=self.on_exit)
        self.exit_button.pack(pady=5)
        
        # 保存されたノートを読み込む
        self.load_notes()
        
        # 終了時の処理
        self.protocol("WM_DELETE_WINDOW", self.on_exit)

    def create_new_note(self, note_data=None):
        if note_data:
            note = StickyNote(
                self,
                note_id=note_data.get("id"),
                text=note_data.get("text", ""),
                x=note_data.get("x"),
                y=note_data.get("y"),
                color=note_data.get("color", "#FFFF99")
            )
        else:
            note = StickyNote(self)
        
        self.notes.append(note)
        return note

    def load_notes(self):
        if os.path.exists(self.notes_file):
            try:
                with open(self.notes_file, "r", encoding="utf-8") as f:
                    notes_data = json.load(f)
                
                for note_data in notes_data:
                    self.create_new_note(note_data)
            except Exception as e:
                messagebox.showerror("エラー", f"ノートの読み込み中にエラーが発生しました: {e}")

    def save_notes(self):
        notes_data = [note.get_note_data() for note in self.notes if note.winfo_exists()]
        try:
            with open(self.notes_file, "w", encoding="utf-8") as f:
                json.dump(notes_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("エラー", f"ノートの保存中にエラーが発生しました: {e}")

    def on_exit(self):
        self.save_notes()
        self.destroy()


if __name__ == "__main__":
    app = StickyNoteApp()
    app.mainloop()