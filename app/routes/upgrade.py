import subprocess
import json
from flask import Blueprint, request, jsonify
from config import settings

upgrade = Blueprint('upgrade', __name__)

@upgrade.route('/packages/upgrade', methods=['POST'])
def upgrade_packages():
    try:
        data = request.json
        packages = data.get('packages', [])
        

        package_manager = data.get('package_manager', settings.PACKAGE_MANAGER)

        with open('config/config.json', 'r') as config_file:
            config = json.load(config_file)

        package_manager_commands = config.get(package_manager)

        if package_manager_commands is None:
            return jsonify({'error': f'No upgrade commands found for package manager: {package_manager}'}), 500

        results = {}
        for command in package_manager_commands.get('upgrade', []):  # Přístup k příkazům pro instalaci balíčků
            if not packages:
                command_to_run = [command]
            else:
                command_to_run = [command] + packages  # Seznam s příkazem a balíčky
            command_to_run_str = ' '.join(command_to_run)  # Spojení prvků do jednoho řetězce
            print("Command to run:", command_to_run_str)
            result = subprocess.run(command_to_run_str, capture_output=True, text=True, shell=True)  # Spuštění příkazu

            results[command] = {
                "returncode": result.returncode,
                "output": result.stdout,
                "error": result.stderr
            }

            if result.returncode == 0:
                if not packages:
                    return jsonify({"success": f"Packages were successfully upgraded"}), 200
                else:
                    return jsonify({'success': f'Package {packages} was successfully upgraded.'}), 200

        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
