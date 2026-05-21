# 本番デプロイ手順（永遠無料）

Render + Neon.tech の完全無料組み合わせ。PostgreSQL が 90 日後に自動課金されません。

## ステップ1: GitHub へプッシュ

```bash
cd C:\Users\kubok\product-intro-ex
git remote add origin https://github.com/YOUR_USERNAME/product-intro-ex.git
git branch -M main
git push -u origin main
```

## ステップ2: Neon.tech で PostgreSQL を作成

1. **サインアップ**
   - https://neon.tech にアクセス
   - Google/GitHub でサインアップ

2. **プロジェクト作成**
   - "Create project" をクリック
   - プロジェクト名：`product-intro-ex`
   - Region：Tokyo（またはお近くの地域）

3. **接続文字列を取得**
   - "Connection string" タブ
   - "Connection string" をコピー
   - 形式：`postgresql://user:password@host/dbname`

## ステップ3: Render でデプロイ

1. **サインアップ**
   - https://render.com にアクセス
   - GitHub でサインアップ

2. **Web Service を作成**
   - ダッシュボード → "New Web Service"
   - GitHub リポジトリを選択：`product-intro-ex`
   - 以下を入力：
     - **Name**: `product-intro-ex`
     - **Runtime**: Python 3.11
     - **Build command**: `pip install -r requirements.txt`
     - **Start command**: `gunicorn wsgi:app`

3. **"Create Web Service" をクリック**

⏳ **デプロイ開始：** 3-5分待つ

## ステップ4: 環境変数を設定

Render ダッシュボード → Web Service → "Environment"

以下を追加：

```
DATABASE_URL=postgresql://...  (Neon.tech から取得)
CLAUDE_API_KEY=sk-...           (Claude API キー)
SECRET_KEY=your-random-secret-key-here
POST_TIME=09:00
SCHEDULER_TIMEZONE=Asia/Tokyo
```

**Neon.tech の接続文字列をコピペするときの注意：**
```
# コピーした文字列の最後に ?sslmode=require が付いているなら削除しない
# そのままペースト
```

## ステップ5: デプロイ確認

1. **Render Logs を確認**
   ```
   Scheduler started. Daily post at 09:00 JST
   ```

2. **Web にアクセス**
   ```
   https://your-app-name.onrender.com
   ```

3. **ダッシュボードが表示される** → 成功 ✅

## 永遠無料の条件

| サービス | 無料枠 | 期限 |
|---------|--------|------|
| Render Web | ∞ | なし |
| Neon PostgreSQL | 3GB | **永遠無料** ✅ |
| Claude API | $5 | 初期クレジット |

→ **データベースは 100% 永遠無料**

## トラブルシューティング

### データベース接続エラー
```
Error: could not connect to server
```
- Neon.tech の接続文字列を再確認
- DATABASE_URL にスペースがないか確認
- Neon.tech のプロジェクトがアクティブか確認

### Scheduler が起動しない
```
Scheduler started というログが出ない
```
- Flask アプリが完全に起動しているか確認
- Logs に Python エラーがないか確認

### API キーエラー
```
API error: invalid key
```
- Claude API キーが正確か確認
- 初期 $5 クレジットが残っているか確認

## ローカルでテスト

```bash
$env:DATABASE_URL = "postgresql://user:pass@host/db"
$env:CLAUDE_API_KEY = "sk-..."
.\venv\Scripts\python.exe -m gunicorn wsgi:app
```

http://localhost:8000 でアクセス

## Neon.tech で DB を確認

1. Neon.tech ダッシュボード → プロジェクト
2. "SQL Editor" で直接 DB を操作可能
3. 商品・投稿履歴が保存されているか確認

## 参考

- [Neon.tech ドキュメント](https://neon.tech/docs)
- [Render ドキュメント](https://render.com/docs)
- [Flask ドキュメント](https://flask.palletsprojects.com)

