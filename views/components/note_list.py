"""付箋リストコンポーネント"""
import tkinter as tk
from tkinter import ttk
from typing import List, Optional, Callable
from models.note_model import NoteData
from utils.constants import (
    COLUMN_ID_WIDTH, COLUMN_DATE_WIDTH, COLUMN_PREVIEW_WIDTH, COLUMN_STATUS_WIDTH,
    TEXT_PREVIEW_MAX_LENGTH
)


class NoteListComponent:
    """付箋リストを表示するコンポーネント"""
    
    def __init__(self, parent: tk.Widget):
        self.parent = parent
        self.search_var = tk.StringVar()
        self.all_notes: List[NoteData] = []
        self._create_widgets()
        self._setup_events()
        
        # コールバック
        self.on_double_click: Optional[Callable[[str], None]] = None
        self.on_selection_change: Optional[Callable[[Optional[str]], None]] = None
        self.on_right_click: Optional[Callable[[tk.Event], None]] = None
    
    def _create_widgets(self) -> None:
        """ウィジェットを作成"""
        # 検索フレーム
        search_frame = ttk.Frame(self.parent)
        search_frame.pack(fill=tk.X, padx=5, pady=2)
        
        search_label = ttk.Label(search_frame, text="検索:")
        search_label.pack(side=tk.LEFT, padx=2)
        
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        clear_button = ttk.Button(search_frame, text="✕", width=3, 
                                command=lambda: self.search_var.set(""))
        clear_button.pack(side=tk.RIGHT, padx=2)
        
        # リストビューフレーム
        list_view_frame = ttk.Frame(self.parent)
        list_view_frame.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        
        # ツリービュー
        self.tree = ttk.Treeview(list_view_frame, columns=("id", "date", "preview", "status"), 
                              show="headings", selectmode="browse")
        
        # カラム設定
        self.tree.heading("id", text="ID")
        self.tree.heading("date", text="日時")
        self.tree.heading("preview", text="内容")
        self.tree.heading("status", text="状態")
        
        self.tree.column("id", width=COLUMN_ID_WIDTH, minwidth=0, stretch=tk.NO)
        self.tree.column("date", width=COLUMN_DATE_WIDTH, anchor="w")
        self.tree.column("preview", width=COLUMN_PREVIEW_WIDTH, anchor="w", stretch=tk.YES)
        self.tree.column("status", width=COLUMN_STATUS_WIDTH, anchor="center")
        
        # スクロールバー
        scrollbar = ttk.Scrollbar(list_view_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # 配置
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
    
    def _setup_events(self) -> None:
        """イベントを設定"""
        # 検索イベント
        self.search_var.trace("w", lambda *args: self._filter_notes())
        
        # リストイベント
        self.tree.bind("<Double-1>", self._on_double_click)
        self.tree.bind("<<TreeviewSelect>>", self._on_selection_change)
        self.tree.bind("<Button-3>", self._on_right_click)
    
    def set_notes(self, notes: List[NoteData]) -> None:
        """付箋リストを設定"""
        self.all_notes = notes
        self._filter_notes()
    
    def refresh(self) -> None:
        """リストを更新"""
        self._filter_notes()
    
    def get_selected_note_id(self) -> Optional[str]:
        """選択された付箋のIDを取得"""
        selected = self.tree.selection()
        if selected:
            item_id = selected[0]
            return self.tree.item(item_id, "values")[0]
        return None
    
    def _filter_notes(self) -> None:
        """検索条件でフィルタリング"""
        search_text = self.search_var.get().lower()
        
        # ツリービューをクリア
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # フィルタリングして表示
        for note in self.all_notes:
            if (search_text in note.id.lower() or 
                search_text in note.text.lower()):
                
                date_display = note.get_formatted_date()
                preview = note.get_preview_text(TEXT_PREVIEW_MAX_LENGTH)
                status = note.get_status_text()
                
                self.tree.insert("", "end", values=(note.id, date_display, preview, status))
    
    def _on_double_click(self, event: tk.Event) -> None:
        """ダブルクリックイベント"""
        note_id = self.get_selected_note_id()
        if note_id and self.on_double_click:
            self.on_double_click(note_id)
    
    def _on_selection_change(self, event: tk.Event) -> None:
        """選択変更イベント"""
        note_id = self.get_selected_note_id()
        if self.on_selection_change:
            self.on_selection_change(note_id)
    
    def _on_right_click(self, event: tk.Event) -> None:
        """右クリックイベント"""
        # 右クリックした項目を選択
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            if self.on_right_click:
                self.on_right_click(event)