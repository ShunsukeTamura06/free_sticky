# モジュラー版への移行ガイド

旧来の`main.py`から新しいモジュラー版への移行手順です。

## 主な変更点

### エントリーポイントの変更

**旧:**
```bash
python main.py
```

**新:**
```bash
python main_new.py
```

### ファイル構成の変更

**旧来版** (単一ファイル):
```
main.py                   # すべてのコード (32KB)
sticky_notes.json         # データファイル
```

**モジュラー版** (分割された構造):
```
app.py                    # メインアプリケーション
main_new.py               # エントリーポイント
controllers/              # ビジネスロジック
models/                   # データモデル
services/                 # サービス層
views/                    # UIコンポーネント
utils/                    # ユーティリティ
sticky_notes.json         # データファイル (互換性あり)
```

## 移行手順

### 1. 新しいバージョンをダウンロード

```bash
git pull origin main
# または
# git clone https://github.com/ShunsukeTamura06/tkinter_app.git
```

### 2. 既存のデータのバックアップ

```bash
# 保存された付箋データをバックアップ
cp sticky_notes.json sticky_notes.json.bak
```

### 3. 新しいエントリーポイントで実行

```bash
python main_new.py
```

### 4. 既存データの確認

- アプリが起動したら、既存の付箋データが正しく読み込まれているか確認
- 付箋の作成、編集、削除などが正常に動作するかテスト

## 互換性

### データファイル
- `sticky_notes.json`の形式は**完全に互換**です
- 既存の付箋データはそのまま使用できます

### 機能
- すべての既存機能が維持されています
- UIの操作方法に変更はありません

## トラブルシューティング

### モジュールが見つからないエラー

```
ModuleNotFoundError: No module named 'models'
```

**解決方法:**
1. カレントディレクトリがプロジェクトルートにあるか確認
2. 必要なフォルダがすべて存在するか確認

### 旧来版との同時実行

- 旧来版(`main.py`)とモジュラー版(`main_new.py`)は同じ`sticky_notes.json`を使用します
- 同時に実行してもデータの競合状態は発生しません

### パフォーマンスの変化

- モジュラー版はファイル読み込み時間がわずかに増加します
- メモリ使用量に大きな変化はありません
- 実際の使用時には体感できる差はありません

## ロールバック手順

万一問題が発生した場合、旧来版に戻すことができます:

```bash
# バックアップしたデータを復元
cp sticky_notes.json.bak sticky_notes.json

# 旧来版で実行 (ある場合)
python main.py
```

## サポート

問題が発生した場合は、GitHubのIssueで報告してください:
https://github.com/ShunsukeTamura06/tkinter_app/issues

報告時には以下の情報を含めてください:
- Pythonのバージョン
- OSの種類
- エラーメッセージの全文
- 再現手順