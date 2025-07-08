"""メインアプリケーションクラス - 全体の統合と管理"""
from typing import Optional
from models.note_model import NoteData
from services.storage_service import StorageService
from controllers.note_controller import NoteController
from views.main_window import MainWindow
from services.ui_service import UIService
from utils.constants import STATUS_NEW_FILE, STATUS_LOAD_FAILED


class StickyNoteApplication:
    """付箋アプリケーションのメインクラス"""
    
    def __init__(self):
        # サービス層の初期化
        self.storage_service = StorageService()
        self._setup_storage_callbacks()
        
        # コントローラーの初期化
        self.note_controller = NoteController(self.storage_service)
        self._setup_controller_callbacks()
        
        # ビューの初期化
        self.main_window = MainWindow()
        self._setup_view_callbacks()
        
        # 初期化完了
        self._initialize_application()
    
    def _setup_storage_callbacks(self) -> None:
        """ストレージサービスのコールバックを設定"""
        self.storage_service.set_error_callback(self._on_storage_error)
        self.storage_service.set_success_callback(self._on_storage_success)
    
    def _setup_controller_callbacks(self) -> None:
        """コントローラーのコールバックを設定"""
        self.note_controller.on_notes_changed = self._on_notes_changed
        self.note_controller.on_status_update = self._on_status_update
    
    def _setup_view_callbacks(self) -> None:
        """ビューのコールバックを設定"""
        self.main_window.on_create_note = self._on_create_note_requested
        self.main_window.on_open_note = self._on_open_note_requested
        self.main_window.on_delete_note = self._on_delete_note_requested
        self.main_window.on_change_color = self._on_change_color_requested
        self.main_window.on_refresh = self._on_refresh_requested
        
        # ウィンドウクローズイベント
        self.main_window.protocol("WM_DELETE_WINDOW", self._on_application_exit)
        
        # 選択変更イベント
        self.main_window.note_list.on_selection_change = self._on_note_selection_changed
    
    def _initialize_application(self) -> None:
        """アプリケーションを初期化"""
        if not self.storage_service.is_file_exists():
            self._on_status_update(STATUS_NEW_FILE)
        
        # コントローラーを初期化（保存されたデータを読み込み）
        self.note_controller.initialize()
    
    def run(self) -> None:
        """アプリケーションを実行"""
        self.main_window.mainloop()
    
    # コールバックメソッド群
    
    def _on_storage_error(self, message: str) -> None:
        """ストレージエラー時の処理"""
        UIService.show_error(message)
        self.main_window.update_status(STATUS_LOAD_FAILED)
    
    def _on_storage_success(self, message: str) -> None:
        """ストレージ成功時の処理"""
        self.main_window.update_status(message)
    
    def _on_notes_changed(self, notes: list[NoteData]) -> None:
        """付箋リストが変更されたときの処理"""
        self.main_window.set_notes(notes)
        
        # 現在選択されている付箋のプレビューを更新
        selected_id = self.main_window.get_selected_note_id()
        if selected_id:
            selected_note = self.note_controller.get_note_by_id(selected_id)
            self.main_window.update_preview(selected_note)
    
    def _on_status_update(self, message: str) -> None:
        """ステータス更新時の処理"""
        self.main_window.update_status(message)
    
    def _on_create_note_requested(self) -> None:
        """新規付箋作成リクエストの処理"""
        self.note_controller.create_new_note()
    
    def _on_open_note_requested(self, note_id: str) -> None:
        """付箋を開くリクエストの処理"""
        self.note_controller.open_note_by_id(note_id)
    
    def _on_delete_note_requested(self, note_id: str) -> None:
        """付箋削除リクエストの処理"""
        self.note_controller.delete_note_by_id(note_id)
    
    def _on_change_color_requested(self, note_id: str) -> None:
        """付箋の色変更リクエストの処理"""
        self.note_controller.change_note_color(note_id)
    
    def _on_refresh_requested(self) -> None:
        """更新リクエストの処理"""
        self.note_controller.refresh_notes()
    
    def _on_note_selection_changed(self, note_id: Optional[str]) -> None:
        """付箋選択変更時の処理"""
        if note_id:
            note = self.note_controller.get_note_by_id(note_id)
            self.main_window.update_preview(note)
        else:
            self.main_window.update_preview(None)
    
    def _on_application_exit(self) -> None:
        """アプリケーション終了時の処理"""
        self.note_controller.shutdown()
        self.main_window.destroy()