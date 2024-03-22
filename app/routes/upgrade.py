import subprocess
import json
from flask import Blueprint, request, jsonify
from config import settings

upgrade = Blueprint('upgrade', __name__)

@upgrade.route('/packages/upgrade', methods=['POST'])
def upgrade_packages():
    try:
        # Načtení balíčkovacího systému z nastavení
        package_manager = settings.PACKAGE_MANAGER
        
        # Načtení příkazů pro balíčkovací systém z config.json
        with open('config/config.json', 'r') as config_file:
            config = json.load(config_file)

        package_manager_commands = config.get(package_manager)

        if package_manager_commands is None:
            return jsonify({'error': f'No update commands found for package manager: {package_manager}'}), 500

        # Spuštění příkazu pro aktualizaci repozitářů
        upgrade_command = package_manager_commands.get('upgrade', [])
        if upgrade_command:
            result_upgrade = subprocess.run(upgrade_command, capture_output=True, text=True, shell=True)
        else:
            result_upgrade = {'returncode': -1, 'output': '', 'error': 'No update command provided'}

        # Vytvoření odpovědi
        response = {
            'update_result': {
                "returncode": result_upgrade.returncode,
                "output": result_upgrade.stdout,
                "error": result_upgrade.stderr
            }
        }

        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
