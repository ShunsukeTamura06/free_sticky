"""付箋データモデル"""
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional
from datetime import datetime
from utils.constants import DEFAULT_NOTE_COLOR, ID_DATE_FORMAT


@dataclass
class NoteData:
    """付箋データを表すデータクラス"""
    id: str
    text: str = ""
    x: Optional[int] = None
    y: Optional[int] = None
    width: int = 200
    height: int = 200
    color: str = DEFAULT_NOTE_COLOR
    is_open: bool = False
    was_open: bool = False
    
    @classmethod
    def create_new(cls, text: str = "", x: Optional[int] = None, y: Optional[int] = None) -> 'NoteData':
        """新しい付箋データを作成"""
        note_id = datetime.now().strftime(ID_DATE_FORMAT)
        return cls(id=note_id, text=text, x=x, y=y, is_open=True, was_open=True)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'NoteData':
        """辞書から付箋データを作成"""
        return cls(
            id=data.get("id", ""),
            text=data.get("text", ""),
            x=data.get("x"),
            y=data.get("y"),
            width=data.get("width", 200),
            height=data.get("height", 200),
            color=data.get("color", DEFAULT_NOTE_COLOR),
            is_open=data.get("is_open", False),
            was_open=data.get("was_open", False)
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """辞書形式に変換"""
        return asdict(self)
    
    def get_formatted_date(self) -> str:
        """日時をフォーマット済み文字列で取得"""
        if len(self.id) == 14 and self.id.isdigit():
            try:
                date_obj = datetime.strptime(self.id, ID_DATE_FORMAT)
                return date_obj.strftime("%Y/%m/%d %H:%M")
            except ValueError:
                return self.id
        return self.id
    
    def get_preview_text(self, max_length: int = 80) -> str:
        """プレビュー用のテキストを取得"""
        text = self.text.strip().replace("\n", " ").replace("\r", " ")
        preview = (text[:max_length] + "...") if len(text) > max_length else text
        return preview if preview else "(内容なし)"
    
    def get_status_text(self) -> str:
        """状態テキストを取得"""
        return "開いている" if self.is_open else "閉じている"