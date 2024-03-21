import subprocess
import json
from flask import Blueprint, request, jsonify
from config import settings

update = Blueprint('update', __name__)

@update.route('/packages/update', methods=['POST'])
def update_packages():
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
        update_command = package_manager_commands.get('update', [])
        if update_command:
            result_update = subprocess.run(update_command, capture_output=True, text=True, shell=True)
        else:
            result_update = {'returncode': -1, 'output': '', 'error': 'No update command provided'}

        # Spuštění příkazu pro zobrazení balíčků, které je možné upgradovat
        show_upgradable_command = package_manager_commands.get('show_upgradable', [])
        if show_upgradable_command:
            result_show_upgradable = subprocess.run(show_upgradable_command, capture_output=True, text=True, shell=True)
        else:
            result_show_upgradable = {'returncode': -1, 'output': '', 'error': 'No show_upgradable command provided'}

        # Vytvoření odpovědi
        response = {
            'update_result': {
                "returncode": result_update.returncode,
                "output": result_update.stdout,
                "error": result_update.stderr
            },
            'show_upgradable_result': {
                "returncode": result_show_upgradable.returncode,
                "output": result_show_upgradable.stdout,
                "error": result_show_upgradable.stderr
            }
        }

        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
