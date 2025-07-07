from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import os
import logging
from datetime import datetime

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Vertex AI Blog Generator Pro",
    description="Google Gemini 2.5 Pro で長文ブログ記事を自動生成",
    version="2.0.0"
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
                self.model = GenerativeModel("gemini-2.5-pro")
                self.available = True
                logger.info("✅ Vertex AI Gemini 2.5 Pro 初期化完了")
            except Exception as e:
                self.error_message = str(e)
                logger.error(f"❌ Vertex AI初期化失敗: {e}")
        else:
            self.error_message = "Vertex AI ライブラリが利用できません"
    
    def generate_blog(self, topic: str, category: str, tone: str):
        """ブログ生成メソッド（1,500-2,000文字対応）"""
        if not self.available:
            return {
                "success": False,
                "error": f"Vertex AI利用不可: {self.error_message}",
                "content": f"# {topic}\n\nVertex AIが利用できません。\n\nエラー詳細: {self.error_message}",
                "word_count": 0,
                "source": "Error System"
            }
        
        try:
            # 現在の日付取得
            current_date = datetime.now().strftime("%Y年%m月")
            
            # カテゴリ別の専門的なアプローチ
            category_prompts = {
                "tech": "最新の技術動向、実装例、ベストプラクティス、将来性を含めて",
                "lifestyle": "日常生活への影響、実体験、具体的なメリット・デメリットを含めて",
                "business": "ビジネス価値、ROI、導入事例、競合分析を含めて",
                "travel": "実際の体験、おすすめスポット、予算感、注意点を含めて",
                "education": "学習効果、実践方法、段階的なアプローチ、成果測定を含めて"
            }
            
            # トーン別の文体調整
            tone_instructions = {
                "professional": "専門的で信頼性の高い文体で、データや事実を重視して",
                "friendly": "親しみやすく共感を呼ぶ文体で、読者との距離を近く感じられるように",
                "casual": "気軽で親近感のある文体で、日常会話のような自然さで"
            }
            
            # 強化されたプロンプト構築
            prompt = f"""
あなたは{current_date}時点の最新情報に精通した、経験豊富なプロフェッショナルライターです。
以下の条件で、読者にとって極めて価値の高い長文ブログ記事を作成してください。

## 📋 記事仕様
- **トピック**: {topic}
- **カテゴリ**: {category}
- **文体**: {tone_instructions.get(tone, "バランスの取れた")}
- **文字数**: 1,500～2,000文字（必須要件）
- **専門領域**: {category_prompts.get(category, "一般的な内容")}

## 📖 記事構成（必須）
1. **魅力的なタイトル** (##使用)
   - SEOを意識し、読者の興味を最大限に引く
   - 数字や具体的な価値提案を含める

2. **導入部** (150-200文字)
   - 読者の課題や関心事に直接言及
   - 記事を読むことで得られる価値を明確に提示
   - 問いかけや統計データで関心を引く

3. **主要コンテンツ** (1,200-1,500文字)
   - ### で区切られた3-5つのセクション
   - 各セクションに具体例、データ、体験談を含める
   - 実践的なアドバイスやステップバイステップの解説
   - 読者が実際に行動に移せる具体的な方法論

4. **実践例・事例紹介** (200-300文字)
   - 成功事例や失敗から学ぶポイント
   - 具体的な数値や成果を含める

5. **まとめ・行動喚起** (100-150文字)
   - 要点の整理と次のステップの提案
   - 読者が今すぐできることを具体的に提示

## 🎯 重要な要件
✅ **{current_date}現在の最新情報**として執筆
✅ **過去の年号や古い情報は一切使用しない**
✅ **専門性と読みやすさの両立**
✅ **具体的な数値、事例、体験談を豊富に含める**
✅ **読者が実際に行動に移せる実践的なアドバイス**
✅ **SEO効果の高い自然なキーワード配置**
✅ **論理的で説得力のある構成**

## 📝 文章スタイル
- {tone_instructions.get(tone, "読みやすい")}
- 一文が長すぎないよう配慮
- 見出しで適切に区切り、読みやすい構造
- 読者の関心を維持する魅力的な表現

それでは、上記の条件に完全に従って、1,500-2,000文字の高品質なブログ記事を作成してください：
"""
            
            # Gemini API呼び出し（長文生成用パラメータ調整）
            response = self.model.generate_content(
                prompt,
                generation_config={
                    "max_output_tokens": 4096,  # 長文対応
                    "temperature": 0.8,  # 創造性を高める
                    "top_p": 0.9,
                    "top_k": 40
                }
            )
            
            content = response.text
            word_count = len(content.replace(" ", ""))  # 日本語文字数
            
            logger.info(f"✅ 長文ブログ生成成功: {word_count}文字")
            
            return {
                "success": True,
                "content": content,
                "source": "Vertex AI Gemini 2.5 Pro",
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
    """メインページ（長文生成対応UI）"""
    status = "✅ 利用可能" if blog_generator.available else "❌ 利用不可"
    status_color = "#28a745" if blog_generator.available else "#dc3545"
    error_detail = blog_generator.error_message if not blog_generator.available else "Gemini 2.5 Pro モデル初期化完了"
    
    return HTMLResponse(f"""
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vertex AI Blog Generator Pro</title>
    <style>
        body {{
            font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .container {{
            background: white;
            border-radius: 25px;
            overflow: hidden;
            box-shadow: 0 25px 50px rgba(0,0,0,0.15);
        }}
        .header {{
            text-align: center;
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 50px 30px;
        }}
        .header h1 {{
            margin: 0;
            font-size: 3em;
            font-weight: 300;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        .header .subtitle {{
            margin: 15px 0;
            opacity: 0.9;
            font-size: 1.3em;
        }}
        .badge {{
            background: #e74c3c;
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
            display: inline-block;
            margin-top: 10px;
        }}
        .status {{
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 30px;
            border-left: 4px solid {status_color};
            margin: 0;
        }}
        .status h3 {{
            margin: 0 0 20px 0;
            color: #333;
            font-size: 1.4em;
        }}
        .status-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        .status-item {{
            background: white;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #e9ecef;
            text-align: center;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        }}
        .form-container {{
            padding: 50px;
            background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        }}
        .form-title {{
            text-align: center;
            color: #333;
            margin-bottom: 40px;
            font-size: 2.2em;
            font-weight: 300;
        }}
        .feature-highlight {{
            background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 40px;
            text-align: center;
        }}
        .feature-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        .feature-item {{
            text-align: center;
            padding: 25px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }}
        .feature-item:hover {{
            transform: translateY(-5px);
        }}
        .feature-icon {{
            font-size: 3em;
            margin-bottom: 15px;
        }}
        .form-group {{
            margin: 30px 0;
        }}
        label {{
            display: block;
            font-weight: 600;
            margin-bottom: 12px;
            color: #333;
            font-size: 1.2em;
        }}
        input, select, textarea {{
            width: 100%;
            padding: 18px;
            border: 2px solid #e9ecef;
            border-radius: 12px;
            font-size: 16px;
            transition: all 0.3s ease;
            box-sizing: border-box;
        }}
        input:focus, select:focus, textarea:focus {{
            border-color: #667eea;
            outline: none;
            box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
            transform: translateY(-2px);
        }}
        textarea {{
            min-height: 120px;
            resize: vertical;
        }}
        .btn {{
            background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
            color: white;
            padding: 20px 40px;
            border: none;
            border-radius: 12px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
            margin-top: 30px;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .btn:hover {{
            transform: translateY(-3px);
            box-shadow: 0 12px 30px rgba(231, 76, 60, 0.4);
        }}
        .btn:active {{
            transform: translateY(0);
        }}
        .github {{
            text-align: center;
            margin: 30px 50px;
            padding: 25px;
            background: linear-gradient(135deg, #24292e 0%, #586069 100%);
            border-radius: 15px;
            color: white;
        }}
        .github a {{
            color: #ffffff;
            text-decoration: none;
            font-weight: 600;
            font-size: 1.1em;
        }}
        .error-detail {{
            font-size: 14px;
            color: #666;
            margin-top: 12px;
            word-break: break-word;
        }}
        .word-count-info {{
            background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
            color: white;
            padding: 20px;
            border-radius: 12px;
            margin: 20px 0;
            text-align: center;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 AI Blog Generator Pro</h1>
            <p class="subtitle">Google Vertex AI Gemini 2.5 Pro による長文ブログ記事生成</p>
            <div class="badge">1,500～2,000文字対応</div>
        </div>
        
        <div class="status">
            <h3>🔮 AI エンジン状態</h3>
            <div class="status-grid">
                <div class="status-item">
                    <strong>Vertex AI Gemini 2.5 Pro</strong><br>
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
                    <strong>文字数</strong><br>
                    1,500-2,000文字
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
            <h2 class="form-title">長文ブログ記事を生成</h2>
            
            <div class="feature-highlight">
                <h3 style="margin: 0 0 15px 0;">✨ 高品質長文生成の特徴</h3>
                <p style="margin: 0;">最新のAI技術で、SEO効果の高い1,500-2,000文字の本格的なブログ記事を自動生成</p>
            </div>
            
            <div class="feature-grid">
                <div class="feature-item">
                    <div class="feature-icon">📝</div>
                    <strong>長文対応</strong><br>
                    1,500-2,000文字の<br>本格的な記事
                </div>
                <div class="feature-item">
                    <div class="feature-icon">🎯</div>
                    <strong>SEO最適化</strong><br>
                    検索エンジンに<br>最適化された構成
                </div>
                <div class="feature-item">
                    <div class="feature-icon">⚡</div>
                    <strong>高速生成</strong><br>
                    60秒以内で<br>高品質記事完成
                </div>
                <div class="feature-item">
                    <div class="feature-icon">🔄</div>
                    <strong>最新情報</strong><br>
                    2025年7月時点の<br>最新内容
                </div>
            </div>

            <div class="word-count-info">
                📊 生成される記事は1,500～2,000文字の本格的な長文コンテンツです
            </div>

            <form method="post" action="/generate">
                <div class="form-group">
                    <label for="topic">📝 ブログのトピック（詳細に記入してください）</label>
                    <textarea id="topic" name="topic" 
                              placeholder="例：初心者でも理解できるVertex AIの活用方法と実践事例。実際の導入プロセス、コスト感、期待できる効果について詳しく解説してほしい。" 
                              required></textarea>
                </div>
                
                <div class="form-group">
                    <label for="category">📂 カテゴリ</label>
                    <select id="category" name="category">
                        <option value="tech">🔧 技術・プログラミング</option>
                        <option value="business">💼 ビジネス・マーケティング</option>
                        <option value="lifestyle">🌱 ライフスタイル・自己啓発</option>
                        <option value="education">📚 教育・学習・スキルアップ</option>
                        <option value="travel">✈️ 旅行・観光・文化</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="tone">🎭 文体・トーン</label>
                    <select id="tone" name="tone">
                        <option value="professional">👔 プロフェッショナル（専門的・信頼性重視）</option>
                        <option value="friendly">😊 フレンドリー（親しみやすく共感重視）</option>
                        <option value="casual">😎 カジュアル（気軽で親近感のある）</option>
                    </select>
                </div>
                
                <button type="submit" class="btn">
                    🚀 Gemini 2.5 Pro で長文記事を生成
                </button>
            </form>
        </div>
    </div>
    
    <div style="text-align: center; margin: 40px 0; font-size: 14px; color: #ffffff;">
        <p>Powered by Google Cloud Vertex AI Gemini 2.5 Pro | Enhanced for Long-form Content</p>
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
    """ブログ生成エンドポイント（長文対応）"""
    logger.info(f"🤖 長文ブログ生成リクエスト受信: {topic[:50]}...")
    
    # AI生成実行
    result = blog_generator.generate_blog(topic, category, tone)
    
    # 結果に応じた表示設定
    if result["success"]:
        status_color = "#28a745"
        status_text = "🎉 長文生成成功"
        status_bg = "linear-gradient(135deg, #28a745 0%, #20c997 100%)"
        word_count_class = "success" if result["word_count"] >= 1500 else "warning"
    else:
        status_color = "#dc3545"
        status_text = "❌ 生成失敗"
        status_bg = "linear-gradient(135deg, #dc3545 0%, #c82333 100%)"
        word_count_class = "error"
    
    # 品質評価バッジ
    if result.get('word_count', 0) >= 1500:
        quality_badge = '<span class="quality-badge quality-excellent">優秀（1500文字以上）</span>'
    elif result.get('word_count', 0) >= 1000:
        quality_badge = '<span class="quality-badge quality-good">良好（1000文字以上）</span>'
    else:
        quality_badge = '<span class="quality-badge quality-needs-improvement">要改善（1000文字未満）</span>'
    
    return HTMLResponse(f"""
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>長文記事生成結果 - {topic[:30]}...</title>
    <style>
        body {{
            font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .container {{
            background: white;
            border-radius: 25px;
            overflow: hidden;
            box-shadow: 0 25px 50px rgba(0,0,0,0.15);
        }}
        .header {{
            text-align: center;
            background: {status_bg};
            color: white;
            padding: 50px 30px;
        }}
        .status {{
            color: white;
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 15px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        .topic {{
            font-size: 1.4em;
            opacity: 0.95;
            margin: 0;
            line-height: 1.4;
        }}
        .nav {{
            text-align: center;
            padding: 30px;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        }}
        .nav a {{
            color: white;
            text-decoration: none;
            padding: 15px 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 12px;
            font-weight: 600;
            margin: 0 15px;
            transition: all 0.3s ease;
            display: inline-block;
            font-size: 1.1em;
        }}
        .nav a:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
        }}
        .meta {{
            background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
            padding: 30px;
            border-left: 4px solid #2196f3;
        }}
        .meta h3 {{
            margin: 0 0 20px 0;
            color: #1565c0;
            font-size: 1.5em;
        }}
        .meta-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        .meta-item {{
            background: white;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        .word-count {{
            font-size: 2em;
            font-weight: bold;
            color: #e91e63;
        }}
        .word-count.success {{
            color: #4caf50;
        }}
        .word-count.warning {{
            color: #ff9800;
        }}
        .word-count.error {{
            color: #f44336;
        }}
        .content {{
            padding: 50px;
        }}
        .content h2 {{
            color: #333;
            margin-bottom: 30px;
            text-align: center;
            font-size: 2em;
        }}
        .blog-content {{
            background: linear-gradient(135deg, #fafafa 0%, #f5f5f5 100%);
            padding: 40px;
            border-radius: 20px;
            border: 1px solid #e0e0e0;
            line-height: 1.8;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);
        }}
        pre {{
            white-space: pre-wrap;
            font-family: 'Georgia', 'Times New Roman', serif;
            font-size: 17px;
            margin: 0;
            color: #333;
            line-height: 1.8;
        }}
        .error-content {{
            background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
            color: #c62828;
            border: 1px solid #ef5350;
        }}
        .quality-badge {{
            display: inline-block;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: bold;
            margin: 5px;
        }}
        .quality-excellent {{
            background: #4caf50;
            color: white;
        }}
        .quality-good {{
            background: #ff9800;
            color: white;
        }}
        .quality-needs-improvement {{
            background: #f44336;
            color: white;
        }}
        .stats {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 12px;
            margin: 20px 0;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="status">{status_text}</div>
            <h1>📄 長文ブログ記事生成結果</h1>
            <p class="topic">{topic}</p>
        </div>
        
        <div class="nav">
            <a href="/">🔄 新しい長文記事を生成</a>
            <a href="https://github.com/syokota-cyber/vertex-ai-blog-generator" target="_blank">📂 GitHub</a>
        </div>
        
        <div class="meta">
            <h3>📊 生成統計情報</h3>
            <div class="meta-grid">
                <div class="meta-item">
                    <strong>AI エンジン</strong><br>
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
                    <span class="word-count {word_count_class}">{result.get('word_count', 0)}</span><br>
                    <small>文字</small>
                </div>
            </div>
            
            <div class="stats">
                <strong>📈 品質評価:</strong>
                {quality_badge}
            </div>
        </div>
        
        <div class="content">
            <h2>📝 生成されたブログ記事</h2>
            <div class="blog-content {'error-content' if not result['success'] else ''}">
                <pre>{result['content']}</pre>
            </div>
        </div>
        
        <div class="nav">
            <a href="/">🆕 別の長文記事を生成する</a>
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
        "version": "2.0.0",
        "features": ["long_form_content", "seo_optimized", "latest_2025_info"],
        "word_count_target": "1500-2000",
        "error": blog_generator.error_message if not blog_generator.available else None
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)