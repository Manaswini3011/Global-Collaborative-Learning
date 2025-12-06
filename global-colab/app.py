from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
import pymysql
import hashlib
import json
from datetime import datetime
import os
from functools import wraps
import re
import sys

# Translation API
try:
    from googletrans import Translator
    TRANSLATOR_AVAILABLE = True
    translator = Translator()
except ImportError:
    TRANSLATOR_AVAILABLE = False
    translator = None
    # Only print warning if in debug mode to avoid cluttering production logs
    import sys
    if '--debug' in sys.argv or os.getenv('FLASK_ENV') == 'development':
        print("Warning: googletrans not installed. Translation will use placeholder.")

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'
CORS(app)

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'global_colab',
    'charset': 'utf8mb4'
}

def get_db_connection():
    """Create database connection"""
    return pymysql.connect(**DB_CONFIG)

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def login_required(f):
    """Decorator for routes that require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

def translate_text(text, from_lang, to_lang):
    """
    Translate text from one language to another using Google Translate API.
    Falls back to placeholder if API is not available.
    
    Args:
        text: Text to translate
        from_lang: Source language code (e.g., 'en', 'es', 'fr')
        to_lang: Target language code (e.g., 'en', 'es', 'fr')
    
    Returns:
        Translated text or original text with indicator if translation fails
    """
    # Validate input
    if not text or not isinstance(text, str):
        return text or ""
    
    # If same language, return original
    if from_lang == to_lang or not from_lang or not to_lang:
        return text
    
    # Use Google Translate API if available
    if TRANSLATOR_AVAILABLE and translator:
        try:
            # Map language codes to googletrans format
            lang_map = {
                'en': 'en', 'es': 'es', 'fr': 'fr', 'pt': 'pt', 
                'ja': 'ja', 'zh': 'zh-cn', 'zh-cn': 'zh-cn', 'zh-tw': 'zh-tw',
                'de': 'de', 'hi': 'hi', 'ar': 'ar', 'ru': 'ru',
                'it': 'it', 'ko': 'ko', 'nl': 'nl', 'pl': 'pl',
                'tr': 'tr', 'vi': 'vi', 'th': 'th', 'id': 'id'
            }
            
            src_lang = lang_map.get(from_lang.lower(), 'auto')
            dest_lang = lang_map.get(to_lang.lower(), 'en')
            
            # Handle empty or very short text
            if len(text.strip()) == 0:
                return text
            
            # Translate the text with retry logic
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    result = translator.translate(text, src=src_lang, dest=dest_lang)
                    if result and result.text:
                        return result.text
                except Exception as retry_error:
                    if attempt == max_retries - 1:
                        raise retry_error
                    # Wait a bit before retry (simple delay)
                    import time
                    time.sleep(0.5)
            
            # If we get here, translation didn't return text
            return text
            
        except Exception as e:
            # Log error for debugging
            error_msg = str(e)
            if '--debug' in sys.argv or os.getenv('FLASK_ENV') == 'development':
                print(f"Translation error ({from_lang} -> {to_lang}): {error_msg}")
            
            # For certain errors, try without specifying source language
            if 'could not be detected' in error_msg.lower() or 'invalid' in error_msg.lower():
                try:
                    result = translator.translate(text, dest=dest_lang)
                    if result and result.text:
                        return result.text
                except:
                    pass
            
            # Fallback to placeholder on error
            return f"🌐 [{to_lang.upper()}] {text}"
    
    # Fallback: Simple demo translations for common phrases
    text_lower = text.lower().strip()
    
    # Common greeting translations
    greetings = {
        'hello': {'es': 'hola', 'fr': 'bonjour', 'pt': 'olá', 'ja': 'こんにちは', 
                  'zh': '你好', 'de': 'hallo', 'hi': 'नमस्ते', 'ar': 'مرحبا', 
                  'ru': 'привет', 'it': 'ciao', 'ko': '안녕하세요'},
        'hi': {'es': 'hola', 'fr': 'salut', 'pt': 'oi', 'ja': 'こんにちは', 
               'zh': '你好', 'de': 'hallo', 'hi': 'नमस्ते', 'ar': 'مرحبا', 
               'ru': 'привет', 'it': 'ciao', 'ko': '안녕하세요'},
        'thanks': {'es': 'gracias', 'fr': 'merci', 'pt': 'obrigado', 'ja': 'ありがとう', 
                   'zh': '谢谢', 'de': 'danke', 'hi': 'धन्यवाद', 'ar': 'شكرا', 
                   'ru': 'спасибо', 'it': 'grazie', 'ko': '감사합니다'},
        'thank you': {'es': 'gracias', 'fr': 'merci', 'pt': 'obrigado', 'ja': 'ありがとう', 
                      'zh': '谢谢', 'de': 'danke', 'hi': 'धन्यवाद', 'ar': 'شكرا', 
                      'ru': 'спасибо', 'it': 'grazie', 'ko': '감사합니다'},
    }
    
    # Check for common phrases
    if text_lower in greetings:
        if to_lang.lower() in greetings[text_lower]:
            return greetings[text_lower][to_lang.lower()]
    
    # Fallback: return text with translation indicator
    return f"🌐 [{to_lang.upper()}] {text}"

def get_user_language(user_id):
    """Get user's preferred language"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT language FROM users WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result[0] if result else 'en'
    except:
        return 'en'

# ==================== AUTHENTICATION ROUTES ====================

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/api/register', methods=['POST'])
def register():
    """User registration"""
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute("SELECT user_id FROM users WHERE email = %s OR username = %s", 
                      (data['email'], data['username']))
        if cursor.fetchone():
            return jsonify({'error': 'User already exists'}), 400
        
        # Insert new user
        password_hash = hash_password(data['password'])
        cursor.execute("""
            INSERT INTO users (username, email, password_hash, full_name, country, language, culture, skills, interests)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (data['username'], data['email'], password_hash, data['full_name'], 
              data.get('country', ''), data.get('language', 'en'), 
              data.get('culture', ''), data.get('skills', ''), data.get('interests', '')))
        
        conn.commit()
        user_id = cursor.lastrowid
        cursor.close()
        conn.close()
        
        session['user_id'] = user_id
        session['username'] = data['username']
        
        return jsonify({'message': 'Registration successful', 'user_id': user_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    """User login"""
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        
        password_hash = hash_password(data['password'])
        cursor.execute("""
            SELECT user_id, username, full_name, email, country, language, points, level
            FROM users WHERE (email = %s OR username = %s) AND password_hash = %s
        """, (data['email'], data['email'], password_hash))
        
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            return jsonify({
                'message': 'Login successful',
                'user': {
                    'user_id': user[0],
                    'username': user[1],
                    'full_name': user[2],
                    'email': user[3],
                    'country': user[4],
                    'language': user[5],
                    'points': user[6],
                    'level': user[7]
                }
            }), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/logout', methods=['POST'])
def logout():
    """User logout"""
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200

# ==================== DASHBOARD ROUTES ====================

@app.route('/dashboard')
def dashboard():
    """Dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/user/profile', methods=['GET'])
@login_required
def get_user_profile():
    """Get user profile"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("""
            SELECT user_id, username, email, full_name, country, language, culture, 
                   skills, interests, points, level, created_at
            FROM users WHERE user_id = %s
        """, (session['user_id'],))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return jsonify(user), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== TEAM ROUTES ====================

@app.route('/api/teams', methods=['GET'])
@login_required
def get_teams():
    """Get all teams for current user"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("""
            SELECT t.*, COUNT(tm.user_id) as member_count
            FROM teams t
            LEFT JOIN team_members tm ON t.team_id = tm.team_id
            WHERE t.team_id IN (
                SELECT team_id FROM team_members WHERE user_id = %s
            )
            GROUP BY t.team_id
        """, (session['user_id'],))
        teams = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(teams), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/teams', methods=['POST'])
@login_required
def create_team():
    """Create a new team"""
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO teams (team_name, description, created_by)
            VALUES (%s, %s, %s)
        """, (data['team_name'], data.get('description', ''), session['user_id']))
        
        team_id = cursor.lastrowid
        
        # Add creator as team member
        cursor.execute("""
            INSERT INTO team_members (team_id, user_id, role)
            VALUES (%s, %s, 'leader')
        """, (team_id, session['user_id']))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Team created successfully', 'team_id': team_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/teams/<int:team_id>/members', methods=['GET'])
@login_required
def get_team_members(team_id):
    """Get team members"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("""
            SELECT u.user_id, u.username, u.full_name, u.country, u.language, 
                   tm.role, tm.joined_at
            FROM team_members tm
            JOIN users u ON tm.user_id = u.user_id
            WHERE tm.team_id = %s
        """, (team_id,))
        members = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(members), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== PROJECT ROUTES ====================

@app.route('/api/projects', methods=['GET'])
@login_required
def get_projects():
    """Get projects for current user"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("""
            SELECT p.*, t.team_name
            FROM projects p
            LEFT JOIN teams t ON p.team_id = t.team_id
            WHERE p.team_id IN (
                SELECT team_id FROM team_members WHERE user_id = %s
            )
        """, (session['user_id'],))
        projects = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(projects), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/projects', methods=['POST'])
@login_required
def create_project():
    """Create a new project"""
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        
        team_id = data.get('team_id')
        if team_id:
            # Check if user is a team member
            cursor.execute("SELECT team_member_id FROM team_members WHERE team_id = %s AND user_id = %s", 
                          (team_id, session['user_id']))
            if not cursor.fetchone():
                cursor.close()
                conn.close()
                return jsonify({'error': 'Only team members can create projects for this team'}), 403
        
        cursor.execute("""
            INSERT INTO projects (project_name, description, team_id, skills_required, difficulty_level)
            VALUES (%s, %s, %s, %s, %s)
        """, (data['project_name'], data.get('description', ''), team_id,
              data.get('skills_required', ''), data.get('difficulty_level', 'medium')))
        
        project_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Project created successfully', 'project_id': project_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== AI RECOMMENDATIONS ====================

@app.route('/api/recommendations', methods=['GET'])
@login_required
def get_recommendations():
    """
    Get AI-powered project recommendations
    
    TODO: Integrate with external AI API for dynamic recommendations:
    - OpenAI API (GPT models) for generating personalized project ideas
    - Hugging Face API for ML-based recommendations
    - Custom recommendation service
    
    Example with OpenAI:
    ```python
    import openai
    openai.api_key = os.getenv('OPENAI_API_KEY')
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": f"Generate project recommendations for user with skills: {user['skills']}, interests: {user['interests']}"}]
    )
    ```
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        # Get user skills and interests
        cursor.execute("SELECT skills, interests FROM users WHERE user_id = %s", (session['user_id'],))
        user = cursor.fetchone()
        
        # TODO: Replace with actual AI API call for dynamic recommendations
        # For now, using curated recommendations based on user profile
        recommendations = [
            {
                'recommendation_id': 1,
                'title': 'Global Climate Change Awareness App',
                'description': 'Build a collaborative app that tracks climate data from different countries',
                'skills_match': 'Web Development, Data Science',
                'difficulty_level': 'medium',
                'estimated_duration': '4-6 weeks'
            },
            {
                'recommendation_id': 2,
                'title': 'Multilingual Learning Platform',
                'description': 'Create a platform for language exchange and cultural learning',
                'skills_match': 'UI/UX, Communication',
                'difficulty_level': 'easy',
                'estimated_duration': '2-3 weeks'
            },
            {
                'recommendation_id': 3,
                'title': 'AI-Powered Cultural Bridge',
                'description': 'Develop an AI system that helps bridge cultural communication gaps',
                'skills_match': 'AI, Machine Learning, Communication',
                'difficulty_level': 'hard',
                'estimated_duration': '8-10 weeks'
            }
        ]
        
        cursor.close()
        conn.close()
        return jsonify(recommendations), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== DISCUSSION ROOMS ====================

@app.route('/api/rooms', methods=['GET'])
@login_required
def get_rooms():
    """Get discussion rooms for user's teams"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("""
            SELECT dr.*, t.team_name, p.project_name
            FROM discussion_rooms dr
            LEFT JOIN teams t ON dr.team_id = t.team_id
            LEFT JOIN projects p ON dr.project_id = p.project_id
            WHERE dr.team_id IN (
                SELECT team_id FROM team_members WHERE user_id = %s
            )
        """, (session['user_id'],))
        rooms = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(rooms), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/rooms', methods=['POST'])
@login_required
def create_room():
    """Create a discussion room"""
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        
        team_id = data.get('team_id')
        if team_id:
            # Check if user is a team member
            cursor.execute("SELECT team_member_id FROM team_members WHERE team_id = %s AND user_id = %s", 
                          (team_id, session['user_id']))
            if not cursor.fetchone():
                cursor.close()
                conn.close()
                return jsonify({'error': 'Only team members can create rooms for this team'}), 403
        
        cursor.execute("""
            INSERT INTO discussion_rooms (room_name, team_id, project_id, created_by)
            VALUES (%s, %s, %s, %s)
        """, (data['room_name'], team_id, data.get('project_id'), session['user_id']))
        
        room_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Room created successfully', 'room_id': room_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/rooms/<int:room_id>/messages', methods=['GET'])
@login_required
def get_messages(room_id):
    """Get messages from a discussion room, translated to current user's language"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if user is a member of the team that owns this room
        cursor.execute("SELECT team_id FROM discussion_rooms WHERE room_id = %s", (room_id,))
        room = cursor.fetchone()
        if not room or not room[0]:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Room not found'}), 404
        
        team_id = room[0]
        
        # Check if user is a team member
        cursor.execute("SELECT team_member_id FROM team_members WHERE team_id = %s AND user_id = %s", 
                      (team_id, session['user_id']))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({'error': 'Only team members can view messages'}), 403
        
        # Get current user's language
        current_user_lang = get_user_language(session['user_id'])
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("""
            SELECT m.*, u.username, u.full_name, u.country, u.language as sender_language
            FROM messages m
            JOIN users u ON m.user_id = u.user_id
            WHERE m.room_id = %s
            ORDER BY m.created_at ASC
        """, (room_id,))
        messages = cursor.fetchall()
        
        # Translate messages to current user's language
        for message in messages:
            original_text = message.get('message_text') or ''
            sender_lang = message.get('sender_language') or message.get('original_language') or 'en'
            
            # Normalize language codes
            if sender_lang:
                sender_lang = sender_lang.lower()
            if current_user_lang:
                current_user_lang = current_user_lang.lower()
            
            # If message is in different language, translate it
            if sender_lang != current_user_lang and original_text:
                try:
                    translated_text = translate_text(original_text, sender_lang, current_user_lang)
                    message['translated_text'] = translated_text
                    message['display_text'] = translated_text  # Text to display to user
                except Exception as e:
                    # If translation fails, use original text
                    message['translated_text'] = None
                    message['display_text'] = original_text
                    if '--debug' in sys.argv or os.getenv('FLASK_ENV') == 'development':
                        print(f"Translation failed for message: {str(e)}")
            else:
                message['translated_text'] = None
                message['display_text'] = original_text
            
            message['original_text'] = original_text  # Keep original for reference
            message['is_translated'] = sender_lang != current_user_lang and original_text
            message['original_language'] = sender_lang
            message['display_language'] = current_user_lang
        
        cursor.close()
        conn.close()
        return jsonify(messages), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/rooms/<int:room_id>/messages', methods=['POST'])
@login_required
def send_message(room_id):
    """Send a message in discussion room with translation"""
    try:
        # Check if user is a member of the team that owns this room
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get room's team_id
        cursor.execute("SELECT team_id FROM discussion_rooms WHERE room_id = %s", (room_id,))
        room = cursor.fetchone()
        if not room or not room[0]:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Room not found or not associated with a team'}), 404
        
        team_id = room[0]
        
        # Check if user is a team member
        cursor.execute("SELECT team_member_id FROM team_members WHERE team_id = %s AND user_id = %s", 
                      (team_id, session['user_id']))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({'error': 'Only team members can send messages'}), 403
        
        data = request.json
        if not data or 'message_text' not in data:
            cursor.close()
            conn.close()
            return jsonify({'error': 'message_text is required'}), 400
        
        message_text = data['message_text'].strip()
        if not message_text:
            cursor.close()
            conn.close()
            return jsonify({'error': 'message_text cannot be empty'}), 400
        
        # Get sender's language
        cursor.execute("SELECT language FROM users WHERE user_id = %s", (session['user_id'],))
        result = cursor.fetchone()
        sender_lang = (result[0] if result and result[0] else 'en') or 'en'
        
        # Store original message with sender's language
        # Translation will happen when messages are retrieved based on each user's language
        cursor.execute("""
            INSERT INTO messages (room_id, user_id, message_text, translated_text, original_language, translated_language)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (room_id, session['user_id'], message_text, None, sender_lang, None))
        
        message_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Message sent successfully', 'message_id': message_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== TRANSLATION API ====================

@app.route('/api/translate', methods=['POST'])
@login_required
def translate_api():
    """
    Translate text from one language to another.
    Supports both automatic language detection and manual language specification.
    
    Request body:
    {
        "text": "Text to translate",
        "from_lang": "en" (optional, defaults to 'auto'),
        "to_lang": "es" (required)
    }
    
    Response:
    {
        "translated_text": "Translated text",
        "original_text": "Original text",
        "from_lang": "en",
        "to_lang": "es",
        "success": true
    }
    """
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        text = data.get('text', '').strip()
        if not text:
            return jsonify({'error': 'Text to translate is required'}), 400
        
        from_lang = data.get('from_lang', 'auto')
        to_lang = data.get('to_lang', 'en')
        
        if not to_lang:
            return jsonify({'error': 'Target language (to_lang) is required'}), 400
        
        # Translate the text
        translated_text = translate_text(text, from_lang, to_lang)
        
        # Detect actual source language if auto was used
        detected_lang = from_lang
        if from_lang == 'auto' and TRANSLATOR_AVAILABLE and translator:
            try:
                result = translator.detect(text)
                if result and result.lang:
                    detected_lang = result.lang
            except:
                pass
        
        return jsonify({
            'translated_text': translated_text,
            'original_text': text,
            'from_lang': detected_lang,
            'to_lang': to_lang,
            'success': True
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@app.route('/api/translate/batch', methods=['POST'])
@login_required
def translate_batch_api():
    """
    Translate multiple texts at once.
    
    Request body:
    {
        "texts": ["Text 1", "Text 2", "Text 3"],
        "from_lang": "en" (optional),
        "to_lang": "es" (required)
    }
    
    Response:
    {
        "translations": [
            {"original": "Text 1", "translated": "Translated 1"},
            {"original": "Text 2", "translated": "Translated 2"}
        ],
        "success": true
    }
    """
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        texts = data.get('texts', [])
        if not texts or not isinstance(texts, list):
            return jsonify({'error': 'Texts array is required'}), 400
        
        from_lang = data.get('from_lang', 'auto')
        to_lang = data.get('to_lang', 'en')
        
        if not to_lang:
            return jsonify({'error': 'Target language (to_lang) is required'}), 400
        
        translations = []
        for text in texts:
            if text:
                translated = translate_text(str(text), from_lang, to_lang)
                translations.append({
                    'original': text,
                    'translated': translated
                })
        
        return jsonify({
            'translations': translations,
            'success': True
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@app.route('/api/translate/languages', methods=['GET'])
def get_supported_languages():
    """
    Get list of supported languages for translation.
    
    Response:
    {
        "languages": [
            {"code": "en", "name": "English"},
            {"code": "es", "name": "Spanish"}
        ]
    }
    """
    languages = [
        {'code': 'en', 'name': 'English'},
        {'code': 'es', 'name': 'Spanish'},
        {'code': 'fr', 'name': 'French'},
        {'code': 'pt', 'name': 'Portuguese'},
        {'code': 'de', 'name': 'German'},
        {'code': 'it', 'name': 'Italian'},
        {'code': 'ja', 'name': 'Japanese'},
        {'code': 'zh', 'name': 'Chinese (Simplified)'},
        {'code': 'zh-cn', 'name': 'Chinese (Simplified)'},
        {'code': 'zh-tw', 'name': 'Chinese (Traditional)'},
        {'code': 'ko', 'name': 'Korean'},
        {'code': 'hi', 'name': 'Hindi'},
        {'code': 'ar', 'name': 'Arabic'},
        {'code': 'ru', 'name': 'Russian'},
        {'code': 'nl', 'name': 'Dutch'},
        {'code': 'pl', 'name': 'Polish'},
        {'code': 'tr', 'name': 'Turkish'},
        {'code': 'vi', 'name': 'Vietnamese'},
        {'code': 'th', 'name': 'Thai'},
        {'code': 'id', 'name': 'Indonesian'},
    ]
    
    return jsonify({'languages': languages}), 200

# ==================== PROGRESS TRACKING ====================

@app.route('/api/progress', methods=['GET'])
@login_required
def get_progress():
    """Get user progress"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("""
            SELECT pr.*, p.project_name, t.team_name
            FROM progress pr
            LEFT JOIN projects p ON pr.project_id = p.project_id
            LEFT JOIN teams t ON pr.team_id = t.team_id
            WHERE pr.user_id = %s
        """, (session['user_id'],))
        progress = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(progress), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== PEER FEEDBACK ====================

@app.route('/api/feedback', methods=['POST'])
@login_required
def submit_feedback():
    """Submit peer feedback"""
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO peer_feedback (project_id, team_id, from_user_id, to_user_id, rating, feedback_text)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (data.get('project_id'), data.get('team_id'), session['user_id'], 
              data['to_user_id'], data['rating'], data.get('feedback_text', '')))
        
        feedback_id = cursor.lastrowid
        
        # Award points to the user receiving feedback
        cursor.execute("UPDATE users SET points = points + %s WHERE user_id = %s", 
                      (data['rating'] * 10, data['to_user_id']))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Feedback submitted successfully', 'feedback_id': feedback_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== RESOURCES ====================

@app.route('/api/resources', methods=['GET'])
@login_required
def get_resources():
    """Get resources for user's teams/projects"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("""
            SELECT r.*, u.username as uploaded_by_name
            FROM resources r
            JOIN users u ON r.uploaded_by = u.user_id
            WHERE r.team_id IN (
                SELECT team_id FROM team_members WHERE user_id = %s
            ) OR r.project_id IN (
                SELECT project_id FROM projects WHERE team_id IN (
                    SELECT team_id FROM team_members WHERE user_id = %s
                )
            )
        """, (session['user_id'], session['user_id']))
        resources = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(resources), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/resources', methods=['POST'])
@login_required
def upload_resource():
    """Upload a resource"""
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO resources (resource_name, resource_type, resource_url, project_id, team_id, uploaded_by, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (data['resource_name'], data.get('resource_type', 'file'), 
              data.get('resource_url', ''), data.get('project_id'), 
              data.get('team_id'), session['user_id'], data.get('description', '')))
        
        resource_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Resource uploaded successfully', 'resource_id': resource_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== ACHIEVEMENTS ====================

@app.route('/api/achievements', methods=['GET'])
@login_required
def get_achievements():
    """Get user achievements"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("""
            SELECT * FROM achievements WHERE user_id = %s ORDER BY earned_at DESC
        """, (session['user_id'],))
        achievements = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(achievements), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== USER DISCOVERY ====================

@app.route('/api/users/discover', methods=['GET'])
@login_required
def discover_users():
    """Discover users with AI-guided skill matching"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        # Get current user's skills and interests
        cursor.execute("SELECT skills, interests FROM users WHERE user_id = %s", (session['user_id'],))
        current_user = cursor.fetchone()
        
        current_skills = set()
        current_interests = set()
        if current_user and current_user['skills']:
            current_skills = set(s.strip().lower() for s in current_user['skills'].split(','))
        if current_user and current_user['interests']:
            current_interests = set(s.strip().lower() for s in current_user['interests'].split(','))
        
        # Get all other users
        cursor.execute("""
            SELECT user_id, username, full_name, country, language, culture, skills, interests, points, level
            FROM users WHERE user_id != %s
        """, (session['user_id'],))
        all_users = cursor.fetchall()
        
        # AI-guided matching: calculate compatibility score
        matched_users = []
        for user in all_users:
            user_skills = set()
            user_interests = set()
            if user['skills']:
                user_skills = set(s.strip().lower() for s in user['skills'].split(','))
            if user['interests']:
                user_interests = set(s.strip().lower() for s in user['interests'].split(','))
            
            # Calculate compatibility score
            skill_match = len(current_skills.intersection(user_skills))
            interest_match = len(current_interests.intersection(user_interests))
            total_score = (skill_match * 2) + interest_match  # Skills weighted more
            
            # Check if user is already in a team with current user
            cursor.execute("""
                SELECT COUNT(*) as count FROM team_members tm1
                JOIN team_members tm2 ON tm1.team_id = tm2.team_id
                WHERE tm1.user_id = %s AND tm2.user_id = %s
            """, (session['user_id'], user['user_id']))
            already_teamed = cursor.fetchone()['count'] > 0
            
            matched_users.append({
                **user,
                'compatibility_score': total_score,
                'skill_matches': list(current_skills.intersection(user_skills)),
                'interest_matches': list(current_interests.intersection(user_interests)),
                'already_teamed': already_teamed
            })
        
        # Sort by compatibility score
        matched_users.sort(key=lambda x: x['compatibility_score'], reverse=True)
        
        cursor.close()
        conn.close()
        return jsonify(matched_users), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== TEAM INVITATIONS ====================

@app.route('/api/invitations', methods=['GET'])
@login_required
def get_invitations():
    """Get invitations (sent and received)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        # Get received invitations
        cursor.execute("""
            SELECT ti.*, t.team_name, u1.full_name as from_user_name, u1.username as from_username,
                   u2.full_name as to_user_name, u2.username as to_username
            FROM team_invitations ti
            JOIN teams t ON ti.team_id = t.team_id
            JOIN users u1 ON ti.from_user_id = u1.user_id
            JOIN users u2 ON ti.to_user_id = u2.user_id
            WHERE ti.to_user_id = %s AND ti.status = 'pending'
        """, (session['user_id'],))
        received = cursor.fetchall()
        
        # Get sent invitations
        cursor.execute("""
            SELECT ti.*, t.team_name, u1.full_name as from_user_name, u1.username as from_username,
                   u2.full_name as to_user_name, u2.username as to_username
            FROM team_invitations ti
            JOIN teams t ON ti.team_id = t.team_id
            JOIN users u1 ON ti.from_user_id = u1.user_id
            JOIN users u2 ON ti.to_user_id = u2.user_id
            WHERE ti.from_user_id = %s
        """, (session['user_id'],))
        sent = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return jsonify({'received': received, 'sent': sent}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/invitations', methods=['POST'])
@login_required
def send_invitation():
    """Send team invitation"""
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        
        team_id = data['team_id']
        to_user_id = data['to_user_id']
        
        # Check if user is a member of the team
        cursor.execute("SELECT team_member_id FROM team_members WHERE team_id = %s AND user_id = %s", 
                      (team_id, session['user_id']))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({'error': 'You must be a team member to send invitations'}), 403
        
        # Check if user is already in the team
        cursor.execute("SELECT team_member_id FROM team_members WHERE team_id = %s AND user_id = %s", 
                      (team_id, to_user_id))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({'error': 'User is already a team member'}), 400
        
        # Check if there's already a pending invitation
        cursor.execute("""
            SELECT invitation_id FROM team_invitations 
            WHERE team_id = %s AND to_user_id = %s AND status = 'pending'
        """, (team_id, to_user_id))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({'error': 'Invitation already sent'}), 400
        
        # Create invitation
        cursor.execute("""
            INSERT INTO team_invitations (team_id, from_user_id, to_user_id, message)
            VALUES (%s, %s, %s, %s)
        """, (team_id, session['user_id'], to_user_id, data.get('message', '')))
        
        invitation_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Invitation sent successfully', 'invitation_id': invitation_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/invitations/<int:invitation_id>/accept', methods=['POST'])
@login_required
def accept_invitation(invitation_id):
    """Accept team invitation"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get invitation
        cursor.execute("""
            SELECT team_id FROM team_invitations WHERE invitation_id = %s AND to_user_id = %s AND status = 'pending'
        """, (invitation_id, session['user_id']))
        invitation = cursor.fetchone()
        
        if not invitation:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Invitation not found or already processed'}), 404
        
        team_id = invitation[0]  # team_id is at index 0
        
        # Update invitation status
        cursor.execute("""
            UPDATE team_invitations SET status = 'accepted', responded_at = NOW()
            WHERE invitation_id = %s
        """, (invitation_id,))
        
        # Add user to team
        cursor.execute("""
            INSERT INTO team_members (team_id, user_id, role)
            VALUES (%s, %s, 'member')
        """, (team_id, session['user_id']))
        
        # Award points for joining team
        cursor.execute("UPDATE users SET points = points + 50 WHERE user_id = %s", (session['user_id'],))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Invitation accepted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/invitations/<int:invitation_id>/reject', methods=['POST'])
@login_required
def reject_invitation(invitation_id):
    """Reject team invitation"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Update invitation status
        cursor.execute("""
            UPDATE team_invitations SET status = 'rejected', responded_at = NOW()
            WHERE invitation_id = %s AND to_user_id = %s AND status = 'pending'
        """, (invitation_id, session['user_id']))
        
        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Invitation not found or already processed'}), 404
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Invitation rejected'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

