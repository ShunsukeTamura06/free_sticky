"""
UI関連の共通サービス
"""
import tkinter as tk
from tkinter import messagebox, colorchooser
import random
from typing import Optional, Tuple
from utils.constants import (
    RANDOM_POSITION_MARGIN, 
    RANDOM_POSITION_OFFSET,
    MSG_SELECT_NOTE_TO_OPEN,
    MSG_SELECT_NOTE_TO_DELETE,
    MSG_SELECT_NOTE_FOR_COLOR,
    MSG_CONFIRM_DELETE,
    MSG_ERROR_NOTE_DATA
)


class UIService:
    """
UI操作の共通サービスクラス
"""
    
    @staticmethod
    def get_random_position(screen_width: int, screen_height: int) -> Tuple[int, int]:
        """ランダムな位置を計算"""
        x = random.randint(RANDOM_POSITION_MARGIN, screen_width - RANDOM_POSITION_OFFSET)
        y = random.randint(RANDOM_POSITION_MARGIN, screen_height - RANDOM_POSITION_OFFSET)
        return x, y
    
    @staticmethod
    def show_info(message: str, title: str = "情報") -> None:
        """情報メッセージを表示"""
        messagebox.showinfo(title, message)
    
    @staticmethod
    def show_error(message: str, title: str = "エラー") -> None:
        """エラーメッセージを表示"""
        messagebox.showerror(title, message)
    
    @staticmethod
    def confirm_delete() -> bool:
        """削除確認ダイアログを表示"""
        return messagebox.askyesno("確認", MSG_CONFIRM_DELETE)
    
    @staticmethod
    def show_select_note_message(action: str) -> None:
        """付箋選択メッセージを表示"""
        messages = {
            "open": MSG_SELECT_NOTE_TO_OPEN,
            "delete": MSG_SELECT_NOTE_TO_DELETE,
            "color": MSG_SELECT_NOTE_FOR_COLOR
        }
        UIService.show_info(messages.get(action, "付箋を選択してください。"))
    
    @staticmethod
    def choose_color(initial_color: str = "#FFFF99") -> Optional[str]:
        """色選択ダイアログを表示"""
        result = colorchooser.askcolor(initialcolor=initial_color)
        return result[1] if result[1] else None
    
    @staticmethod
    def configure_window_style(window: tk.Tk, style: Optional[object] = None) -> None:
        """ウィンドウのスタイルを設定"""
        if style:
            # スタイルの設定
            style.theme_use('clam')
            
            # ボタンスタイル
            style.configure('TButton', 
                           font=('Yu Gothic UI', 10),
                           borderwidth=1,
                           focusthickness=3,
                           focuscolor='none')
            
            style.map('TButton',
                     background=[('active', '#e1e1e1'), ('pressed', '#d0d0d0')],
                     relief=[('pressed', 'sunken')])
            
            # タブスタイル
            style.configure('TNotebook.Tab', 
                           font=('Yu Gothic UI', 10),
                           padding=[10, 4])
    
    @staticmethod
    def bind_window_events(window: tk.Toplevel, drag_start_func, drag_func, 
                          resize_start_func, resize_func, 
                          drag_handle: tk.Widget, resize_handle: tk.Widget) -> None:
        """ウィンドウのイベントをバインド"""
        # ドラッグイベント
        drag_handle.bind("<Button-1>", drag_start_func)
        drag_handle.bind("<B1-Motion>", drag_func)
        
        # リサイズイベント
        resize_handle.bind("<Button-1>", resize_start_func)
        resize_handle.bind("<B1-Motion>", resize_func)