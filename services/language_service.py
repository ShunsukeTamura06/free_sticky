"""言語管理サービス"""
import json
import os
from typing import Optional, Callable
from utils.translations import TRANSLATIONS, AVAILABLE_LANGUAGES, DEFAULT_LANGUAGE, get_translation, get_language_name


class LanguageService:
    """言語設定とローカライゼーションを管理するサービス"""
    
    SETTINGS_FILE = "free_sticky_settings.json"
    
    def __init__(self):
        self._current_language = DEFAULT_LANGUAGE
        self._language_changed_callback: Optional[Callable[[str], None]] = None
        self._load_settings()
    
    def set_language_changed_callback(self, callback: Callable[[str], None]) -> None:
        """言語変更コールバックを設定"""
        self._language_changed_callback = callback
    
    def get_current_language(self) -> str:
        """現在の言語を取得"""
        return self._current_language
    
    def set_language(self, language_code: str) -> bool:
        """言語を設定"""
        if language_code in AVAILABLE_LANGUAGES:
            self._current_language = language_code
            self._save_settings()
            if self._language_changed_callback:
                self._language_changed_callback(language_code)
            return True
        return False
    
    def get_available_languages(self) -> list[tuple[str, str]]:
        """利用可能な言語のリストを取得 (コード, 名前)のタプルのリスト"""
        return [(code, get_language_name(code)) for code in AVAILABLE_LANGUAGES]
    
    def translate(self, key: str, *args) -> str:
        """現在の言語で翻訳を取得"""
        return get_translation(key, self._current_language, *args)
    
    def _load_settings(self) -> None:
        """設定を読み込み"""
        if os.path.exists(self.SETTINGS_FILE):
            try:
                with open(self.SETTINGS_FILE, "r", encoding="utf-8") as f:
                    settings = json.load(f)
                    language = settings.get("language", DEFAULT_LANGUAGE)
                    if language in AVAILABLE_LANGUAGES:
                        self._current_language = language
            except Exception:
                # 設定ファイルの読み込みに失敗した場合はデフォルトを使用
                pass
    
    def _save_settings(self) -> None:
        """設定を保存"""
        try:
            settings = {
                "language": self._current_language
            }
            with open(self.SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
        except Exception:
            # 設定ファイルの保存に失敗した場合は無視
            pass


# グローバルインスタンス
_language_service = LanguageService()

def get_language_service() -> LanguageService:
    """言語サービスのシングルトンインスタンスを取得"""
    return _language_service
