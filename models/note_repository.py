"""付箋データのリポジトリパターン実装"""
from typing import List, Optional, Protocol
from abc import abstractmethod
import json
import os
from models.note_model import NoteData
from utils.constants import NOTES_FILE


class NoteRepositoryInterface(Protocol):
    """付箋リポジトリのインターフェース"""
    
    @abstractmethod
    def load_all(self) -> List[NoteData]:
        """すべての付箋データを読み込み"""
        pass
    
    @abstractmethod
    def save_all(self, notes: List[NoteData]) -> bool:
        """すべての付箋データを保存"""
        pass
    
    @abstractmethod
    def find_by_id(self, note_id: str) -> Optional[NoteData]:
        """IDで付箋を検索"""
        pass
    
    @abstractmethod
    def add(self, note: NoteData) -> bool:
        """付箋を追加"""
        pass
    
    @abstractmethod
    def update(self, note: NoteData) -> bool:
        """付箋を更新"""
        pass
    
    @abstractmethod
    def delete(self, note_id: str) -> bool:
        """付箋を削除"""
        pass


class JsonNoteRepository:
    """JSON形式での付箋データ永続化"""
    
    def __init__(self, file_path: str = NOTES_FILE):
        self.file_path = file_path
        self._notes_cache: List[NoteData] = []
        self._cache_loaded = False
    
    def load_all(self) -> List[NoteData]:
        """すべての付箋データを読み込み"""
        if not self._cache_loaded:
            self._load_from_file()
        return self._notes_cache.copy()
    
    def save_all(self, notes: List[NoteData]) -> bool:
        """すべての付箋データを保存"""
        try:
            data = [note.to_dict() for note in notes]
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self._notes_cache = notes.copy()
            return True
        except Exception:
            return False
    
    def find_by_id(self, note_id: str) -> Optional[NoteData]:
        """IDで付箋を検索"""
        if not self._cache_loaded:
            self._load_from_file()
        
        for note in self._notes_cache:
            if note.id == note_id:
                return note
        return None
    
    def add(self, note: NoteData) -> bool:
        """付箋を追加"""
        if not self._cache_loaded:
            self._load_from_file()
        
        # 既存チェック
        if self.find_by_id(note.id):
            return False
        
        self._notes_cache.append(note)
        return self.save_all(self._notes_cache)
    
    def update(self, note: NoteData) -> bool:
        """付箋を更新"""
        if not self._cache_loaded:
            self._load_from_file()
        
        for i, existing_note in enumerate(self._notes_cache):
            if existing_note.id == note.id:
                self._notes_cache[i] = note
                return self.save_all(self._notes_cache)
        
        return False
    
    def delete(self, note_id: str) -> bool:
        """付箋を削除"""
        if not self._cache_loaded:
            self._load_from_file()
        
        for i, note in enumerate(self._notes_cache):
            if note.id == note_id:
                del self._notes_cache[i]
                return self.save_all(self._notes_cache)
        
        return False
    
    def _load_from_file(self) -> None:
        """ファイルからデータを読み込み"""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self._notes_cache = [NoteData.from_dict(item) for item in data]
            except Exception:
                self._notes_cache = []
        else:
            self._notes_cache = []
        
        self._cache_loaded = True
    
    def file_exists(self) -> bool:
        """データファイルが存在するかチェック"""
        return os.path.exists(self.file_path)
    
    def get_notes_count(self) -> int:
        """付箋数を取得"""
        if not self._cache_loaded:
            self._load_from_file()
        return len(self._notes_cache)