"""付箋ウィンドウビュー"""
import tkinter as tk
from tkinter import messagebox
from typing import Callable, Optional
from models.note_model import NoteData
from services.ui_service import UIService
from utils.constants import (
    DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT, MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT,
    ALWAYS_ON_TOP, CONTROL_HEIGHT, RESIZE_HANDLE_SIZE, CONTROL_TEXT_COLOR,
    DEFAULT_FONT, CONTROL_FONT
)


class StickyNoteWindow(tk.Toplevel):
    """付箋ウィンドウクラス"""
    
    def __init__(self, master, note_data: NoteData):
        super().__init__(master)
        self.master = master
        self.note_data = note_data
        
        # コールバック
        self.on_save: Optional[Callable[[NoteData], None]] = None
        self.on_close: Optional[Callable[[str], None]] = None
        self.on_color_change: Optional[Callable[[str, str], None]] = None
        
        # ドラッグ用変数
        self.drag_start_x = 0
        self.drag_start_y = 0
        
        # リサイズ用変数
        self.resize_start_x = 0
        self.resize_start_y = 0
        self.resize_start_width = 0
        self.resize_start_height = 0
        
        self._setup_window()
        self._create_widgets()
        self._setup_events()
        self._apply_note_data()
    
    def _setup_window(self) -> None:
        """ウィンドウの基本設定"""
        self.overrideredirect(True)
        self.geometry(f"{DEFAULT_WINDOW_WIDTH}x{DEFAULT_WINDOW_HEIGHT}")
        self.config(bg=self.note_data.color)
        self.attributes("-topmost", ALWAYS_ON_TOP)
        self.resizable(True, True)
    
    def _create_widgets(self) -> None:
        """ウィジェットを作成"""
        # コントロールフレーム
        self.control_frame = tk.Frame(self, bg=self.note_data.color, height=CONTROL_HEIGHT)
        self.control_frame.pack(fill=tk.X, side=tk.TOP)
        
        # 閉じるボタン
        self.close_button = tk.Label(self.control_frame, text="×", bg=self.note_data.color, 
                                    fg=CONTROL_TEXT_COLOR, font=CONTROL_FONT)
        self.close_button.pack(side=tk.RIGHT, padx=5)
        
        # 設定ボタン
        self.settings_button = tk.Label(self.control_frame, text="⚙", bg=self.note_data.color, 
                                      fg=CONTROL_TEXT_COLOR, font=CONTROL_FONT)
        self.settings_button.pack(side=tk.RIGHT, padx=5)
        
        # ドラッグハンドル
        self.drag_label = tk.Label(self.control_frame, text="≡", bg=self.note_data.color, 
                                  fg=CONTROL_TEXT_COLOR, font=CONTROL_FONT)
        self.drag_label.pack(side=tk.LEFT, padx=5)
        
        # サイズ変更ハンドル
        self.resize_frame = tk.Frame(self, bg=self.note_data.color, cursor="sizing")
        self.resize_frame.place(relx=1.0, rely=1.0, anchor="se", 
                              width=RESIZE_HANDLE_SIZE, height=RESIZE_HANDLE_SIZE)
        
        # テキストエリア
        self.text_area = tk.Text(self, wrap=tk.WORD, bg=self.note_data.color, 
                               relief=tk.FLAT, font=DEFAULT_FONT, bd=2)
        self.text_area.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        
        # コンテキストメニュー
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="色の変更", command=self._change_color)
        self.context_menu.add_command(label="閉じる", command=self._on_close_clicked)
    
    def _setup_events(self) -> None:
        """イベントを設定"""
        # ボタンイベント
        self.close_button.bind("<Button-1>", lambda e: self._on_close_clicked())
        self.settings_button.bind("<Button-1>", self._show_context_menu)
        
        # ドラッグイベント
        UIService.bind_window_events(
            self, self._start_drag, self._on_drag,
            self._start_resize, self._on_resize,
            self.drag_label, self.resize_frame
        )
        
        # テキストイベント
        self.bind("<FocusOut>", self._save_on_focus_out)
        self.bind("<Control-s>", self._save_note)
        self.text_area.bind("<Button-3>", self._show_context_menu)
        self.text_area.bind("<Button-1>", lambda e: self.text_area.focus_set())
        
        # ウィンドウイベント
        self.protocol("WM_DELETE_WINDOW", self._on_close_clicked)
    
    def _apply_note_data(self) -> None:
        """付箋データをウィンドウに適用"""
        # テキストを設定
        self.text_area.insert(tk.END, self.note_data.text)
        
        # 位置とサイズを設定
        if self.note_data.x is not None and self.note_data.y is not None:
            self.geometry(f"{self.note_data.width}x{self.note_data.height}+{self.note_data.x}+{self.note_data.y}")
        else:
            # ランダムな位置を設定
            x, y = UIService.get_random_position(self.winfo_screenwidth(), self.winfo_screenheight())
            self.geometry(f"{self.note_data.width}x{self.note_data.height}+{x}+{y}")
    
    def _start_drag(self, event: tk.Event) -> None:
        """ドラッグ開始"""
        self.drag_start_x = event.x
        self.drag_start_y = event.y
    
    def _on_drag(self, event: tk.Event) -> None:
        """ドラッグ処理"""
        x = self.winfo_x() + (event.x - self.drag_start_x)
        y = self.winfo_y() + (event.y - self.drag_start_y)
        self.geometry(f"+{x}+{y}")
    
    def _start_resize(self, event: tk.Event) -> None:
        """リサイズ開始"""
        self.resize_start_x = event.x_root
        self.resize_start_y = event.y_root
        self.resize_start_width = self.winfo_width()
        self.resize_start_height = self.winfo_height()
    
    def _on_resize(self, event: tk.Event) -> None:
        """リサイズ処理"""
        new_width = max(MIN_WINDOW_WIDTH, 
                       self.resize_start_width + (event.x_root - self.resize_start_x))
        new_height = max(MIN_WINDOW_HEIGHT, 
                        self.resize_start_height + (event.y_root - self.resize_start_y))
        self.geometry(f"{new_width}x{new_height}")
    
    def _show_context_menu(self, event: Optional[tk.Event] = None) -> None:
        """コンテキストメニュー表示"""
        try:
            if event:
                self.context_menu.tk_popup(event.x_root, event.y_root)
            else:
                x = self.settings_button.winfo_rootx()
                y = self.settings_button.winfo_rooty() + self.settings_button.winfo_height()
                self.context_menu.tk_popup(x, y)
        finally:
            self.context_menu.grab_release()
    
    def _change_color(self) -> None:
        """色を変更"""
        color = UIService.choose_color(self.note_data.color)
        if color:
            self._apply_color(color)
            self.note_data.color = color
            self._save_note()
            if self.on_color_change:
                self.on_color_change(self.note_data.id, color)
    
    def _apply_color(self, color: str) -> None:
        """色をウィンドウに適用"""
        self.config(bg=color)
        self.text_area.config(bg=color)
        self.control_frame.config(bg=color)
        self.close_button.config(bg=color)
        self.settings_button.config(bg=color)
        self.drag_label.config(bg=color)
        self.resize_frame.config(bg=color)
    
    def _save_on_focus_out(self, event: Optional[tk.Event] = None) -> None:
        """フォーカスが外れたときに保存"""
        self._save_note()
    
    def _save_note(self, event: Optional[tk.Event] = None) -> str:
        """付箋を保存"""
        self._update_note_data()
        if self.on_save:
            self.on_save(self.note_data)
        return "break"
    
    def _update_note_data(self) -> None:
        """ウィンドウの状態をデータに反映"""
        self.note_data.text = self.text_area.get("1.0", tk.END).strip()
        self.note_data.x = self.winfo_x()
        self.note_data.y = self.winfo_y()
        self.note_data.width = self.winfo_width()
        self.note_data.height = self.winfo_height()
        self.note_data.is_open = True
        self.note_data.was_open = True
    
    def _on_close_clicked(self) -> None:
        """閉じるボタンがクリックされたとき"""
        self._save_note()
        self.note_data.is_open = False
        if self.on_close:
            self.on_close(self.note_data.id)
        self.destroy()
    
    def apply_color_change(self, color: str) -> None:
        """外部からの色変更を適用"""
        self.note_data.color = color
        self._apply_color(color)
    
    def focus_text_area(self) -> None:
        """テキストエリアにフォーカスを当てる"""
        self.focus_force()
        self.lift()
        self.text_area.focus_set()
    
    def get_note_id(self) -> str:
        """付箋IDを取得"""
        return self.note_data.id