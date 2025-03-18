import tkinter as tk
from tkinter import messagebox, simpledialog, colorchooser, ttk
import json
import os
from datetime import datetime
import random

class StickyNote(tk.Toplevel):
    def __init__(self, master, note_id=None, text="", x=None, y=None, color="#FFFF99"):
        super().__init__(master)
        self.master = master
        self.note_id = note_id or datetime.now().strftime("%Y%m%d%H%M%S")
        
        # タイトルバーを非表示に統一
        self.overrideredirect(True)
        
        # ウィンドウの設定
        self.geometry("200x200")
        self.config(bg=color)
        self.attributes("-topmost", True)
        self.resizable(True, True)
        
        # 位置の設定（指定がなければランダムに配置）
        if x is not None and y is not None:
            self.geometry(f"+{x}+{y}")
        else:
            # ランダムな位置を設定（画面内に収まるように）
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            random_x = random.randint(50, screen_width - 250)
            random_y = random.randint(50, screen_height - 250)
            self.geometry(f"+{random_x}+{random_y}")
        
        # コントロールフレーム（ヘッダー代わり）の作成
        self.control_frame = tk.Frame(self, bg=color, height=20)
        self.control_frame.pack(fill=tk.X, side=tk.TOP)
        
        # 閉じるボタン
        self.close_button = tk.Label(self.control_frame, text="×", bg=color, 
                                    fg="#555555", font=("Arial", 10, "bold"))
        self.close_button.pack(side=tk.RIGHT, padx=5)
        self.close_button.bind("<Button-1>", lambda e: self.on_close())
        
        # 設定ボタン
        self.settings_button = tk.Label(self.control_frame, text="⚙", bg=color, 
                                      fg="#555555", font=("Arial", 10, "bold"))
        self.settings_button.pack(side=tk.RIGHT, padx=5)
        self.settings_button.bind("<Button-1>", self.show_context_menu)
        
        # ドラッグ用のハンドル
        self.drag_label = tk.Label(self.control_frame, text="≡", bg=color, 
                                  fg="#555555", font=("Arial", 10, "bold"))
        self.drag_label.pack(side=tk.LEFT, padx=5)
        self.drag_label.bind("<Button-1>", self.start_drag)
        self.drag_label.bind("<B1-Motion>", self.on_drag)
        
        # サイズ変更ハンドル（右下隅）
        self.resize_frame = tk.Frame(self, bg=color, cursor="sizing")
        self.resize_frame.place(relx=1.0, rely=1.0, anchor="se", width=15, height=15)
        self.resize_frame.bind("<Button-1>", self.start_resize)
        self.resize_frame.bind("<B1-Motion>", self.on_resize)
        
        # テキストエリアの設定
        self.text_area = tk.Text(self, wrap=tk.WORD, bg=color, relief=tk.FLAT, 
                               font=("Yu Gothic UI", 10), bd=2)
        self.text_area.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        self.text_area.insert(tk.END, text)
        
        # コンテキストメニュー（右クリックメニュー）
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="色の変更", command=self.change_color)
        self.context_menu.add_command(label="閉じる", command=self.on_close)
        
        # サイズ変更用の変数
        self.resize_start_x = 0
        self.resize_start_y = 0
        self.resize_start_width = 0 
        self.resize_start_height = 0
        
        # イベントバインド
        self.bind("<FocusOut>", self.save_on_focus_out)
        self.bind("<Control-s>", self.save_note)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.text_area.bind("<Button-3>", self.show_context_menu)  # 右クリック
        
        # テキストエリアでのドラッグを無効化（テキスト編集のため）
        self.text_area.bind("<Button-1>", lambda e: self.text_area.focus_set())
        
        self.drag_start_x = 0
        self.drag_start_y = 0
        
    def start_resize(self, event):
        """ウィンドウのリサイズ開始"""
        self.resize_start_x = event.x_root
        self.resize_start_y = event.y_root
        self.resize_start_width = self.winfo_width()
        self.resize_start_height = self.winfo_height()
    
    def on_resize(self, event):
        """ウィンドウのリサイズ処理"""
        # 最小サイズを確保
        new_width = max(100, self.resize_start_width + (event.x_root - self.resize_start_x))
        new_height = max(100, self.resize_start_height + (event.y_root - self.resize_start_y))
        
        self.geometry(f"{new_width}x{new_height}")

    def show_context_menu(self, event=None):
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

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
            self.control_frame.config(bg=color)
            self.close_button.config(bg=color)
            self.settings_button.config(bg=color)
            self.drag_label.config(bg=color)
            self.resize_frame.config(bg=color)
            self.save_note()
            # 選択されている場合、リスト表示も更新
            self.master.update_note_in_list(self.note_id)

    # toggle_title_bar メソッドを削除（ヘッダーなしに統一したため）

    def get_note_data(self):
        return {
            "id": self.note_id,
            "text": self.text_area.get("1.0", tk.END).strip(),
            "x": self.winfo_x(),
            "y": self.winfo_y(),
            "width": self.winfo_width(),
            "height": self.winfo_height(),
            "color": self.cget("bg"),
            "is_open": True  # 付箋が開いている状態を記録
        }

    def save_on_focus_out(self, event=None):
        self.save_note()

    def save_note(self, event=None):
        self.master.save_notes()
        # マスターのリストビューを更新
        self.master.update_note_in_list(self.note_id)
        return "break"  # イベントの伝播を停止

    def on_close(self):
        # 付箋を閉じる（削除ではなく）
        self.save_note()
        # リストビューの状態を更新
        note_data = self.get_note_data()
        note_data["is_open"] = False
        self.master.update_closed_note(note_data)
        self.destroy()


class StickyNoteApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("付箋管理アプリ")
        self.geometry("600x500")
        self.configure(bg="#f0f0f0")
        
        # タイトルバーを非表示（ヘッダーなしに統一）
        self.overrideredirect(True)
        
        # アイコン設定（リソースがあれば）
        try:
            self.iconbitmap("sticky_note_icon.ico")
        except:
            pass
        
        # スタイル設定
        self.style = ttk.Style()
        self.style.theme_use('clam')  # または 'alt', 'default', 'classic'
        
        # ボタンスタイルのカスタマイズ
        self.style.configure('TButton', 
                           font=('Yu Gothic UI', 10),
                           borderwidth=1,
                           focusthickness=3,
                           focuscolor='none')
        
        self.style.map('TButton',
                     background=[('active', '#e1e1e1'), ('pressed', '#d0d0d0')],
                     relief=[('pressed', 'sunken')])
        
        # タブスタイルのカスタマイズ
        self.style.configure('TNotebook.Tab', 
                           font=('Yu Gothic UI', 10),
                           padding=[10, 4])
        
        # ヘッダーフレーム（タイトルバー代わり）
        header_frame = tk.Frame(self, bg="#4a86e8", height=30)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        
        # タイトル
        header_label = tk.Label(header_frame, text="付箋管理アプリ", font=("Yu Gothic UI", 12, "bold"), 
                              bg="#4a86e8", fg="white")
        header_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # ドラッグ用のバインド
        header_frame.bind("<Button-1>", self.start_move)
        header_frame.bind("<B1-Motion>", self.on_move)
        
        # 閉じるボタン
        close_button = tk.Label(header_frame, text="×", bg="#4a86e8", fg="white", 
                             font=("Arial", 12, "bold"))
        close_button.pack(side=tk.RIGHT, padx=10)
        close_button.bind("<Button-1>", lambda e: self.on_exit())
        
        # 最小化ボタン
        minimize_button = tk.Label(header_frame, text="_", bg="#4a86e8", fg="white", 
                               font=("Arial", 12, "bold"))
        minimize_button.pack(side=tk.RIGHT, padx=5)
        minimize_button.bind("<Button-1>", lambda e: self.iconify())
        
        # 設定
        self.notes = []  # 開いている付箋のリスト
        self.all_notes = []  # すべての付箋データ
        self.notes_file = "sticky_notes.json"
        
        # メインフレーム（上下分割）
        self.paned_window = ttk.PanedWindow(self, orient=tk.VERTICAL)
        self.paned_window.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # リストフレーム（上部）
        self.list_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(self.list_frame, weight=2)
        
        # タブコントロール
        self.notebook = ttk.Notebook(self.list_frame)
        self.notebook.pack(expand=True, fill=tk.BOTH)
        
        # 付箋リストタブ
        self.notes_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.notes_tab, text="すべての付箋")
        
        # ツールバー
        toolbar_frame = ttk.Frame(self.notes_tab)
        toolbar_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 付箋リストのツールバーボタン
        self.new_button = ttk.Button(toolbar_frame, text="新規作成", command=self.create_new_note)
        self.new_button.pack(side=tk.LEFT, padx=2)
        
        self.open_button = ttk.Button(toolbar_frame, text="開く", command=self.open_selected_note)
        self.open_button.pack(side=tk.LEFT, padx=2)
        
        self.delete_button = ttk.Button(toolbar_frame, text="削除", command=self.delete_selected_note)
        self.delete_button.pack(side=tk.LEFT, padx=2)
        
        self.color_button = ttk.Button(toolbar_frame, text="色変更", command=self.change_selected_note_color)
        self.color_button.pack(side=tk.LEFT, padx=2)
        
        self.refresh_button = ttk.Button(toolbar_frame, text="更新", command=self.refresh_note_list)
        self.refresh_button.pack(side=tk.RIGHT, padx=2)
        
        # 検索フレーム
        search_frame = ttk.Frame(self.notes_tab)
        search_frame.pack(fill=tk.X, padx=5, pady=2)
        
        search_label = ttk.Label(search_frame, text="検索:")
        search_label.pack(side=tk.LEFT, padx=2)
        
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda name, index, mode: self.filter_notes())
        
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        clear_button = ttk.Button(search_frame, text="✕", width=3, 
                                command=lambda: self.search_var.set(""))
        clear_button.pack(side=tk.RIGHT, padx=2)
        
        # リストビューフレーム
        list_view_frame = ttk.Frame(self.notes_tab)
        list_view_frame.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        
        # ツリービュー（リスト表示）のカラム設定
        self.tree = ttk.Treeview(list_view_frame, columns=("id", "date", "preview", "status"), 
                              show="headings", selectmode="browse")
        
        # カラム設定
        self.tree.heading("id", text="ID")
        self.tree.heading("date", text="日時")
        self.tree.heading("preview", text="内容")
        self.tree.heading("status", text="状態")
        
        self.tree.column("id", width=80, anchor="w")
        self.tree.column("date", width=140, anchor="w")
        self.tree.column("preview", width=250, anchor="w")
        self.tree.column("status", width=80, anchor="center")
        
        # スクロールバー
        scrollbar = ttk.Scrollbar(list_view_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # 配置
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        
        # ダブルクリックイベント
        self.tree.bind("<Double-1>", lambda e: self.open_selected_note())
        # 右クリックメニュー
        self.tree.bind("<Button-3>", self.show_tree_context_menu)
        
        # プレビューフレーム（下部）
        self.preview_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(self.preview_frame, weight=1)
        
        # プレビューラベル
        preview_label = ttk.Label(self.preview_frame, text="プレビュー:", font=("Yu Gothic UI", 10, "bold"))
        preview_label.pack(anchor="w", padx=5, pady=2)
        
        # プレビューテキスト
        self.preview_text = tk.Text(self.preview_frame, wrap=tk.WORD, height=5, 
                                  font=("Yu Gothic UI", 10), state="disabled")
        self.preview_text.pack(expand=True, fill=tk.BOTH, padx=5, pady=2)
        
        # ツリービューの選択イベント
        self.tree.bind("<<TreeviewSelect>>", self.update_preview)
        
        # コンテキストメニュー
        self.context_menu = tk.Menu(self.tree, tearoff=0)
        self.context_menu.add_command(label="開く", command=self.open_selected_note)
        self.context_menu.add_command(label="色変更", command=self.change_selected_note_color)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="削除", command=self.delete_selected_note)
        
        # ステータスバー
        self.status_var = tk.StringVar()
        self.status_var.set("準備完了")
        status_bar = tk.Label(self, textvariable=self.status_var, 
                            font=("Yu Gothic UI", 8), bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 保存されたノートを読み込む
        self.load_notes()
        
        # 終了時の処理
        self.protocol("WM_DELETE_WINDOW", self.on_exit)

    def show_tree_context_menu(self, event):
        # 右クリックした項目を選択
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            try:
                self.context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                self.context_menu.grab_release()

    def update_preview(self, event=None):
        selected = self.tree.selection()
        if selected:
            item_id = selected[0]
            note_id = self.tree.item(item_id, "values")[0]
            
            # 選択した付箋のデータを取得
            note_data = None
            for note in self.all_notes:
                if note["id"] == note_id:
                    note_data = note
                    break
            
            if note_data:
                # プレビューテキストを更新
                self.preview_text.config(state="normal")
                self.preview_text.delete("1.0", tk.END)
                self.preview_text.insert("1.0", note_data.get("text", ""))
                self.preview_text.config(state="disabled")
                
                # 付箋の色を反映
                color = note_data.get("color", "#FFFF99")
                self.preview_text.config(bg=color)
        
        else:
            # 選択がなければプレビューをクリア
            self.preview_text.config(state="normal")
            self.preview_text.delete("1.0", tk.END)
            self.preview_text.config(state="disabled", bg="white")

    def filter_notes(self):
        # 検索条件でフィルタリング
        search_text = self.search_var.get().lower()
        
        # ツリービューをクリア
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # フィルタリングして表示
        for note in self.all_notes:
            if (search_text in note.get("id", "").lower() or 
                search_text in note.get("text", "").lower()):
                
                # 日時表示を整形
                date_str = note["id"]
                if len(date_str) == 14 and date_str.isdigit():  # YYYYMMDDHHMMSSの14桁
                    try:
                        date_obj = datetime.strptime(date_str, "%Y%m%d%H%M%S")
                        date_display = date_obj.strftime("%Y/%m/%d %H:%M")
                    except:
                        date_display = date_str
                else:
                    date_display = date_str
                
                # テキストプレビュー（1行に制限）
                text = note.get("text", "").strip()
                # 改行を削除して1行に
                text = text.replace("\n", " ").replace("\r", " ")
                preview = (text[:50] + "...") if len(text) > 50 else text
                if not preview:
                    preview = "(内容なし)"
                
                # 状態表示
                status = "開いている" if note.get("is_open", False) else "閉じている"
                
                # ツリービューに追加
                self.tree.insert("", "end", values=(note["id"], date_display, preview, status))

    def create_new_note(self, note_data=None):
        if isinstance(note_data, dict):
            note = StickyNote(
                self,
                note_id=note_data.get("id"),
                text=note_data.get("text", ""),
                x=note_data.get("x"),
                y=note_data.get("y"),
                color=note_data.get("color", "#FFFF99")
            )
            
            # サイズを設定（保存されていればそのサイズを復元）
            if "width" in note_data and "height" in note_data:
                note.geometry(f"{note_data['width']}x{note_data['height']}")
            
            # 新規ウィンドウか既存のウィンドウかを判断
            is_new = True
            for i, existing_note in enumerate(self.all_notes):
                if existing_note["id"] == note.note_id:
                    # 既存の付箋データを更新
                    self.all_notes[i] = note.get_note_data()
                    is_new = False
                    break
            
            if is_new:
                # 新規付箋をリストに追加
                self.all_notes.append(note.get_note_data())
        else:
            # 完全に新規の付箋を作成
            note = StickyNote(self)
            self.all_notes.append(note.get_note_data())
        
        self.notes.append(note)
        self.status_var.set(f"付箋を作成しました（ID: {note.note_id}）")
        
        # リストを更新
        self.refresh_note_list()
        
        return note

    def open_selected_note(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("情報", "開く付箋を選択してください。")
            return
        
        item_id = selected[0]
        note_id = self.tree.item(item_id, "values")[0]
        
        # 既に開いているか確認
        for note in self.notes:
            if note.winfo_exists() and note.note_id == note_id:
                note.focus_force()  # 既に開いている場合はフォーカスを当てる
                note.lift()         # 最前面に表示
                note.text_area.focus_set()  # 編集モードにする
                return
        
        # 選択した付箋のデータを取得
        note_data = None
        for note in self.all_notes:
            if note["id"] == note_id:
                note_data = note
                # 開いている状態に更新
                note["is_open"] = True
                break
        
        if note_data:
            new_note = self.create_new_note(note_data)
            new_note.text_area.focus_set()  # 編集モードにする
        else:
            messagebox.showerror("エラー", "付箋データの取得に失敗しました。")

    # edit_selected_note メソッドを削除（open_selected_note に統合）

    def delete_selected_note(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("情報", "削除する付箋を選択してください。")
            return
        
        if not messagebox.askyesno("確認", "選択した付箋を完全に削除しますか？\nこの操作は元に戻せません。"):
            return
        
        item_id = selected[0]
        note_id = self.tree.item(item_id, "values")[0]
        
        # 開いているウィンドウがあれば閉じる
        for note in list(self.notes):
            if note.winfo_exists() and note.note_id == note_id:
                note.destroy()
                self.notes.remove(note)
        
        # データから削除
        for i, note in enumerate(self.all_notes):
            if note["id"] == note_id:
                del self.all_notes[i]
                break
        
        # 保存して表示を更新
        self.save_notes()
        self.refresh_note_list()
        self.status_var.set(f"付箋を削除しました（ID: {note_id}）")

    def change_selected_note_color(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("情報", "色を変更する付箋を選択してください。")
            return
        
        item_id = selected[0]
        note_id = self.tree.item(item_id, "values")[0]
        
        # 選択した付箋のデータを取得
        note_data = None
        for i, note in enumerate(self.all_notes):
            if note["id"] == note_id:
                note_data = note
                note_index = i
                break
        
        if not note_data:
            return
        
        # 現在の色を取得
        current_color = note_data.get("color", "#FFFF99")
        
        # 色選択ダイアログを表示
        color = colorchooser.askcolor(initialcolor=current_color)[1]
        if not color:
            return
        
        # 色を更新
        note_data["color"] = color
        self.all_notes[note_index] = note_data
        
        # 開いているウィンドウがあれば色を更新
        for note in self.notes:
            if note.winfo_exists() and note.note_id == note_id:
                note.config(bg=color)
                note.text_area.config(bg=color)
                if not note.show_title_bar:
                    note.control_frame.config(bg=color)
                    note.close_button.config(bg=color)
                    note.settings_button.config(bg=color)
                    note.drag_label.config(bg=color)
        
        # 保存して表示を更新
        self.save_notes()
        self.refresh_note_list()
        self.update_preview()
        self.status_var.set(f"付箋の色を変更しました（ID: {note_id}）")

    def update_note_in_list(self, note_id):
        """特定の付箋のデータを更新"""
        # 開いている付箋のデータを取得
        updated_data = None
        for note in self.notes:
            if note.winfo_exists() and note.note_id == note_id:
                updated_data = note.get_note_data()
                break
        
        if not updated_data:
            return
        
        # データリストの対応する付箋を更新
        for i, note in enumerate(self.all_notes):
            if note["id"] == note_id:
                self.all_notes[i] = updated_data
                break
        
        # 表示を更新
        self.refresh_note_list()
        self.update_preview()

    def update_closed_note(self, note_data):
        """閉じられた付箋のデータを更新"""
        note_id = note_data["id"]
        
        # データリストの対応する付箋を更新
        for i, note in enumerate(self.all_notes):
            if note["id"] == note_id:
                self.all_notes[i] = note_data
                break
        
        # 表示を更新
        self.refresh_note_list()

    def refresh_note_list(self):
        """付箋リストを更新"""
        # 開いている付箋の状態を更新
        open_note_ids = []
        for note in self.notes:
            if note.winfo_exists():
                open_note_ids.append(note.note_id)
                
                # データに反映
                for i, note_data in enumerate(self.all_notes):
                    if note_data["id"] == note.note_id:
                        self.all_notes[i] = note.get_note_data()
                        break
        
        # 閉じている付箋の状態を更新
        for i, note_data in enumerate(self.all_notes):
            if note_data["id"] not in open_note_ids:
                self.all_notes[i]["is_open"] = False
        
        # リスト表示を更新
        self.filter_notes()

    def load_notes(self):
        if os.path.exists(self.notes_file):
            try:
                with open(self.notes_file, "r", encoding="utf-8") as f:
                    self.all_notes = json.load(f)
                
                # リスト表示を更新
                self.refresh_note_list()
                
                # 前回開いていた付箋を再表示
                open_notes = [note for note in self.all_notes if note.get("is_open", False)]
                for note_data in open_notes:
                    self.create_new_note(note_data)
                
                self.status_var.set(f"{len(self.all_notes)}個の付箋データを読み込みました")
            except Exception as e:
                messagebox.showerror("エラー", f"ノートの読み込み中にエラーが発生しました: {e}")
                self.status_var.set("ノートの読み込みに失敗しました")
        else:
            self.status_var.set("新規データファイルを作成します")

    def save_notes(self):
        # 開いている付箋の状態を更新
        self.refresh_note_list()
        
        try:
            with open(self.notes_file, "w", encoding="utf-8") as f:
                json.dump(self.all_notes, f, ensure_ascii=False, indent=2)
            self.status_var.set(f"{len(self.all_notes)}個の付箋を保存しました")
        except Exception as e:
            messagebox.showerror("エラー", f"ノートの保存中にエラーが発生しました: {e}")
            self.status_var.set("ノートの保存に失敗しました")

    def start_move(self, event):
        """ウィンドウ移動開始"""
        self.x = event.x
        self.y = event.y

    def on_move(self, event):
        """ウィンドウ移動処理"""
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry(f"+{x}+{y}")
    
    def on_exit(self):
        self.save_notes()
        self.destroy()


if __name__ == "__main__":
    app = StickyNoteApp()
    app.mainloop()