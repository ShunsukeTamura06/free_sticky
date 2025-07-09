"""メインウィンドウビュー"""
import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable, List
from models.note_model import NoteData
from views.components.note_list import NoteListComponent
from views.components.preview_panel import PreviewPanelComponent
from services.ui_service import UIService
from utils.constants import (
    DEFAULT_MAIN_WIDTH, DEFAULT_MAIN_HEIGHT, MAIN_BG_COLOR, STATUS_FONT,
    STATUS_READY, TOOLBAR_PADDING, MSG_SELECT_NOTE_TO_OPEN, MSG_SELECT_NOTE_TO_DELETE,
    MSG_SELECT_NOTE_FOR_COLOR, STATUS_BAR_HEIGHT
)


class MainWindow(tk.Tk):
    """メインウィンドウクラス"""
    
    def __init__(self):
        super().__init__()
        
        # コールバック
        self.on_create_note: Optional[Callable[[], None]] = None
        self.on_open_note: Optional[Callable[[str], None]] = None
        self.on_delete_note: Optional[Callable[[str], None]] = None
        self.on_change_color: Optional[Callable[[str], None]] = None
        self.on_refresh: Optional[Callable[[], None]] = None
        
        self._setup_window()
        self._create_widgets()
        self._setup_events()
    
    def _setup_window(self) -> None:
        """ウィンドウの基本設定"""
        self.title("付箋管理アプリ")
        self.geometry(f"{DEFAULT_MAIN_WIDTH}x{DEFAULT_MAIN_HEIGHT}")
        self.configure(bg=MAIN_BG_COLOR)
        
        # アイコン設定（リソースがあれば）
        try:
            self.iconbitmap("free_sticky.ico")
        except:
            pass
        
        # スタイル設定
        self.style = ttk.Style()
        UIService.configure_window_style(self, self.style)
    
    def _create_widgets(self) -> None:
        """ウィジェットを作成"""
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
        self._create_toolbar()
        
        # 付箋リストコンポーネント
        self.note_list = NoteListComponent(self.notes_tab)
        self.note_list.on_double_click = self._on_note_double_clicked
        self.note_list.on_selection_change = self._on_note_selection_changed
        self.note_list.on_right_click = self._on_note_right_clicked
        
        # プレビューフレーム（下部）
        self.preview_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(self.preview_frame, weight=1)
        
        # プレビューコンポーネント
        self.preview_panel = PreviewPanelComponent(self.preview_frame)
        
        # コンテキストメニュー
        self._create_context_menu()
        
        # ステータスバー
        self._create_status_bar()
    
    def _create_toolbar(self) -> None:
        """ツールバーを作成"""
        toolbar_frame = ttk.Frame(self.notes_tab)
        toolbar_frame.pack(fill=tk.X, padx=TOOLBAR_PADDING, pady=TOOLBAR_PADDING)
        
        # 付箋リストのツールバーボタン
        self.new_button = ttk.Button(toolbar_frame, text="新規作成", command=self._on_new_clicked)
        self.new_button.pack(side=tk.LEFT, padx=2)
        
        self.open_button = ttk.Button(toolbar_frame, text="開く", command=self._on_open_clicked)
        self.open_button.pack(side=tk.LEFT, padx=2)
        
        self.delete_button = ttk.Button(toolbar_frame, text="削除", command=self._on_delete_clicked)
        self.delete_button.pack(side=tk.LEFT, padx=2)
        
        self.color_button = ttk.Button(toolbar_frame, text="色変更", command=self._on_color_clicked)
        self.color_button.pack(side=tk.LEFT, padx=2)
        
        self.refresh_button = ttk.Button(toolbar_frame, text="更新", command=self._on_refresh_clicked)
        self.refresh_button.pack(side=tk.RIGHT, padx=2)
    
    def _create_context_menu(self) -> None:
        """コンテキストメニューを作成"""
        self.context_menu = tk.Menu(self.note_list.tree, tearoff=0)
        self.context_menu.add_command(label="開く", command=self._on_open_clicked)
        self.context_menu.add_command(label="色変更", command=self._on_color_clicked)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="削除", command=self._on_delete_clicked)
    
    def _create_status_bar(self) -> None:
        """ステータスバーを作成"""
        self.status_var = tk.StringVar()
        self.status_var.set(STATUS_READY)
        status_bar = tk.Label(self, textvariable=self.status_var, 
                            font=STATUS_FONT, bd=1, relief=tk.SUNKEN, anchor=tk.W,
                            height=STATUS_BAR_HEIGHT)  # 固定高さを設定
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def _setup_events(self) -> None:
        """イベントを設定"""
        pass  # コールバックベースなので特に設定はなし
    
    def set_notes(self, notes: List[NoteData]) -> None:
        """付箋リストを設定"""
        self.note_list.set_notes(notes)
    
    def refresh_notes(self) -> None:
        """付箋リストを更新"""
        self.note_list.refresh()
    
    def update_status(self, message: str) -> None:
        """ステータスメッセージを更新"""
        self.status_var.set(message)
    
    def update_preview(self, note: Optional[NoteData]) -> None:
        """プレビューを更新"""
        self.preview_panel.update_preview(note)
    
    def _on_new_clicked(self) -> None:
        """新規作成ボタンがクリックされたとき"""
        if self.on_create_note:
            self.on_create_note()
    
    def _on_open_clicked(self) -> None:
        """開くボタンがクリックされたとき"""
        note_id = self.note_list.get_selected_note_id()
        if note_id:
            if self.on_open_note:
                self.on_open_note(note_id)
        else:
            UIService.show_select_note_message("open")
    
    def _on_delete_clicked(self) -> None:
        """削除ボタンがクリックされたとき"""
        note_id = self.note_list.get_selected_note_id()
        if note_id:
            if self.on_delete_note:
                self.on_delete_note(note_id)
        else:
            UIService.show_select_note_message("delete")
    
    def _on_color_clicked(self) -> None:
        """色変更ボタンがクリックされたとき"""
        note_id = self.note_list.get_selected_note_id()
        if note_id:
            if self.on_change_color:
                self.on_change_color(note_id)
        else:
            UIService.show_select_note_message("color")
    
    def _on_refresh_clicked(self) -> None:
        """更新ボタンがクリックされたとき"""
        if self.on_refresh:
            self.on_refresh()
    
    def _on_note_double_clicked(self, note_id: str) -> None:
        """付箋がダブルクリックされたとき"""
        if self.on_open_note:
            self.on_open_note(note_id)
    
    def _on_note_selection_changed(self, note_id: Optional[str]) -> None:
        """付箋の選択が変更されたとき"""
        # プレビューを更新するためにメインコントローラーに通知
        # ここでは何もしない（コントローラーが処理）
        pass
    
    def _on_note_right_clicked(self, event: tk.Event) -> None:
        """付箋が右クリックされたとき"""
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
    
    def get_selected_note_id(self) -> Optional[str]:
        """選択された付箋IDを取得"""
        return self.note_list.get_selected_note_id()