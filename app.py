from flask import Flask, render_template, request, jsonify
import os
import json
from init import click_tile, reset_game, get_game_state, set_difficulty

app = Flask(__name__)

@app.route('/')
def index():
    """Serve the main game page"""
    return render_template('index.html')

@app.route('/set_difficulty', methods=['POST'])
def handle_set_difficulty():
    """Handle difficulty selection"""
    try:
        data = request.get_json()
        difficulty = data.get('difficulty', 'beginner')
        
        if difficulty not in ['beginner', 'intermediate', 'expert']:
            return jsonify({
                'success': False,
                'error': 'Invalid difficulty level'
            }), 400
        
        # Set the difficulty
        set_difficulty(difficulty)
        game_state = get_game_state()
        
        print(f"Difficulty set to: {difficulty}")
        
        return jsonify({
            'success': True,
            'difficulty': difficulty,
            'game_state': game_state
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/click_tile', methods=['POST'])
def handle_click_tile():
    """Handle tile click requests"""
    try:
        data = request.get_json()
        row = data.get('row')
        col = data.get('col')
        
        if row is None or col is None:
            return jsonify({
                'success': False,
                'error': 'Missing row or col parameter'
            }), 400
        
        # Use the game logic from init.py
        game_state = click_tile(row, col)
        
        print(f"Tile clicked: ({row}, {col})")
        print(f"Game state: {game_state}")
        
        return jsonify({
            'success': True,
            'game_state': game_state
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/flag_tile', methods=['POST'])
def handle_flag_tile():
    """Handle tile flag requests"""
    try:
        data = request.get_json()
        row = data.get('row')
        col = data.get('col')
        
        if row is None or col is None:
            return jsonify({
                'success': False,
                'error': 'Missing row or col parameter'
            }), 400
        
        # Import flag_tile function
        from init import flag_tile
        game_state = flag_tile(row, col)
        
        return jsonify({
            'success': True,
            'game_state': game_state
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/reset_game', methods=['POST'])
def handle_reset_game():
    """Reset the game state"""
    try:
        reset_game()
        game_state = get_game_state()
        
        return jsonify({
            'success': True,
            'message': 'Game reset successfully',
            'game_state': game_state
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/game_state', methods=['GET'])
def get_current_game_state():
    """Get current game state"""
    try:
        game_state = get_game_state()
        return jsonify({
            'success': True,
            'game_state': game_state
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

if __name__ == '__main__':
    # Create static/media directory if it doesn't exist
    os.makedirs('static/media', exist_ok=True)
    
    # Move media files to static/media if they exist in the root media folder
    if os.path.exists('media'):
        import shutil
        for file in os.listdir('media'):
            if file.endswith('.png'):
                src = os.path.join('media', file)
                dst = os.path.join('static/media', file)
                if not os.path.exists(dst):
                    shutil.copy2(src, dst)
                    print(f"Copied {file} to static/media/")
    
    print("Starting Carlosweeper Flask app...")
    print("Open your browser and go to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000) 