# Python付箋アプリ - モジュラー版

会社ＰＣで標準の「付箋」アプリが使用できない場合の代替として作成したシンプルなＰｙｔｈｏｎ製付箋アプリです。

このバージョンは**SOLID原則**に基づいてモジュール化され、可読性、保守性、拡張性が大幅に向上しています。

## 特徴

### 機能
- 複数の付箋を作成、管理
- 付箋の内容を自動保存
- 付箋の色をカスタマイズ
- 付箋をドラッグして移動可能
- アプリケーション終了後も付箋の状態を復元
- 最小化時にタスクバーに表示
- 付箋の検索機能
- プレビュー表示
- **固定サイズステータスバー**: ウィンドウサイズ変更時にフッターが潰れない

### アーキテクチャ

**SOLID原則を適用:**

1. **Single Responsibility Principle (単一責任原則)**
   - 各クラスは単一の責任を持つ
   - `NoteData`: 付箋データのみ担当
   - `StorageService`: データ永続化のみ担当

2. **Open/Closed Principle (開放・閉鎖原則)**
   - 拡張には開いているが修正には閉じている
   - `NoteRepositoryInterface`で新しいストレージ方式を簡単に追加可能

3. **Liskov Substitution Principle (リスコフの置換原則)**
   - サブタイプは基底タイプと置換可能
   - 異なるリポジトリ実装を透明に切り替え可能

4. **Interface Segregation Principle (インターフェース分離原則)**
   - クライアントは使用しないインターフェースに依存しない
   - コンポーネントごとに必要なインターフェースのみ提供

5. **Dependency Inversion Principle (依存性逆転原則)**
   - 高レベルモジュールは低レベルモジュールに依存しない
   - コントローラーは抽象インターフェースに依存

**レイヤー構造:**
```
Presentation Layer  (プレゼンテーション層)
│
│   views/          # UIコンポーネント
│   ├─ main_window.py
│   ├─ note_window.py 
│   └─ components/
│
Business Logic Layer (ビジネスロジック層)
│
│   controllers/     # ビジネスロジック
│   └─ note_controller.py
│
Service Layer      (サービス層)
│
│   services/        # サービスクラス
│   ├─ storage_service.py
│   └─ ui_service.py
│
Data Layer        (データ層)
│
│   models/          # データモデル
│   ├─ note_model.py
│   └─ note_repository.py
│
Utilities         (ユーティリティ)
│
└── utils/
    └─ constants.py
```

## ファイル構成

### メインファイル
- `app.py`: メインアプリケーションクラス
- `main_new.py`: **新しいエントリーポイント** 🆕
- `sticky_notes.json`: 付箋データの保存ファイル（自動生成）

> **重要**: 旧来の`main.py`はモジュラー版では**使用しません**。新しいエントリーポイントは`main_new.py`です。

### モジュール構成

#### `models/` - データモデル層
- `note_model.py`: 付箋データモデル
- `note_repository.py`: データ永続化の抽象化

#### `services/` - サービス層
- `storage_service.py`: データストレージサービス
- `ui_service.py`: UI関連サービス

#### `controllers/` - ビジネスロジック層
- `note_controller.py`: 付箋のビジネスロジック

#### `views/` - プレゼンテーション層
- `main_window.py`: メインウィンドウ
- `note_window.py`: 付箋ウィンドウ
- `components/note_list.py`: 付箋リストコンポーネント
- `components/preview_panel.py`: プレビューパネルコンポーネント

#### `utils/` - ユーティリティ
- `constants.py`: 定数定義

## 必要条件

- Python 3.8+
- tkinter（Pythonの標準ライブラリ）

## インストール方法

このリポジトリをクローンまたはダウンロードして使用できます。

```bash
git clone https://github.com/ShunsukeTamura06/tkinter_app.git
cd tkinter_app

# モジュラー版を実行 (新しい方法)
python main_new.py
```

## 使い方

### 基本操作

1. アプリを起動すると付箋管理ウィンドウが表示されます
2. 「新規作成」ボタンで付箋を作成します
3. 付箋に内容を入力します（フォーカスを失うと自動保存）
4. 付箋のメニューから「色の変更」で色を変更できます
5. 付箋は画面上でドラッグして自由に配置できます
6. 不要な付箋はリストから選択して削除できます
7. アプリを終了すると、すべての付箋情報が保存されます

### 高度な機能

- **検索**: 付箋リストの検索ボックスで内容を検索
- **プレビュー**: リストで付箋を選択すると下部にプレビュー表示
- **コンテキストメニュー**: 右クリックで色変更や削除などの操作
- **キーボードショートカット**: Ctrl+Sで手動保存
- **固定サイズステータスバー**: ウィンドウサイズ変更時にフッターが潰れない

## モジュラーアーキテクチャの利点

### 保守性
- 各クラスが単一責任を持ち、修正が容易
- コードの結合度が低く、変更が他に影響しにくい

### 拡張性
- 新しいストレージ形式（XML、SQLiteなど）を簡単に追加可能
- 新しいUIコンポーネントを独立して開発可能

### テスタビリティ
- 各モジュールを独立してテスト可能
- モックオブジェクトを使った単体テストが容易

### 可読性
- コードが組織化され、理解しやすい
- 各クラスの役割が明確

## 開発者向け情報

### アーキテクチャパターン

- **Repository Pattern**: データアクセスの抽象化
- **Service Layer Pattern**: ビジネスロジックのカプセル化
- **Observer Pattern**: コールバックベースのイベント処理
- **Dependency Injection**: 依存性の注入

### カスタマイズ方法

新しいストレージ形式を追加する場合:

```python
# 新しいリポジトリクラスを作成
class DatabaseNoteRepository:
    def load_all(self) -> List[NoteData]:
        # データベースから読み込み
        pass
    
    def save_all(self, notes: List[NoteData]) -> bool:
        # データベースに保存
        pass

# アプリケーションで使用
storage_service = StorageService(DatabaseNoteRepository())
```

新しいUIコンポーネントを追加する場合:

```python
class TagPanelComponent:
    def __init__(self, parent: tk.Widget):
        # タグ機能を持つコンポーネント
        pass

# メインウィンドウに組み込み
self.tag_panel = TagPanelComponent(self.some_frame)
```

## バグ修正履歴

- **v2.1.0**: 付箋ウィンドウ閉じるエラーを修正（masterパラメーターの正しい設定）
- **v2.0.1**: ステータスバーの固定高さ化（ウィンドウサイズ変更時の潰れ防止）

## 更新履歴

- 2025-07-08: 付箋ウィンドウ閉じるエラー修正、ステータスバー固定高さ化
- 2025-03-18: SOLID原則に基づくモジュール化リファクタリング
- 2025-03-18: READMEの修正、正確なリポジトリ情報を追加

## ライセンス

MITライセンス