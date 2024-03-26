import subprocess
import json
from flask import Blueprint, request, jsonify
from config import settings

remove = Blueprint('remove', __name__)

@remove.route('/packages/remove', methods=['POST'])
def remove_packages():
    try:
        data = request.json
        packages = data.get('packages', [])

        if not packages:
            return jsonify({'error': 'No packages provided in the request.'}), 400

        package_manager = data.get('package_manager', settings.PACKAGE_MANAGER)

        with open('config/config.json', 'r') as config_file:
            config = json.load(config_file)

        package_manager_commands = config.get(package_manager)

        if package_manager_commands is None:
            return jsonify({'error': f'No remove commands found for package manager: {package_manager}'}), 500
        
        results = {}
        for command in package_manager_commands.get('remove', []):
            command_to_run = [command] + packages  # Seznam s příkazem a balíčky
            command_to_run_str = ' '.join(command_to_run)  # Spojení prvků do jednoho řetězce
            print("Command to run:", command_to_run_str)
            result = subprocess.run(command_to_run_str, capture_output=True, text=True, shell=True)

            results[command] = {
                    "returncode": result.returncode,
                    "output": result.stdout,
                    "error": result.stderr
                }

            if result.returncode == 0:
                return jsonify({'success': f'Package {packages} was successfully removed.'}), 200
            

    except Exception as e:
        return jsonify({'error': str(e)}), 500
        