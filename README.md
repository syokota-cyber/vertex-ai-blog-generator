# 🤖 Vertex AI Blog Generator

Google Vertex AI Gemini Pro を使用した高品質ブログ記事自動生成システム

## ✨ 特徴

- 🚀 **Google Gemini Pro**: 最新のAI技術による高品質コンテンツ生成
- 🎨 **カスタマイズ可能**: カテゴリ、文体、トーンを自由に調整
- 🌐 **美しいUI**: レスポンシブなモダンWebインターフェース
- ⚡ **高速生成**: 30秒以内でブログ記事を完成
- 🔗 **GitHub連携**: 自動デプロイメントとバージョン管理
- 🛡️ **堅牢性**: エラーハンドリングとヘルスチェック機能

## 🛠️ 技術スタック

### フロントエンド
- **HTML5/CSS3**: モダンでレスポンシブなUI
- **JavaScript**: インタラクティブな機能

### バックエンド
- **FastAPI**: 高性能Python Webフレームワーク
- **Pydantic**: データバリデーション
- **Uvicorn**: ASGI サーバー

### AI・クラウド
- **Vertex AI**: Google Cloud の AI プラットフォーム
- **Gemini Pro**: Google の大規模言語モデル
- **Cloud Run**: サーバーレスコンテナ実行環境

### DevOps
- **Docker**: コンテナ化
- **GitHub Actions**: CI/CD パイプライン
- **Google Cloud Build**: 自動ビルド

## 🚀 クイックスタート

### 前提条件

- Google Cloud Platform アカウント
- Vertex AI API の有効化
- GitHub アカウント

### デプロイ方法

#### 1. GitHub連携デプロイ（推奨）

```bash
# 1. このリポジトリをフォーク
# 2. Cloud Run コンソールでデプロイ
```

**Cloud Run設定:**
- ソース: GitHub リポジトリ
- ブランチ: main
- ビルドタイプ: Dockerfile
- リージョン: us-central1
- メモリ: 2GiB
- CPU: 1

#### 2. 手動デプロイ

```bash
# リポジトリクローン
git clone https://github.com/syokota-cyber/vertex-ai-blog-generator.git
cd vertex-ai-blog-generator

# Cloud Run デプロイ
gcloud run deploy vertex-ai-blog-generator \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### ローカル開発

```bash
# 依存関係インストール
pip install -r requirements.txt

# アプリケーション起動
uvicorn main:app --reload

# ブラウザでアクセス
open http://localhost:8000
```

## 🔧 設定

### 環境変数

| 変数名 | 説明 | デフォルト値 |
|--------|------|-------------|
| `GOOGLE_CLOUD_PROJECT` | GCP プロジェクトID | `gcp-handson-30days-30010` |
| `PORT` | アプリケーションポート | `8080` |

### 必要なGCP API

```bash
# API 有効化
gcloud services enable aiplatform.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

## 📡 API仕様

### エンドポイント

| メソッド | パス | 説明 |
|----------|------|------|
| `GET` | `/` | メインUI |
| `POST` | `/generate` | ブログ生成 |
| `GET` | `/health` | ヘルスチェック |

### ブログ生成リクエスト

```bash
curl -X POST "https://your-app-url/generate" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "topic=Vertex AIの活用方法&category=tech&tone=professional"
```

### ヘルスチェックレスポンス

```json
{
  "status": "healthy",
  "vertex_ai_available": true,
  "project_id": "your-project-id",
  "location": "us-central1",
  "version": "1.0.0"
}
```

## 🎯 使用例

### 1. 技術ブログ
- **トピック**: "Dockerコンテナ最適化のベストプラクティス"
- **カテゴリ**: 技術・プログラミング
- **トーン**: プロフェッショナル

### 2. ライフスタイル記事
- **トピック**: "リモートワークで生産性を上げる方法"
- **カテゴリ**: ライフスタイル
- **トーン**: フレンドリー

### 3. ビジネス記事
- **トピック**: "AIを活用したマーケティング戦略"
- **カテゴリ**: ビジネス
- **トーン**: プロフェッショナル

## 🔍 運用・監視

### ログ確認

```bash
# Cloud Run ログ
gcloud run services logs read vertex-ai-blog-generator --region us-central1

# リアルタイムログ
gcloud run services logs tail vertex-ai-blog-generator --region us-central1
```

### パフォーマンス監視

```bash
# サービス状態確認
gcloud run services describe vertex-ai-blog-generator --region us-central1

# メトリクス確認
# Cloud Console > Cloud Run > vertex-ai-blog-generator > メトリクス
```

## 🚧 トラブルシューティング

### よくある問題

#### 1. Vertex AI が利用できない

**症状**: "❌ Vertex AI 利用不可" と表示される

**解決策**:
```bash
# API 有効化確認
gcloud services list --enabled | grep aiplatform

# 権限確認
gcloud projects get-iam-policy YOUR_PROJECT_ID
```

#### 2. メモリ不足エラー

**症状**: Container が OOM で終了する

**解決策**: Cloud Run のメモリを 2GiB に増加

#### 3. タイムアウトエラー

**症状**: AI生成が時間切れになる

**解決策**: Cloud Run のタイムアウトを 300秒 に設定

## 🔄 アップデート

### 新機能追加時

```bash
# コード変更後
git add .
git commit -m "Add new feature: XXX"
git push origin main

# GitHub連携により自動デプロイされます
```

## 📊 Day24 学習目標達成

このプロジェクトは **GCP 30日トレーニング Day24** の成果物として、以下の学習目標を達成しています：

### ✅ 達成項目

- **Vertex AI (Generative) 入門**: Google Gemini Pro の実装
- **実際のAI生成**: モックではない本物のAI機能
- **Cloud Run デプロイ**: スケーラブルな本番環境
- **GitHub連携**: 自動デプロイメントパイプライン
- **エラーハンドリング**: 堅牢なシステム設計
- **UI/UX**: 実用的なWebインターフェース

### 📈 学習成果

1. **技術習得**
   - Vertex AI SDK の使用方法
   - FastAPI による REST API 開発
   - Docker コンテナ化
   - Cloud Run デプロイメント

2. **実践経験**
   - AI アプリケーション開発
   - エラーハンドリング設計
   - GitHub Actions CI/CD
   - プロダクションレベルの実装

## 🤝 コントリビューション

改善提案やバグ報告は Issue または Pull Request でお願いします。

### 開発ガイドライン

1. **ブランチ戦略**: `feature/機能名` でブランチ作成
2. **コミットメッセージ**: 英語で簡潔に記述
3. **テスト**: 機能追加時は動作確認必須
4. **ドキュメント**: README の更新も忘れずに

## 📄 ライセンス

MIT License - 詳細は [LICENSE](LICENSE) ファイルを参照

## 🙏 謝辞

- Google Cloud Platform
- Vertex AI チーム
- FastAPI コミュニティ
- オープンソースコミュニティ

---

**作成日**: 2025年7月6日  
**最終更新**: 2025年7月6日  
**バージョン**: 1.0.0  
**作成者**: Day24 学習プロジェクト