import subprocess
from flask import Blueprint, request, jsonify

# Vytvoření blueprintu (modulu)
bp = Blueprint('execute', __name__)

# Definice API endpointu pro instalaci balíčků
@bp.route('/packages/execute', methods=['POST'])
def execute_command():
    data = request.json
    command = data.get('command')

    if command is None:
        return jsonify({'error': 'No command provided'}), 400

    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return jsonify({'output': result.stdout, 'error': result.stderr}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


