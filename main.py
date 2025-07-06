from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import os
import logging

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Vertex AI Blog Generator",
    description="Google Gemini Pro でブログ記事を自動生成",
    version="1.0.0"
)

# Vertex AI インポート
try:
    import vertexai
    from vertexai.generative_models import GenerativeModel
    VERTEX_AI_AVAILABLE = True
    logger.info("✅ Vertex AI libraries loaded successfully")
except ImportError as e:
    VERTEX_AI_AVAILABLE = False
    logger.error(f"❌ Vertex AI libraries not available: {e}")

# 設定
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "gcp-handson-30days-30010")
LOCATION = "us-central1"

class BlogGenerator:
    def __init__(self):
        self.available = False
        self.model = None
        self.error_message = None
        
        if VERTEX_AI_AVAILABLE:
            try:
                logger.info("🚀 Vertex AI初期化中...")
                vertexai.init(project=PROJECT_ID, location=LOCATION)
                self.model = GenerativeModel("gemini-1.5-pro")
                self.available = True
                logger.info("✅ Vertex AI Gemini Pro 初期化完了")
            except Exception as e:
                self.error_message = str(e)
                logger.error(f"❌ Vertex AI初期化失敗: {e}")
        else:
            self.error_message = "Vertex AI ライブラリが利用できません"
    
    def generate_blog(self, topic: str, category: str, tone: str):
        """ブログ生成メソッド"""
        if not self.available:
            return {
                "success": False,
                "error": f"Vertex AI利用不可: {self.error_message}",
                "content": f"# {topic}\n\nVertex AIが利用できません。\n\nエラー詳細: {self.error_message}",
                "word_count": 0,
                "source": "Error System"
            }
        
        try:
            # プロンプト構築
            prompt = f"""
あなたは経験豊富なプロのブログライターです。以下の条件で魅力的で実用的なブログ記事を作成してください。

## 記事条件
- **トピック**: {topic}
- **カテゴリ**: {category}
- **文体**: {tone}
- **文字数**: 800-1200文字程度

## 記事構成要件
1. **魅力的なタイトル** - SEOを意識し、読者の関心を引く
2. **導入部** - 読者の問題意識に共感し、記事の価値を示す
3. **本文** - 具体例、体験談、実践的なアドバイスを含む
4. **見出しの活用** - 読みやすい構造化（##、###を使用）
5. **まとめ** - 要点の振り返りと行動喚起

## 重要なポイント
- 読者にとって実用的で価値のある内容
- 具体的な例やエピソードを含める
- 専門性を示しつつ、分かりやすい説明
- 読者が実際に行動に移せるアドバイス

それでは、上記の条件に従ってブログ記事を作成してください：
"""
            
            # Gemini API呼び出し
            response = self.model.generate_content(
                prompt,
                generation_config={
                    "max_output_tokens": 2048,
                    "temperature": 0.7,
                    "top_p": 0.8,
                    "top_k": 40
                }
            )
            
            content = response.text
            word_count = len(content.split())
            
            logger.info(f"✅ ブログ生成成功: {word_count}語")
            
            return {
                "success": True,
                "content": content,
                "source": "Vertex AI Gemini Pro",
                "word_count": word_count,
                "topic": topic,
                "category": category,
                "tone": tone
            }
            
        except Exception as e:
            error_msg = f"AI生成エラー: {str(e)}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg,
                "content": f"# {topic}\n\n生成中にエラーが発生しました。\n\n詳細: {error_msg}",
                "word_count": 0,
                "source": "Error"
            }

# ブログ生成器初期化
blog_generator = BlogGenerator()

@app.get("/", response_class=HTMLResponse)
async def home():
    """メインページ"""
    status = "✅ 利用可能" if blog_generator.available else "❌ 利用不可"
    status_color = "#28a745" if blog_generator.available else "#dc3545"
    error_detail = blog_generator.error_message if not blog_generator.available else "Gemini Pro モデル初期化完了"
    
    return HTMLResponse(f"""
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vertex AI Blog Generator</title>
    <style>
        body {{
            font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }}
        .container {{
            background: white;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 30px;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }}
        .header p {{
            margin: 10px 0 0 0;
            opacity: 0.9;
            font-size: 1.1em;
        }}
        .status {{
            background: #f8f9fa;
            padding: 25px;
            border-left: 4px solid {status_color};
            margin: 0;
        }}
        .status h3 {{
            margin: 0 0 15px 0;
            color: #333;
        }}
        .status-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-top: 15px;
        }}
        .status-item {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #e9ecef;
        }}
        .form-container {{
            padding: 40px;
        }}
        .form-group {{
            margin: 25px 0;
        }}
        label {{
            display: block;
            font-weight: 600;
            margin-bottom: 8px;
            color: #333;
            font-size: 1.1em;
        }}
        input, select {{
            width: 100%;
            padding: 15px;
            border: 2px solid #e9ecef;
            border-radius: 10px;
            font-size: 16px;
            transition: border-color 0.3s ease;
            box-sizing: border-box;
        }}
        input:focus, select:focus {{
            border-color: #667eea;
            outline: none;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }}
        .btn {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 18px 30px;
            border: none;
            border-radius: 10px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
            margin-top: 20px;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        .btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        }}
        .btn:active {{
            transform: translateY(0);
        }}
        .github {{
            text-align: center;
            margin: 20px 40px;
            padding: 20px;
            background: #f6f8fa;
            border-radius: 10px;
            border: 1px solid #d0d7de;
        }}
        .github a {{
            color: #0366d6;
            text-decoration: none;
            font-weight: 600;
        }}
        .error-detail {{
            font-size: 13px;
            color: #666;
            margin-top: 8px;
            word-break: break-word;
        }}
        .feature-list {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}
        .feature-item {{
            text-align: center;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI Blog Generator</h1>
            <p>Google Vertex AI Gemini Pro による高品質ブログ記事生成</p>
        </div>
        
        <div class="status">
            <h3>🔮 AI エンジン状態</h3>
            <div class="status-grid">
                <div class="status-item">
                    <strong>Vertex AI Gemini Pro</strong><br>
                    <span style="color: {status_color}; font-weight: bold;">{status}</span>
                </div>
                <div class="status-item">
                    <strong>プロジェクト</strong><br>
                    {PROJECT_ID}
                </div>
                <div class="status-item">
                    <strong>リージョン</strong><br>
                    {LOCATION}
                </div>
                <div class="status-item">
                    <strong>デプロイ方式</strong><br>
                    GitHub連携
                </div>
            </div>
            <div class="error-detail"><strong>詳細:</strong> {error_detail}</div>
        </div>
        
        <div class="github">
            <h4>📂 GitHub リポジトリ</h4>
            <p>このアプリケーションのソースコード</p>
            <a href="https://github.com/syokota-cyber/vertex-ai-blog-generator" target="_blank">
                🔗 GitHub で見る
            </a>
        </div>

        <div class="form-container">
            <h2 style="text-align: center; color: #333; margin-bottom: 30px;">ブログ記事を生成</h2>
            
            <div class="feature-list">
                <div class="feature-item">
                    <div style="font-size: 24px;">🤖</div>
                    <strong>AI生成</strong><br>
                    高品質なコンテンツ
                </div>
                <div class="feature-item">
                    <div style="font-size: 24px;">🎨</div>
                    <strong>カスタマイズ</strong><br>
                    トーン・カテゴリ調整
                </div>
                <div class="feature-item">
                    <div style="font-size: 24px;">⚡</div>
                    <strong>高速生成</strong><br>
                    30秒以内で完成
                </div>
            </div>

            <form method="post" action="/generate">
                <div class="form-group">
                    <label for="topic">📝 ブログのトピック</label>
                    <input type="text" id="topic" name="topic" 
                           placeholder="例：初心者向けのVertex AI活用ガイド" 
                           required>
                </div>
                
                <div class="form-group">
                    <label for="category">📂 カテゴリ</label>
                    <select id="category" name="category">
                        <option value="tech">🔧 技術・プログラミング</option>
                        <option value="lifestyle">🌱 ライフスタイル</option>
                        <option value="business">💼 ビジネス</option>
                        <option value="travel">✈️ 旅行・観光</option>
                        <option value="education">📚 教育・学習</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="tone">🎭 文体・トーン</label>
                    <select id="tone" name="tone">
                        <option value="professional">👔 プロフェッショナル</option>
                        <option value="friendly">😊 フレンドリー</option>
                        <option value="casual">😎 カジュアル</option>
                    </select>
                </div>
                
                <button type="submit" class="btn">
                    🚀 Gemini AI でブログを生成する
                </button>
            </form>
        </div>
    </div>
    
    <div style="text-align: center; margin: 30px 0; font-size: 14px; color: #666;">
        <p>Powered by Google Cloud Vertex AI | Deployed via GitHub Actions</p>
    </div>
</body>
</html>
""")

@app.post("/generate", response_class=HTMLResponse)
async def generate(
    topic: str = Form(...), 
    category: str = Form("tech"), 
    tone: str = Form("professional")
):
    """ブログ生成エンドポイント"""
    logger.info(f"🤖 ブログ生成リクエスト受信: {topic}")
    
    # AI生成実行
    result = blog_generator.generate_blog(topic, category, tone)
    
    # 結果に応じた表示設定
    if result["success"]:
        status_color = "#28a745"
        status_text = "🎉 生成成功"
        status_bg = "linear-gradient(135deg, #28a745 0%, #20c997 100%)"
    else:
        status_color = "#dc3545"
        status_text = "❌ 生成失敗"
        status_bg = "linear-gradient(135deg, #dc3545 0%, #c82333 100%)"
    
    return HTMLResponse(f"""
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>生成結果 - {topic}</title>
    <style>
        body {{
            font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }}
        .container {{
            background: white;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            background: {status_bg};
            color: white;
            padding: 40px 30px;
        }}
        .status {{
            color: white;
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        .topic {{
            font-size: 1.3em;
            opacity: 0.95;
            margin: 0;
        }}
        .nav {{
            text-align: center;
            padding: 25px;
            background: #f8f9fa;
        }}
        .nav a {{
            color: white;
            text-decoration: none;
            padding: 12px 25px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 8px;
            font-weight: 600;
            margin: 0 10px;
            transition: transform 0.2s ease;
            display: inline-block;
        }}
        .nav a:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }}
        .meta {{
            background: #e7f3ff;
            padding: 25px;
            border-left: 4px solid #007bff;
        }}
        .meta-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }}
        .meta-item {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }}
        .content {{
            padding: 40px;
        }}
        .content h2 {{
            color: #333;
            margin-bottom: 25px;
            text-align: center;
        }}
        .blog-content {{
            background: #f8f9fa;
            padding: 30px;
            border-radius: 15px;
            border: 1px solid #e9ecef;
            line-height: 1.8;
        }}
        pre {{
            white-space: pre-wrap;
            font-family: Georgia, 'Times New Roman', serif;
            font-size: 16px;
            margin: 0;
            color: #333;
        }}
        .error-content {{
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="status">{status_text}</div>
            <h1>📄 ブログ生成結果</h1>
            <p class="topic">{topic}</p>
        </div>
        
        <div class="nav">
            <a href="/">🔄 新しい記事を生成</a>
            <a href="https://github.com/syokota-cyber/vertex-ai-blog-generator" target="_blank">📂 GitHub</a>
        </div>
        
        <div class="meta">
            <h3>📊 生成情報</h3>
            <div class="meta-grid">
                <div class="meta-item">
                    <strong>生成エンジン</strong><br>
                    {result.get('source', 'System')}
                </div>
                <div class="meta-item">
                    <strong>カテゴリ</strong><br>
                    {result.get('category', category)}
                </div>
                <div class="meta-item">
                    <strong>文体</strong><br>
                    {result.get('tone', tone)}
                </div>
                <div class="meta-item">
                    <strong>文字数</strong><br>
                    {result.get('word_count', 0)}語
                </div>
            </div>
        </div>
        
        <div class="content">
            <h2>📝 生成されたブログ記事</h2>
            <div class="blog-content {'error-content' if not result['success'] else ''}">
                <pre>{result['content']}</pre>
            </div>
        </div>
        
        <div class="nav">
            <a href="/">🆕 別の記事を生成する</a>
        </div>
    </div>
</body>
</html>
""")

@app.get("/health")
async def health_check():
    """ヘルスチェックエンドポイント"""
    return {
        "status": "healthy",
        "vertex_ai_available": blog_generator.available,
        "project_id": PROJECT_ID,
        "location": LOCATION,
        "version": "1.0.0",
        "error": blog_generator.error_message if not blog_generator.available else None
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)