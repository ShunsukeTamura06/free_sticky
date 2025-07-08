#!/usr/bin/env python3
"""
付箋アプリケーションのエントリーポイント

SOLID原則に基づいてモジュール化されたアーキテクチャ:

- Single Responsibility Principle: 各クラスは単一の責任を持つ
- Open/Closed Principle: 拡張には開いているが修正には閉じている
- Liskov Substitution Principle: サブタイプは基底タイプと置換可能
- Interface Segregation Principle: クライアントは使用しないインターフェースに依存しない
- Dependency Inversion Principle: 高レベルモジュールは低レベルモジュールに依存しない

アーキテクチャ構造:

app.py                    # メインアプリケーションクラス
controllers/             # ビジネスロジック層
  note_controller.py     # 付箋のビジネスロジック
models/                  # データモデル層
  note_model.py          # 付箋データモデル
  note_repository.py     # データ永続化抽象化
services/                # サービス層
  storage_service.py     # データストレージサービス
  ui_service.py          # UI関連サービス
views/                   # プレゼンテーション層
  main_window.py         # メインウィンドウ
  note_window.py         # 付箋ウィンドウ
  components/            # UIコンポーネント
    note_list.py         # 付箋リストコンポーネント
    preview_panel.py     # プレビューパネルコンポーネント
utils/                   # ユーティリティ
  constants.py           # 定数定義

使用方法:
    python main_new.py
"""

if __name__ == "__main__":
    try:
        from app import StickyNoteApplication
        
        # アプリケーションの作成と実行
        app = StickyNoteApplication()
        app.run()
        
    except ImportError as e:
        print(f"モジュールのインポートに失敗しました: {e}")
        print("必要なファイルが存在するか確認してください。")
    except Exception as e:
        print(f"アプリケーションの実行中にエラーが発生しました: {e}")
        import traceback
        traceback.print_exc()