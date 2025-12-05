from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file,  session, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models import db
#from OpenAI import OpenAI
from openai import OpenAI
from moviepy.editor import VideoFileClip
import tempfile, json, os, re
from flask import render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from datetime import datetime
import logging
import os
import requests
from datetime import datetime
import datetime
from sqlalchemy import func
from models import db, User
#from googletrans import Translator
import pytz
from flask_socketio import SocketIO, emit
#from googletrans import Translator
import speech_recognition as sr
from flask import request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
#from googletrans import Translator
from datetime import datetime
from models import db, Translation, LiveTranslation, zimbabwe_now
import base64
import numpy as np
from pydub import AudioSegment
import speech_recognition as sr
import io
import uuid
import soundfile as sf
import tempfile
import cv2



trans_bp = Blueprint('trans', __name__, url_prefix='/trans')

#translator = Translator()

from models import  MediaFile
# Upload settings
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")

# Ensure folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {"mp4", "mp3", "wav"}

#translator = Translator()


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def zimbabwe_now():
    harare_tz = pytz.timezone("Africa/Harare")
    return datetime.now(harare_tz)


@trans_bp.route('/home', methods=['GET', 'POST'])
@login_required
def home():

    return render_template(
        "trans/home.html",
        user=current_user,
    )


# @trans_bp.route('/video-translation', methods=['GET', 'POST'])
# @login_required
# def video_translation():

#     return render_template(
#         "trans/translation.html",
#         user=current_user,
#     )

#translator = Translator()


@trans_bp.route('/video-translation')
@login_required
def video_translation():
    return render_template('trans/translation.html', user=current_user)
from deep_translator import GoogleTranslator


client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


@trans_bp.route("/api/live-translate", methods=["POST"])
@login_required
def live_translate():
    try:
        data = request.get_json()
        text = data.get("text", "").strip()
        lang = data.get("language", "shona").lower()

        if not text:
            return jsonify({"translation": "", "status": "empty input"})

        start_time = zimbabwe_now()

        # ------------------ Step 1: Translate using OpenAI ------------------
        result = None
        try:
            prompt = (
                f"Translate the following English text to {lang.capitalize()}.\n\n"
                f"English: \"{text}\"\n"
                f"Return only the translated text."
            )
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            result = response.choices[0].message.content.strip()
        except Exception as e:
            print(f"OpenAI API failed: {e}")

        # ------------------ Step 2: Fallback to deep-translator ------------------
        if not result:
            from deep_translator import GoogleTranslator
            if lang == "shona":
                result = GoogleTranslator(source='en', target='sn').translate(text)
            elif lang == "ndebele":
                result = GoogleTranslator(source='en', target='nd').translate(text)
            else:
                result = text  # fallback if unknown language

        # ------------------ Step 3: Save to LiveTranslation only ------------------
        try:
            live = LiveTranslation(
                translation_id=None,  # Not storing in main Translation table
                selected_language=lang,
                original_text=text,
                translated_text=result,
                start_time=start_time,
                end_time=zimbabwe_now()
            )
            db.session.add(live)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Could not save to live translations: {e}")
            return jsonify({"translation": result, "status": "failed to save live translation"})

        # ------------------ Step 4: Return result ------------------
        return jsonify({
            "translation": result,
            "status": "success",
            "time_taken_seconds": (zimbabwe_now() - start_time).total_seconds()
        })

    except Exception as e:
        print(f"Server error: {e}")
        return jsonify({"translation": "", "status": "server error"})

@trans_bp.route("/api/debug-db")
@login_required
def debug_database():
    
    translations = Translation.query.all()
    
    result = []
    for trans in translations:
        result.append({
            'id': trans.id,
            'english': trans.english_sentence,
            'shona': trans.shona_translation,
            'ndebele': trans.ndebele_translation
        })
    
    print(" DATABASE CONTENT")
    for item in result:
        print(f"English: '{item['english']}' -> Shona: '{item['shona']}'")
    
    return jsonify({
        'count': len(result),
        'translations': result
    })


@trans_bp.route('/language', methods=['GET', 'POST'])
@login_required
def language():

    return render_template(
        "trans/language.html",
        user=current_user,
    )


# @trans_bp.route('/recorded-translation', methods=['GET', 'POST'])
# @login_required
# def recorded_translation():


#     return render_template("trans/recorded.html")


from openai import OpenAI
from moviepy.editor import VideoFileClip
import tempfile, json, os, re
from flask import render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from datetime import datetime
import logging

# Configure logging
logger = logging.getLogger(__name__)

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"mp3", "wav", "mp4"}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB limit

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_size(file):
    """Get file size safely"""
    current_pos = file.tell()
    file.seek(0, 2)  # Seek to end
    size = file.tell()
    file.seek(current_pos)  # Reset to original position
    return size

def extract_audio_moviepy(video_path):
    """Lightweight audio extraction using MoviePy with optimized settings"""
    try:
        # Load only audio to save memory
        clip = VideoFileClip(video_path)
        audio_path = tempfile.mktemp(suffix=".wav")
        
        # Optimize audio settings for faster processing
        clip.audio.write_audiofile(
            audio_path, 
            codec='pcm_s16le',
            fps=16000,  # Lower sample rate for faster processing
            verbose=False,
            logger=None
        )
        clip.close()
        return audio_path
    except Exception as e:
        logger.error(f"MoviePy audio extraction error: {e}")
        return None

def transcribe_audio_optimized(audio_path):
    """Optimized transcription with error handling"""
    try:
        with open(audio_path, "rb") as f:
            transcript = client.audio.transcriptions.create(
                file=f, 
                model="whisper-1",
                response_format="text"
            )
        return transcript.strip()
    except Exception as e:
        logger.error(f"Transcription error: {e}")
        return None

def translate_text_optimized(text, target_language):
    """Optimized translation with faster response"""
    language_map = {
        "shona": "Shona",
        "ndebele": "Ndebele"
    }
    
    lang_name = language_map.get(target_language, target_language)
    
    # Simplified prompt for faster processing
    prompt = f"""Translate this to {lang_name} only: {text}"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # Keeping your original model
            messages=[
                {
                    "role": "system", 
                    "content": "You are a translator. Return only the translation without any explanations or JSON."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            max_tokens=300,
            temperature=0.1  # Lower temperature for consistent results
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Translation error: {e}")
        return text  # Fallback to original text

@trans_bp.route("/recorded-translation", methods=["GET", "POST"])
@login_required
def recorded_translation():
    uploaded_file = None
    extracted_text = None
    translated_text = None
    selected_language = None
    processing_time = None

    if request.method == "POST":
        file = request.files.get("file")
        target_language = request.form.get("language", "shona")
        selected_language = target_language

        if not file or file.filename.strip() == "":
            flash("Please select a file to upload.", "danger")
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash("Only audio or video files (.mp4, .mp3, .wav) are allowed.", "danger")
            return redirect(request.url)

        # Check file size
        file_size = get_file_size(file)
        if file_size > MAX_FILE_SIZE:
            flash("File size too large (max 50MB).", "danger")
            return redirect(request.url)

        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        uploaded_file = filename

        # Save file in DB
        media = MediaFile(
            user_id=current_user.id,
            filename=filename,
            file_type=filename.rsplit(".", 1)[1].lower(),
            original_language="english"
        )
        db.session.add(media)
        db.session.commit()

        start_time = datetime.now()
        audio_path = filepath
        temp_audio_path = None

        try:
            # Convert video to audio if needed
            file_ext = filename.rsplit(".", 1)[1].lower()
            if file_ext == "mp4":
                temp_audio_path = extract_audio_moviepy(filepath)
                if temp_audio_path:
                    audio_path = temp_audio_path
                else:
                    flash("Error extracting audio from video.", "danger")
                    return redirect(request.url)

            # Transcribe with Whisper
            extracted_text = transcribe_audio_optimized(audio_path)
            if not extracted_text:
                flash("Error transcribing audio.", "danger")
                return redirect(request.url)

            # Translate with optimized function
            translated_text = translate_text_optimized(extracted_text, target_language)

            # Save translations in DB
            translation = Translation(
                english_sentence=extracted_text,
                shona_subtitle=translated_text if target_language == "shona" else "",
                shona_translation=translated_text if target_language == "shona" else "",
                ndebele_subtitle=translated_text if target_language == "ndebele" else "",
                ndebele_translation=translated_text if target_language == "ndebele" else "",
            )
            db.session.add(translation)
            db.session.commit()

            # Save user's live translation
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()

            live_trans = LiveTranslation(
                translation_id=translation.id,
                selected_language=target_language,
                original_text=extracted_text,
                translated_text=translated_text,
                start_time=start_time,
                end_time=end_time
            )
            db.session.add(live_trans)
            db.session.commit()

            flash(f"Translation completed in {processing_time:.1f} seconds!", "success")

        except Exception as e:
            logger.error(f"Processing error: {e}")
            flash("An error occurred during processing.", "danger")
            return redirect(request.url)
            
        finally:
            # Cleanup temporary audio file
            if temp_audio_path and os.path.exists(temp_audio_path):
                try:
                    os.remove(temp_audio_path)
                except Exception as e:
                    logger.error(f"Error cleaning up temp file: {e}")

    # Fetch files and translations for display
    files = MediaFile.query.filter_by(user_id=current_user.id).all()
    live_translations = LiveTranslation.query.join(Translation).all()

    for lt in live_translations:
        lt.time_taken = (lt.end_time - lt.start_time).total_seconds() if lt.start_time and lt.end_time else None

    return render_template(
        "trans/recorded.html",
        files=files,
        translations=live_translations,
        uploaded_file=uploaded_file,
        extracted_text=extracted_text,
        translated_text=translated_text,
        selected_language=selected_language,
        processing_time=processing_time
    )

# Additional lightweight endpoint for progress tracking
@trans_bp.route("/upload-progress", methods=["POST"])
@login_required
def upload_progress():
    """Lightweight endpoint to check upload status"""
    return jsonify({"status": "completed"})

# @trans_bp.route('/recorded-translation', methods=['GET', 'POST'])
# @login_required
# def recorded_translation():

#     return render_template("trans/recorded.html")

@trans_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():

    return render_template("trans/profile.html")


# @trans_bp.route('/reports', methods=['GET', 'POST'])
# @login_required
# def reports():
#     return render_template('trans/reports.html', user=current_user)

@trans_bp.route('/reports', methods=['GET', 'POST'])
@login_required
def reports():
    reports_data = []

    # Reports from uploaded media files (with linked translations)
    files = MediaFile.query.filter_by(user_id=current_user.id).all()
    for file in files:
        # Fetch translations for this file
        translations = Translation.query.all()  # You can filter by file if needed
        for t in translations:
            time_taken = (t.created_at - file.created_at).total_seconds() if t.created_at and file.created_at else 0
            reports_data.append({
                "filename": file.filename,
                "file_type": file.file_type,
                "uploaded_at": file.created_at,
                "original_text": t.english_sentence,
                "language": "Shona & Ndebele",
                "translated_text": f"Shona: {t.shona_translation} | Ndebele: {t.ndebele_translation}",
                "processed_at": t.created_at,
                "time_taken": f"{time_taken:.2f} seconds"
            })

    # Reports from live translations
    live_translations = LiveTranslation.query.join(Translation).all()
    for lt in live_translations:
        duration = (lt.end_time - lt.start_time).total_seconds() if lt.end_time and lt.start_time else 0
        reports_data.append({
            "filename": "Live Stream",
            "file_type": "Live",
            "uploaded_at": lt.start_time,
            "original_text": lt.original_text,
            "language": lt.selected_language.capitalize(),
            "translated_text": lt.translated_text,
            "processed_at": lt.end_time,
            "time_taken": f"{duration:.2f} seconds" if duration else "Real-Time"
        })

    return render_template(
        "trans/reports.html",
        user=current_user,
        reports=reports_data
    )


