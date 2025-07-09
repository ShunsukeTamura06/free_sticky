"""プレビューパネルコンポーネント"""
import tkinter as tk
from tkinter import ttk
from typing import Optional
from models.note_model import NoteData
from utils.constants import DEFAULT_FONT, HEADER_FONT, PREVIEW_HEIGHT


class PreviewPanelComponent:
    """付箋のプレビューを表示するコンポーネント"""
    
    def __init__(self, parent: tk.Widget):
        self.parent = parent
        self._create_widgets()
    
    def _create_widgets(self) -> None:
        """ウィジェットを作成"""
        # プレビューラベル
        preview_label = ttk.Label(self.parent, text="プレビュー:", font=HEADER_FONT)
        preview_label.pack(anchor="w", padx=5, pady=2)
        
        # プレビューテキスト
        self.preview_text = tk.Text(self.parent, wrap=tk.WORD, height=PREVIEW_HEIGHT, 
                                  font=DEFAULT_FONT, state="disabled")
        self.preview_text.pack(expand=True, fill=tk.BOTH, padx=5, pady=2)
    
    def update_preview(self, note: Optional[NoteData]) -> None:
        """プレビューを更新"""
        self.preview_text.config(state="normal")
        self.preview_text.delete("1.0", tk.END)
        
        if note:
            self.preview_text.insert("1.0", note.text)
            self.preview_text.config(bg=note.color)
        else:
            self.preview_text.config(bg="white")
        
        self.preview_text.config(state="disabled")
    
    def clear_preview(self) -> None:
        """プレビューをクリア"""
        self.update_preview(None)