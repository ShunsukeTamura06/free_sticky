"""付箋コントローラー - ビジネスロジックを管理"""
from typing import Dict, List, Optional, Callable
from models.note_model import NoteData
from services.storage_service import StorageService
from services.ui_service import UIService
from views.note_window import StickyNoteWindow
from utils.constants import (
    STATUS_CREATED, STATUS_EDITING, STATUS_DELETED, STATUS_COLOR_CHANGED,
    MSG_ERROR_NOTE_DATA
)


class NoteController:
    """付箋のビジネスロジックを管理するコントローラー"""
    
    def __init__(self, storage_service: StorageService, main_window=None):
        self.storage_service = storage_service
        self.main_window = main_window  # メインウィンドウの参照を保持
        self.open_windows: Dict[str, StickyNoteWindow] = {}
        self.all_notes: List[NoteData] = []
        
        # コールバック
        self.on_notes_changed: Optional[Callable[[List[NoteData]], None]] = None
        self.on_status_update: Optional[Callable[[str], None]] = None
    
    def set_main_window(self, main_window) -> None:
        """メインウィンドウを設定"""
        self.main_window = main_window
    
    def initialize(self) -> None:
        """コントローラーを初期化"""
        self.all_notes = self.storage_service.load_all_notes()
        
        # 前回開いていた付箋を再表示
        for note in self.all_notes:
            if note.is_open or note.was_open:
                self._create_note_window(note)
        
        if self.on_notes_changed:
            self.on_notes_changed(self.all_notes)
    
    def create_new_note(self, text: str = "") -> None:
        """新しい付箋を作成"""
        note = NoteData.create_new(text)
        self.all_notes.append(note)
        self.storage_service.save_all_notes(self.all_notes)
        
        window = self._create_note_window(note)
        window.focus_text_area()
        
        if self.on_status_update:
            self.on_status_update(STATUS_CREATED.format(note.id))
        
        if self.on_notes_changed:
            self.on_notes_changed(self.all_notes)
    
    def open_note_by_id(self, note_id: str) -> None:
        """指定したIDの付箋を開く"""
        # 既に開いているかチェック
        if note_id in self.open_windows:
            window = self.open_windows[note_id]
            if window.winfo_exists():
                window.focus_text_area()
                if self.on_status_update:
                    self.on_status_update(STATUS_EDITING.format(note_id))
                return
        
        # 付箋データを検索
        note = self._find_note_by_id(note_id)
        if note:
            note.is_open = True
            window = self._create_note_window(note)
            window.focus_text_area()
            self.storage_service.save_all_notes(self.all_notes)
        else:
            UIService.show_error(MSG_ERROR_NOTE_DATA)
    
    def delete_note_by_id(self, note_id: str) -> bool:
        """指定したIDの付箋を削除"""
        if not UIService.confirm_delete():
            return False
        
        # 開いているウィンドウを閉じる
        if note_id in self.open_windows:
            window = self.open_windows[note_id]
            if window.winfo_exists():
                window.destroy()
            del self.open_windows[note_id]
        
        # データから削除
        self.all_notes = [note for note in self.all_notes if note.id != note_id]
        self.storage_service.save_all_notes(self.all_notes)
        
        if self.on_status_update:
            self.on_status_update(STATUS_DELETED.format(note_id))
        
        if self.on_notes_changed:
            self.on_notes_changed(self.all_notes)
        
        return True
    
    def change_note_color(self, note_id: str, new_color: str = None) -> None:
        """付箋の色を変更"""
        note = self._find_note_by_id(note_id)
        if not note:
            return
        
        if new_color is None:
            new_color = UIService.choose_color(note.color)
            if not new_color:
                return
        
        # データを更新
        note.color = new_color
        
        # 開いているウィンドウに適用
        if note_id in self.open_windows:
            window = self.open_windows[note_id]
            if window.winfo_exists():
                window.apply_color_change(new_color)
        
        self.storage_service.save_all_notes(self.all_notes)
        
        if self.on_status_update:
            self.on_status_update(STATUS_COLOR_CHANGED.format(note_id))
        
        if self.on_notes_changed:
            self.on_notes_changed(self.all_notes)
    
    def get_all_notes(self) -> List[NoteData]:
        """すべての付箋データを取得"""
        return self.all_notes.copy()
    
    def get_note_by_id(self, note_id: str) -> Optional[NoteData]:
        """指定したIDの付箋データを取得"""
        return self._find_note_by_id(note_id)
    
    def refresh_notes(self) -> None:
        """付箋リストを更新"""
        # 開いているウィンドウの状態を更新
        for note_id, window in list(self.open_windows.items()):
            if window.winfo_exists():
                note = self._find_note_by_id(note_id)
                if note:
                    window._update_note_data()
                    # データを更新
                    for i, existing_note in enumerate(self.all_notes):
                        if existing_note.id == note_id:
                            self.all_notes[i] = window.note_data
                            break
            else:
                # ウィンドウが閉じられている場合
                del self.open_windows[note_id]
        
        # 閉じている付箋の状態を更新
        open_note_ids = set(self.open_windows.keys())
        for note in self.all_notes:
            note.is_open = note.id in open_note_ids
        
        self.storage_service.save_all_notes(self.all_notes)
        
        if self.on_notes_changed:
            self.on_notes_changed(self.all_notes)
    
    def save_all_notes(self) -> None:
        """すべての付箋を保存"""
        self.refresh_notes()
    
    def shutdown(self) -> None:
        """シャットダウン処理"""
        # 開いている付箋を「前回開いていた付箋」としてマーク
        for note in self.all_notes:
            if note.is_open:
                note.was_open = True
        
        self.save_all_notes()
    
    def _create_note_window(self, note: NoteData) -> StickyNoteWindow:
        """付箋ウィンドウを作成"""
        window = StickyNoteWindow(self.main_window, note)  # メインウィンドウをmasterとして渡す
        
        # コールバックを設定
        window.on_save = self._on_note_saved
        window.on_close = self._on_note_closed
        window.on_color_change = self._on_note_color_changed
        
        self.open_windows[note.id] = window
        return window
    
    def _find_note_by_id(self, note_id: str) -> Optional[NoteData]:
        """指定したIDの付箋を検索"""
        for note in self.all_notes:
            if note.id == note_id:
                return note
        return None
    
    def _on_note_saved(self, note_data: NoteData) -> None:
        """付箋が保存されたときのコールバック"""
        # データを更新
        for i, note in enumerate(self.all_notes):
            if note.id == note_data.id:
                self.all_notes[i] = note_data
                break
        
        self.storage_service.save_all_notes(self.all_notes)
        
        if self.on_notes_changed:
            self.on_notes_changed(self.all_notes)
    
    def _on_note_closed(self, note_id: str) -> None:
        """付箋が閉じられたときのコールバック"""
        if note_id in self.open_windows:
            del self.open_windows[note_id]
        
        # データの状態を更新
        note = self._find_note_by_id(note_id)
        if note:
            note.is_open = False
            note.was_open = True
        
        self.storage_service.save_all_notes(self.all_notes)
        
        if self.on_notes_changed:
            self.on_notes_changed(self.all_notes)
    
    def _on_note_color_changed(self, note_id: str, new_color: str) -> None:
        """付箋の色が変更されたときのコールバック"""
        if self.on_notes_changed:
            self.on_notes_changed(self.all_notes)