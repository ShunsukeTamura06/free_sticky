"""アプリケーション定数定義"""

# ファイル名
NOTES_FILE = "sticky_notes.json"

# デフォルト値
DEFAULT_NOTE_COLOR = "#FFFF99"
DEFAULT_WINDOW_WIDTH = 200
DEFAULT_WINDOW_HEIGHT = 200
MIN_WINDOW_WIDTH = 100
MIN_WINDOW_HEIGHT = 100
DEFAULT_MAIN_WIDTH = 600
DEFAULT_MAIN_HEIGHT = 500

# フォント設定
DEFAULT_FONT = ("Yu Gothic UI", 10)
BUTTON_FONT = ("Yu Gothic UI", 10)
STATUS_FONT = ("Yu Gothic UI", 8)
HEADER_FONT = ("Yu Gothic UI", 10, "bold")
CONTROL_FONT = ("Arial", 10, "bold")

# 色設定
MAIN_BG_COLOR = "#f0f0f0"
CONTROL_TEXT_COLOR = "#555555"

# サイズ設定
CONTROL_HEIGHT = 20
RESIZE_HANDLE_SIZE = 15
TOOLBAR_PADDING = 5
SEARCH_PADDING = 2
LIST_PADDING = 5
PREVIEW_HEIGHT = 5

# テキスト設定
TEXT_PREVIEW_MAX_LENGTH = 80
DATE_FORMAT = "%Y/%m/%d %H:%M"
ID_DATE_FORMAT = "%Y%m%d%H%M%S"

# ウィンドウ設定
ALWAYS_ON_TOP = True
RANDOM_POSITION_MARGIN = 50
RANDOM_POSITION_OFFSET = 250

# リストビューカラム幅
COLUMN_ID_WIDTH = 0
COLUMN_DATE_WIDTH = 140
COLUMN_PREVIEW_WIDTH = 350
COLUMN_STATUS_WIDTH = 80

# メッセージ
MSG_SELECT_NOTE_TO_OPEN = "開く付箋を選択してください。"
MSG_SELECT_NOTE_TO_DELETE = "削除する付箋を選択してください。"
MSG_SELECT_NOTE_FOR_COLOR = "色を変更する付箋を選択してください。"
MSG_CONFIRM_DELETE = "選択した付箋を完全に削除しますか？\nこの操作は元に戻せません。"
MSG_ERROR_NOTE_DATA = "付箋データの取得に失敗しました。"
MSG_EMPTY_CONTENT = "(内容なし)"

# ステータスメッセージ
STATUS_READY = "準備完了"
STATUS_CREATED = "付箋を作成しました（ID: {}）"
STATUS_EDITING = "付箋を編集中（ID: {}）"
STATUS_DELETED = "付箋を削除しました（ID: {}）"
STATUS_COLOR_CHANGED = "付箋の色を変更しました（ID: {}）"
STATUS_LOADED = "{}個の付箋データを読み込みました"
STATUS_SAVED = "{}個の付箋を保存しました"
STATUS_LOAD_FAILED = "ノートの読み込みに失敗しました"
STATUS_SAVE_FAILED = "ノートの保存に失敗しました"
STATUS_NEW_FILE = "新規データファイルを作成します"