# クイックスタート（永遠無料デプロイ）

## 準備物

1. Claude API キー（https://console.anthropic.com）
2. GitHub アカウント
3. Render アカウント（https://render.com）
4. Neon.tech アカウント（https://neon.tech — 無料 PostgreSQL）

## 永遠無料でデプロイ

### ステップ1️⃣ GitHub にプッシュ

https://github.com/new で新規リポジトリを作成して、プッシュ：

```bash
cd C:\Users\kubok\product-intro-ex
git remote add origin https://github.com/YOUR_USERNAME/product-intro-ex.git
git branch -M main
git push -u origin main
```

### ステップ2️⃣ Neon.tech で PostgreSQL を作成

1. https://neon.tech にサインアップ
2. "Create project" → Project 作成
3. "Connection string" をコピー

**接続文字列の形式：**
```
postgresql://user:password@host/dbname
```

### ステップ3️⃣ Render でデプロイ

1. https://render.com でサインアップ
2. ダッシュボード → "New +" → "Web Service"
3. GitHub リポジトリを選択 → "product-intro-ex"
4. 以下を設定：
   - **Name**: product-intro-ex
   - **Runtime**: Python 3.11
   - **Build command**: `pip install -r requirements.txt`
   - **Start command**: `gunicorn wsgi:app`

### ステップ4️⃣ 環境変数を設定

Render Web Service → "Environment"

以下を追加：
```
DATABASE_URL=postgresql://...  (Neon.tech の接続文字列)
CLAUDE_API_KEY=sk-...
SECRET_KEY=your-random-secret-key
POST_TIME=09:00
```

### ステップ5️⃣ デプロイ確認

Logs に以下が表示されたら成功：
```
Scheduler started. Daily post at 09:00 JST
```

ブラウザで `https://your-app-name.onrender.com` でアクセス ✅

---

## 商品登録・実行

1. **Web UI → "商品を追加"** で URL を入力
2. **毎日 09:00 JST に自動投稿** 開始
3. **Web UI → "投稿履歴"** で確認

---

## 永遠無料コスト比較

| サービス | 無料枠 | 制限 |
|---------|--------|------|
| **Render Web** | ∞ | 15分無使用で停止（再起動で復帰） |
| **Neon PostgreSQL** | 3GB | 制限なし、永遠無料 |
| **Claude API** | $5 | 超過後課金（使用量に応じて） |

→ **データベース永遠無料** ✅  
→ Claude API のみ初期 $5 クレジット（その後課金）

---

## トラブルシューティング

| 問題 | 原因 | 解決 |
|-----|-----|------|
| DB接続エラー | DATABASE_URL が間違い | Neon から接続文字列を再コピー |
| Scheduler が起動しない | Flask アプリ起動失敗 | Render Logs を確認 |
| API キーエラー | 空白やタイプミス | 値を再入力、スペース削除 |

---

詳細は [DEPLOY.md](DEPLOY.md) を参照。
