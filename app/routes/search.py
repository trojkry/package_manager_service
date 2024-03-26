import subprocess
import json
from flask import Blueprint, request, jsonify
from config import settings

search = Blueprint('search', __name__)

@search.route('/packages/search', methods=['POST'])
def search_packages():
    try:
        data = request.json
        package = data.get('package', [])

        if not package:
            return jsonify({'error': 'No packages provided in the request.'}), 400

        package_manager = data.get('package_manager', settings.PACKAGE_MANAGER)

        with open('config/config.json', 'r') as config_file:
            config = json.load(config_file)

        package_manager_commands = config.get(package_manager)

        if package_manager_commands is None:
            return jsonify({'error': f'No search commands found for package manager: {package_manager}'}), 500

        results = {}
        for command in package_manager_commands.get('search', []):
            command_to_run = [command] + [package]  # Seznam s příkazem a balíčky
            command_to_run_str = ' '.join(command_to_run)  # Spojení prvků do jednoho řetězce
            print("Command to run:", command_to_run_str)
            result = subprocess.run(command_to_run_str, capture_output=True, text=True, shell=True)

            results[command] = {
                    "returncode": result.returncode,
                    "output": result.stdout,
                    "error": result.stderr
                }

            if result.returncode == 0:
                return jsonify(results), 200

        return jsonify(results), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
