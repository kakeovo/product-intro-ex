# 本番デプロイ手順（Render 無料）

## ステップ1: GitHub へプッシュ

```bash
cd C:\Users\kubok\product-intro-ex

git init
git add .
git commit -m "Initial commit: Product Intro EX app"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/product-intro-ex.git
git push -u origin main
```

## ステップ2: Render でデプロイ

1. https://render.com にアクセス → サインアップ
2. 左メニュー "Blueprint" → "New Blueprint Instance"
3. GitHub リポジトリを連携
4. リポジトリを選択 → "Deploy"

**自動デプロイされるもの：**
- Python Web Service（Flask アプリ）
- PostgreSQL Database（無料）
- 環境変数自動設定

## ステップ3: 環境変数を設定

Render ダッシュボード → Web Service 選択 → "Environment"

以下を追加：

```
CLAUDE_API_KEY=sk-...  (あなたの Claude API キー)
NOTE_API_KEY=...        (Note API キー、オプション)
TWITTER_API_KEY=...     (Twitter API キー、オプション)
SECRET_KEY=your-random-secret-key-here
```

**DATABASE_URL は自動設定されます（Render PostgreSQL）**

## ステップ4: デプロイ確認

- ログを確認：Render ダッシュボード → "Logs"
- 以下が表示されたら成功：
  ```
  Scheduler started. Daily post at 09:00 JST
  ```

- アプリにアクセス：
  ```
  https://your-app-name.onrender.com
  ```

## ステップ5: 毎日の自動投稿確認

- 09:00 JST に自動で商品が投稿される
- Render Logs で投稿ログを確認
- Web UI → 投稿履歴 で履歴確認

## 無料枠の制限

| サービス | 無料枠 | 制限 |
|---------|--------|------|
| Render Web | 無料 | 15分無使用で停止、手動再起動必要 |
| PostgreSQL | 90日無料 | 以降有料化（約$7/月） |
| Claude API | $5クレジット | 超過したら課金 |

**推奨：** 本番運用時は Render PostgreSQL を有料化（月$7）に切り替え

## トラブルシューティング

### デプロイが失敗する
- ログを確認：Render Logs
- requirements.txt に全パッケージが入っているか確認
- Python version 指定を確認（3.11）

### スケジューラーが動かない
- Flask アプリが起動していることを確認
- Logs に "Scheduler started" があるか確認
- 時刻設定：POSTドTIME=09:00 (JST)

### API キーエラー
- Render Environment で設定を確認
- キーに空白がないか確認
- 無料ティアで API 制限がないか確認

## ローカルテスト（オプション）

デプロイ前にローカルで本番環境をシミュレート：

```bash
$env:DATABASE_URL = "postgresql://..."
$env:CLAUDE_API_KEY = "sk-..."
.\venv\Scripts\python.exe -m gunicorn wsgi:app
```

http://localhost:8000 でアクセス可能
