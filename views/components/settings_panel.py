"""設定パネルコンポーネント"""
import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable
from services.language_service import get_language_service
from utils.constants import HEADER_FONT


class SettingsPanelComponent:
    """設定パネルを表示するコンポーネント"""
    
    def __init__(self, parent: tk.Widget):
        self.parent = parent
        self.language_service = get_language_service()
        self.language_var = tk.StringVar()
        self._create_widgets()
        self._setup_events()
        self._update_interface()
        
        # 言語変更コールバック
        self.on_language_changed: Optional[Callable[[str], None]] = None
        
        # 言語サービスのコールバック設定
        self.language_service.set_language_changed_callback(self._on_language_changed)
    
    def _create_widgets(self) -> None:
        """ウィジェットを作成"""
        # 言語設定セクション
        language_frame = ttk.LabelFrame(self.parent, text="Language / 言語")
        language_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 言語選択
        language_label = ttk.Label(language_frame, text="Language:", font=HEADER_FONT)
        language_label.pack(anchor="w", padx=10, pady=5)
        
        self.language_combo = ttk.Combobox(language_frame, textvariable=self.language_var, 
                                         state="readonly", width=30)
        self.language_combo.pack(anchor="w", padx=10, pady=5)
        
        # 言語選択肢を設定
        languages = self.language_service.get_available_languages()
        self.language_combo['values'] = [f"{name} ({code})" for code, name in languages]
        
        # 現在の言語を選択
        current_lang = self.language_service.get_current_language()
        for i, (code, name) in enumerate(languages):
            if code == current_lang:
                self.language_combo.current(i)
                break
    
    def _setup_events(self) -> None:
        """イベントを設定"""
        self.language_combo.bind('<<ComboboxSelected>>', self._on_language_selection_changed)
    
    def _on_language_selection_changed(self, event) -> None:
        """言語選択が変更されたとき"""
        selection = self.language_combo.get()
        if selection:
            # "Language Name (code)" 形式から code を抽出
            if '(' in selection and ')' in selection:
                code = selection.split('(')[-1].rstrip(')')
                self.language_service.set_language(code)
    
    def _on_language_changed(self, language_code: str) -> None:
        """言語が変更されたときのコールバック"""
        self._update_interface()
        if self.on_language_changed:
            self.on_language_changed(language_code)
    
    def _update_interface(self) -> None:
        """インターフェース言語を更新"""
        # ラベルテキストを更新
        try:
            # LabelFrameのテキストを更新 
            for widget in self.parent.winfo_children():
                if isinstance(widget, ttk.LabelFrame):
                    widget.configure(text=f"{self.language_service.translate('language')} / Language")
                    break
            
            # 言語ラベルを更新
            for widget in self.parent.winfo_children():
                if isinstance(widget, ttk.LabelFrame):
                    for child in widget.winfo_children():
                        if isinstance(child, ttk.Label):
                            child.configure(text=f"{self.language_service.translate('language')}:")
                            break
                    break
        except:
            # エラーが発生した場合は無視
            pass
