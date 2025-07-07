"""ストレージサービス - データの永続化を担当"""
from typing import List, Optional, Callable
from models.note_model import NoteData
from models.note_repository import JsonNoteRepository, NoteRepositoryInterface


class StorageService:
    """データストレージを管理するサービスクラス"""
    
    def __init__(self, repository: NoteRepositoryInterface = None):
        self.repository = repository or JsonNoteRepository()
        self._error_callback: Optional[Callable[[str], None]] = None
        self._success_callback: Optional[Callable[[str], None]] = None
    
    def set_error_callback(self, callback: Callable[[str], None]) -> None:
        """エラーコールバックを設定"""
        self._error_callback = callback
    
    def set_success_callback(self, callback: Callable[[str], None]) -> None:
        """成功コールバックを設定"""
        self._success_callback = callback
    
    def load_all_notes(self) -> List[NoteData]:
        """すべての付箋を読み込み"""
        try:
            notes = self.repository.load_all()
            if self._success_callback:
                self._success_callback(f"{len(notes)}個の付箋データを読み込みました")
            return notes
        except Exception as e:
            if self._error_callback:
                self._error_callback(f"ノートの読み込み中にエラーが発生しました: {e}")
            return []
    
    def save_all_notes(self, notes: List[NoteData]) -> bool:
        """すべての付箋を保存"""
        try:
            success = self.repository.save_all(notes)
            if success and self._success_callback:
                self._success_callback(f"{len(notes)}個の付箋を保存しました")
            elif not success and self._error_callback:
                self._error_callback("ノートの保存に失敗しました")
            return success
        except Exception as e:
            if self._error_callback:
                self._error_callback(f"ノートの保存中にエラーが発生しました: {e}")
            return False
    
    def find_note_by_id(self, note_id: str) -> Optional[NoteData]:
        """IDで付箋を検索"""
        return self.repository.find_by_id(note_id)
    
    def add_note(self, note: NoteData) -> bool:
        """付箋を追加"""
        return self.repository.add(note)
    
    def update_note(self, note: NoteData) -> bool:
        """付箋を更新"""
        return self.repository.update(note)
    
    def delete_note(self, note_id: str) -> bool:
        """付箋を削除"""
        return self.repository.delete(note_id)
    
    def is_file_exists(self) -> bool:
        """データファイルが存在するかチェック"""
        if hasattr(self.repository, 'file_exists'):
            return self.repository.file_exists()
        return False