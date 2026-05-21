# 商品紹介EX

毎日ランダムに商品（趣味嗜好の合う）を紹介して、アフィリエイト報酬を得るアプリケーション。

## 機能

- 毎日自動で商品を抽選・紹介する
- 商品リンク（URL）の登録・管理
- 過去紹介した商品の履歴管理（同じ紹介をしない）
- アフィリエイトリンク の自動変換
- 紹介文の自動生成（Claude API利用）
- Note・Twitter への自動投稿
- Web管理画面（ダッシュボード、商品管理、投稿履歴）

## セットアップ

### ローカル開発環境

1. **リポジトリをクローン**
```bash
cd product-intro-ex
```

2. **Python 仮想環境を作成**
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

3. **依存パッケージをインストール**
```bash
pip install -r requirements.txt
```

4. **環境変数を設定**
```bash
cp .env.example .env
# .env を編集して、各種APIキーを入力
```

5. **アプリケーションを起動**
```bash
python -m flask --app app.main run
# または
python app/main.py
```

ブラウザで `http://localhost:5000` にアクセス。

### 本番環境（Render/Railway）

1. **Render の場合**
   - `render.yaml` を使用して自動デプロイ
   - PostgreSQL は無料枠を使用

2. **Railway の場合**
   - `requirements.txt` を使用
   - PostgreSQL を接続

3. **環境変数の設定**
   - `CLAUDE_API_KEY`：Claude APIキー
   - `NOTE_API_KEY`：Note APIキー（オプション）
   - `TWITTER_API_KEY` など：Twitter APIキー（オプション）
   - `SECRET_KEY`：Flask用シークレットキー

## 使い方

### Web管理画面

- **ダッシュボード**: 登録商品数、総投稿数、最近の投稿を表示
- **商品管理**: 商品の登録・削除
- **投稿履歴**: 過去の投稿ログを表示

### API

#### 商品登録
```bash
POST /api/products
Content-Type: application/json

{
  "url": "https://example.com/product"
}
```

#### 商品一覧取得
```bash
GET /api/products
```

#### 投稿履歴取得
```bash
GET /api/history
```

## 自動スケジューリング

毎日 09:00 JST に自動で商品を抽選・投稿します（`.env` の `POST_TIME` で変更可）。

## 技術スタック

- **言語**: Python 3.11+
- **フレームワーク**: Flask
- **データベース**: PostgreSQL（本番）/ SQLite（開発）
- **ORM**: SQLAlchemy
- **自動スケジュール**: APScheduler
- **API**: Claude API, Note API, Twitter API
- **デプロイ**: Render / Railway

## 設定項目

`.env` ファイルで設定可能：

```env
DATABASE_URL=postgresql://user:pass@host:5432/db
CLAUDE_API_KEY=sk-...
NOTE_API_KEY=...
TWITTER_API_KEY=...
POST_TIME=09:00
SCHEDULER_TIMEZONE=Asia/Tokyo
```

## トラブルシューティング

### 「No module named 'anthropic'」エラー
```bash
pip install anthropic
```

### データベース接続エラー
```bash
# ローカルの場合、SQLiteを使用（自動）
# 本番の場合、DATABASE_URLを確認
```

### スケジューラーが動かない
- Flask アプリケーションが起動中であることを確認
- ログで `Scheduler started` メッセージを確認

## 開発予定

- [ ] ユーザー趣味嗜好の学習機能
- [ ] エンゲージメント分析
- [ ] 季節・トレンド対応
- [ ] モバイルアプリ版

## ライセンス

個人利用のみ。

## 注意事項

- アフィリエイト報酬は API では自動化されません（ASP の手動処理）
- SNS API の仕様変更に注意
- Claude API は従量課金制（月額コストを監視してください）
