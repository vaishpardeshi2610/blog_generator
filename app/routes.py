from flask import request, jsonify
from template.chat import chatinterface
from .blog_generator import BlogGenerator

# Initialize blog generator
blog_generator = BlogGenerator()

def init_routes(app):
    @app.route('/generate-blog', methods=['POST'])
    def generate_blog():
        try:
            data = request.get_json()
            topic = data.get('topic')
            
            if not topic:
                return jsonify({"error": "Topic is required"}), 400
                
            if len(topic) > 200:
                return jsonify({"error": "Topic is too long. Please keep it under 200 characters"}), 400
            
            result = blog_generator.generate_blog(topic)
            return jsonify(result), 200
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/chat', methods=['GET'])
    def chat_interface():
        return chatinterface()