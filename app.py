import os
import base64
from flask import Flask, render_template, request, session, redirect, url_for, jsonify, flash, get_flashed_messages
import time # Import module time

# Import các module cần thiết từ thư thư viện cryptography
from cryptography.hazmat.primitives import serialization
# Đảm bảo rằng file crypto_utils.py tồn tại và các hàm được import là đúng.
from crypto_utils import (
    caesar_cipher,
    vigenere_cipher,
    generate_rsa_key_pair,
    rsa_encrypt,
    rsa_decrypt,
    generate_aes_key_and_iv,
    aes_encrypt,
    aes_decrypt
)

app = Flask(__name__)
app.secret_key = os.urandom(24) # RẤT QUAN TRỌNG: Đặt khóa bí mật để sử dụng session

# Thời gian mặc định cho mỗi màn chơi (ví dụ: 5 phút = 300 giây)
DEFAULT_LEVEL_TIME_LIMIT = 300 # seconds (5 minutes)

MUSIC_TRACKS = {
    'intro': 'intro.mp3',
    'select_level': 'level_select.mp3',
    'level_01': 'level_01.mp3',
    'level_02': 'level_02.mp3',
    'level_03': 'level_03.mp3',
    'level_04': 'level_04.mp3',
    'game_complete': 'game_complete.mp3',
}

SFX_TRACKS = {
    'intro': {
        'button_click': 'button_click.mp3',
        'settings_open': 'settings_open.mp3',
        'settings_close': 'settings_close.mp3',
        'game_start': 'game_start.mp3'
    },
    'select_level': {
        'button_click': 'button_click.mp3',
        'level_locked': 'level_locked.mp3',
        'game_reset': 'game_reset.mp3' 
    },
    'level_01': {
        'correct_answer': 'correct_answer.mp3',
        'wrong_answer': 'wrong_answer.mp3',
        'hint_sound': 'hint.mp3',
        'time_low_sound': 'time_low.mp3',
        'time_up_sound': 'time_up.mp3',
        'button_click': 'button_click.mp3'
    },
    'level_02': {
        'correct_answer': 'correct_answer.mp3',
        'wrong_answer': 'wrong_answer.mp3',
        'hint_sound': 'hint.mp3',
        'time_low_sound': 'time_low.mp3',
        'time_up_sound': 'time_up.mp3',
        'button_click': 'button_click.mp3'
    },
    'level_03': {
        'correct_answer': 'correct_answer.mp3',
        'wrong_answer': 'wrong_answer.mp3',
        'hint_sound': 'hint.mp3',
        'time_low_sound': 'time_low.mp3',
        'time_up_sound': 'time_up.mp3',
        'button_click': 'button_click.mp3'
    },
    'level_04': {
        'correct_answer': 'correct_answer.mp3',
        'wrong_answer': 'wrong_answer.mp3',
        'hint_sound': 'hint.mp3',
        'time_low_sound': 'time_low.mp3',
        'time_up_sound': 'time_up.mp3',
        'button_click': 'button_click.mp3'
    },
    'game_complete': {
        'congrats_music': 'Chuc_mung.mp3', # Nhạc chúc mừng cuối game
        'button_click': 'button_click.mp3'
    }
}


# Initialize RSA and AES keys once per user session
@app.before_request
def initialize_keys():
    """Initializes cryptographic keys (RSA and AES) and user settings for the session if they don't exist."""
    # RSA keys
    if 'rsa_private_key_pem' not in session:
        try:
            private_key, public_key = generate_rsa_key_pair()
            session['rsa_private_key_pem'] = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ).decode('utf-8')
            session['rsa_public_key_pem'] = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            ).decode('utf-8')
            print("DEBUG: RSA keys initialized successfully.")
        except Exception as e:
            print(f"ERROR: Failed to initialize RSA keys: {e}")
            # Consider more robust error handling for production
            raise

    # AES key (IV is generated per encryption for CBC mode)
    if 'aes_key_b64' not in session:
        try:
            aes_key, _ = generate_aes_key_and_iv() # We only need the key here
            session['aes_key_b64'] = base64.b64encode(aes_key).decode('utf-8')
            print("DEBUG: AES key initialized successfully.")
        except Exception as e:
            print(f"ERROR: Failed to initialize AES key: {e}")
            # Consider more robust error handling for production
            raise

    # Initialize default settings in session if not present
    if 'music_enabled' not in session:
        session['music_enabled'] = True
    if 'language' not in session:
        session['language'] = 'vi'
    if 'volume' not in session: # Thêm khởi tạo âm lượng mặc định
        session['volume'] = 50 # Mặc định là 50%

# --- Game data (Answers and puzzles) ---
GAME_DATA = {
    'level_01': {
        'title': 'Bí mật của "Khuong"',
        'encrypted_message': 'KHUONG',
        'correct_answer': 'GWEN', # KHUONG -> GWEN is a Caesar cipher with shift -3 (or +23)
        'description': 'Bạn tìm thấy một mảnh giấy cũ với dòng chữ kỳ lạ: "<span class="text-yellow-400 font-bold text-xl">{{ encrypted_message | default(\'Khuong\') }}</span>". Có vẻ như nó đã bị mã hóa bằng một phương pháp dịch chuyển đơn giản, và đây là tên của một người. Gwen và Bob là hai người bạn thân, và một trong số họ đã để lại tin nhắn này.<br>Bạn có thể tìm ra tên thật không?',
        'hint': 'Gợi ý: Hãy thử dịch chuyển các chữ cái trong bảng chữ cái! Ví dụ A->D, B->E... Hoặc tìm hiểu về mã Caesar.',
        'cipher_type': 'caesar',
        'caesar_shift': -3 # K-3=H, H-3=E, U-3=R, O-3=L, N-3=K, G-3=D
    },
    'level_02': {
        'title': 'Dấu vết của "SDUN"',
        'encrypted_message': 'SDUN',
        'correct_answer': 'PARK', # SDUN -> PARK is Caesar cipher with shift -3
        'description': 'Bạn tìm thấy một ghi chú viết vội trên bàn, chỉ có bốn chữ cái: "<span class="text-yellow-400 font-bold text-xl">{{ encrypted_message | default(\'SDUN\') }}</span>". Dòng chữ này dường như là một mật mã Caesar đơn giản, và nó liên quan đến một địa điểm quen thuộc. Lisa và Peter thường xuyên gặp nhau ở nơi này.<br>Bạn có thể tìm ra địa điểm đó không?',
        'hint': 'Gợi ý: Vẫn là mã Caesar! Hãy thử dịch chuyển các chữ cái ngược lại với Màn 01.',
        'cipher_type': 'caesar',
        'caesar_shift': -3 # S-3=P, D-3=A, U-3=R, N-3=K
    },
    'level_03': {
        'title': 'Tin nhắn từ "WKH"',
        'encrypted_message': 'WKH',
        'correct_answer': 'THE', # WKH -> THE is Caesar cipher with shift -3
        'description': 'Trên một cuốn sách cũ, bạn phát hiện một ký hiệu lạ: "<span class="text-yellow-400 font-bold text-xl">{{ encrypted_message | default(\'WKH\') }}</span>". Có vẻ như nó đã được mã hóa bằng một phương pháp dịch chuyển đơn giản, và đây là một từ khóa quan trọng để mở một chiếc hộp bí ẩn. Một trong số ba người bạn thân – Alice, Ben và Carol – đã để lại dấu vết này.<br>Bạn có thể tìm ra từ khóa đó không?',
        'hint': 'Gợi ý: Đây vẫn là một dạng mã dịch chuyển. Hãy thử dịch chuyển ngược lại!',
        'cipher_type': 'caesar',
        'caesar_shift': -3 # W-3=T, K-3=H, H-3=E
    },
    'level_04': {
        'title': 'Thử thách của "AZQLMO"',
        'encrypted_message': 'AZQLMO',
        'correct_answer': 'SECRET', # AZQLMO -> SECRET using Vigenere with key HUNT
        'description': 'Bạn nhận được một tin nhắn khó hiểu: "<span class="text-yellow-400 font-bold text-xl">{{ encrypted_message | default(\'AZQLMO\') }}</span>". Đây không phải là một tên người, mà là một mật mã Vigenere với khóa là "HUNT". Tin nhắn này là manh mối để mở cánh cửa cuối cùng.<br>Bạn có thể tìm ra từ khóa giải mã không?',
        'hint': 'Gợi ý: Đây là mật mã Vigenere. Hãy nhớ sử dụng khóa "HUNT" và bảng Vigenere.',
        'cipher_type': 'vigenere',
        'vigenere_key': 'HUNT'
    }
}


# --- Route for Game Introduction Page (New Homepage) ---
@app.route('/', methods=['GET', 'POST'])
@app.route('/intro', methods=['GET', 'POST'])
def intro():
    """Renders the game introduction page and handles settings updates."""
    # Lấy giá trị hiện tại từ session, nếu không có thì dùng mặc định
    initial_music_enabled = session.get('music_enabled', True)
    current_language = session.get('language', 'vi')
    current_volume = session.get('volume', 50) # Lấy giá trị âm lượng từ session

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'save_settings':
            music_enabled = 'music_enabled' in request.form
            language = request.form.get('language')
            volume = int(request.form.get('volume', 50)) # Lấy giá trị âm lượng từ form

            session['music_enabled'] = music_enabled
            session['language'] = language
            session['volume'] = volume # Lưu âm lượng vào session
            
            flash("Cài đặt đã được lưu thành công!", "success")
            
            # Cập nhật các biến để hiển thị đúng trong template sau khi lưu
            initial_music_enabled = music_enabled
            current_language = language
        
    return render_template('game_intro.html', 
                            initial_music_enabled=initial_music_enabled,
                            current_language=current_language,
                            current_volume=current_volume, 
                            music_track=MUSIC_TRACKS.get('intro'), 
                            sfx_tracks=SFX_TRACKS.get('intro', {}), 
                            messages=get_flashed_messages(with_categories=True))

@app.route('/select_level')
def select_level():
    """Renders the level selection page and passes completion status."""
    levels_completed = {
        'level_01': session.get('level_01_correct', False),
        'level_02': session.get('level_02_correct', False),
        'level_03': session.get('level_03_correct', False),
        'level_04': session.get('level_04_correct', False)
    }

    levels_unlocked = {
        'level_01': True, 
        'level_02': levels_completed['level_01'], 
        'level_03': levels_completed['level_02'], 
        'level_04': levels_completed['level_03'],
    }

    return render_template('select_level.html',
                            levels_unlocked=levels_unlocked,
                            levels_completed=levels_completed,
                            music_track=MUSIC_TRACKS.get('select_level'),
                            sfx_tracks=SFX_TRACKS.get('select_level', {}), 
                            messages=get_flashed_messages(with_categories=True))

def common_level_logic(level_id, next_level_route=None):
    """
    Handles common logic for all game levels (fetching puzzle, processing answer, countdown timer).
    Args:
        level_id (str): The ID of the current level (e.g., 'level_01').
        next_level_route (str): The route name for the next level, if any.
    Returns:
        dict: Context for rendering the template.
    """
    puzzle = GAME_DATA.get(level_id)
    if not puzzle:
        flash("Level không tồn tại.", "error")
        return redirect(url_for('select_level'))

    if f'{level_id}_start_time' not in session:
        session[f'{level_id}_start_time'] = time.time()
        session[f'{level_id}_time_up'] = False 

    is_correct = session.get(f'{level_id}_correct', False)
    
    time_elapsed = time.time() - session.get(f'{level_id}_start_time', time.time())
    time_remaining = DEFAULT_LEVEL_TIME_LIMIT - time_elapsed

    if time_remaining <= 0 and not is_correct:
        session[f'{level_id}_time_up'] = True
        if not session.get(f'flashed_time_up_{level_id}', False): 
            flash('Hết giờ! Bạn không thể nộp câu trả lời nữa.', 'error')
            session[f'flashed_time_up_{level_id}'] = True 
        
    if request.method == 'POST' and not is_correct and not session.get(f'{level_id}_time_up', False):
        user_answer = request.form.get('user_answer')
        
        if user_answer:
            if user_answer.strip().upper() == puzzle['correct_answer'].upper():
                flash("Chúc mừng! Bạn đã giải mã thành công!", "success")
                is_correct = True
                session[f'{level_id}_correct'] = True
                # Dừng bộ đếm ngược khi trả lời đúng
                session.pop(f'{level_id}_start_time', None)
                session.pop(f'{level_id}_time_up', None)
                session.pop(f'flashed_time_up_{level_id}', None) # Xóa cờ flash cho level này
            else:
                flash("Sai rồi! Hãy thử lại.", "error")
                session[f'{level_id}_correct'] = False
        else:
            flash("Vui lòng nhập câu trả lời.", "error")

    # Nếu đã hết giờ hoặc đã trả lời đúng, không cho phép nộp nữa
    can_submit = not is_correct and not session.get(f'{level_id}_time_up', False)

    return render_template(f'{level_id}.html',
                            game_title=puzzle['title'],
                            encrypted_message=puzzle['encrypted_message'],
                            puzzle_description=puzzle['description'],
                            correct_answer=puzzle['correct_answer'],
                            hint=puzzle['hint'],
                            is_correct=is_correct,
                            next_level_route=next_level_route,
                            time_limit_seconds=DEFAULT_LEVEL_TIME_LIMIT,
                            time_remaining_seconds=max(0, int(time_remaining)), # Đảm bảo không âm
                            time_up=session.get(f'{level_id}_time_up', False),
                            can_submit=can_submit,
                            music_enabled=session.get('music_enabled', True), # Pass music settings
                            volume=session.get('volume', 50), # Pass volume settings
                            music_track=MUSIC_TRACKS.get(level_id), # Truyền tên file nhạc nền
                            sfx_tracks=SFX_TRACKS.get(level_id, {}), # Truyền các hiệu ứng âm thanh
                            messages=get_flashed_messages(with_categories=True))

@app.route('/level_01', methods=['GET', 'POST'])
def level_01():
    """Renders Level 01 game screen and handles its logic."""
    return common_level_logic('level_01', 'level_02')


@app.route('/level_02', methods=['GET', 'POST'])
def level_02():
    """Renders Level 02 game screen and handles its logic."""
    if not session.get('level_01_correct', False):
        flash("Bạn cần hoàn thành Màn 01 trước để truy cập màn này!", "warning")
        return redirect(url_for('select_level'))
    
    return common_level_logic('level_02', 'level_03')


@app.route('/level_03', methods=['GET', 'POST'])
def level_03():
    """Renders Level 03 game screen and handles its logic."""
    if not session.get('level_02_correct', False):
        flash("Bạn cần hoàn thành Màn 02 trước để truy cập màn này!", "warning")
        return redirect(url_for('select_level'))
    
    return common_level_logic('level_03', 'level_04')


@app.route('/level_04', methods=['GET', 'POST'])
def level_04():
    """Renders Level 04 game screen and handles its logic."""
    if not session.get('level_03_correct', False):
        flash("Bạn cần hoàn thành Màn 03 trước để truy cập màn này!", "warning")
        return redirect(url_for('select_level'))
    
    # Đối với level cuối cùng (level 04), next_level_route sẽ là 'game_complete'
    return common_level_logic('level_04', 'game_complete') # Đã sửa để truyền 'game_complete'

@app.route('/game_complete')
def game_complete():
    """Renders the game completion page."""
    session.pop('level_01_correct', None)
    session.pop('level_02_correct', None)
    session.pop('level_03_correct', None)
    session.pop('level_04_correct', None)
    # Clear any lingering time-related session variables
    for i in range(1, 5):
        session.pop(f'level_0{i}_start_time', None)
        session.pop(f'level_0{i}_time_up', None)
        session.pop(f'flashed_time_up_level_0{i}', None) # Đảm bảo xóa cờ này cho từng level

    return render_template('game_complete.html',
                           music_enabled=session.get('music_enabled', True),
                           volume=session.get('volume', 50),
                           music_track=MUSIC_TRACKS.get('game_complete'), # Truyền tên file nhạc nền
                           sfx_tracks=SFX_TRACKS.get('game_complete', {})) # Truyền các hiệu ứng âm thanh

@app.route('/reset_game', methods=['POST'])
def reset_game():
    """Handles resetting all game progress in the session."""
    session.clear() # Xóa toàn bộ session, bao gồm cả keys và settings
    flash("Trò chơi đã được đặt lại!", "info")
    return redirect(url_for('intro')) # Chuyển hướng về trang giới thiệu sau khi reset


if __name__ == '__main__':
    # Ensure 'static' and 'templates' directories exist
    os.makedirs('static/images', exist_ok=True)
    os.makedirs('static/audio', exist_ok=True) # Tạo thư mục audio nếu chưa có
    os.makedirs('templates', exist_ok=True)
    app.run(debug=True)