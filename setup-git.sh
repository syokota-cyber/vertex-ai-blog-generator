#!/bin/bash

# Vertex AI Blog Generator - Git初期化とGitHub連携スクリプト

echo "🎯 Vertex AI Blog Generator - Git初期化開始"
echo ""

# プロジェクトディレクトリに移動
cd /Users/syokota_mac/Desktop/vertex-ai-blog-generator

echo "📂 現在のディレクトリ:"
pwd

echo ""
echo "📝 作成されたファイル一覧:"
ls -la

echo ""
echo "🔧 Git初期化..."

# Git初期化
git init

# すべてのファイルをステージング
git add .

# 初回コミット
git commit -m "Initial commit: Vertex AI Blog Generator

✨ Features:
- Google Vertex AI Gemini Pro integration
- Beautiful responsive web UI
- Real-time AI blog generation
- Docker containerization
- Health check endpoints
- Comprehensive error handling

🛠️ Tech Stack:
- FastAPI + Uvicorn
- Vertex AI SDK
- Docker + Cloud Run
- GitHub Actions ready

📊 Day24 Achievement:
- Complete Vertex AI implementation
- Production-ready deployment
- GitHub integration setup"

echo ""
echo "🔗 GitHubリポジトリと連携..."

# GitHubリモートリポジトリを追加
git remote add origin https://github.com/syokota-cyber/vertex-ai-blog-generator.git

# ブランチをmainに設定
git branch -M main

echo ""
echo "📤 GitHubにプッシュ..."

# GitHubにプッシュ
git push -u origin main

echo ""
echo "🎉 Git初期化とGitHubプッシュ完了！"
echo ""
echo "📋 次の手順:"
echo "1. ✅ ファイル作成完了"
echo "2. ✅ Git初期化完了"
echo "3. ✅ GitHubプッシュ完了"
echo "4. 🌐 Cloud Run コンソールでデプロイ"
echo ""
echo "🔗 Cloud Run デプロイURL:"
echo "https://console.cloud.google.com/run/create"
echo ""
echo "⚙️  設定値:"
echo "- ソースリポジトリから継続的にデプロイする"
echo "- GitHub リポジトリ: syokota-cyber/vertex-ai-blog-generator"
echo "- ブランチ: main"
echo "- ビルドタイプ: Dockerfile"
echo "- サービス名: vertex-ai-blog-generator"
echo "- リージョン: us-central1"
echo "- CPU: 1"
echo "- メモリ: 2GiB"
echo "- 最大インスタンス数: 10"
echo "- 認証: 未認証の呼び出しを許可"