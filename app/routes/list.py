import json
import subprocess
from flask import Blueprint, jsonify
from config import settings

list = Blueprint('list', __name__)

@list.route('/packages/list', methods=['POST'])
def list_installed_packages():
    try:
        # Načtení balíčkovacího systému z nastavení
        package_manager = settings.PACKAGE_MANAGER
        
        # Načtení příkazu pro výpis nainstalovaných balíčků z config.json
        with open('config/config.json', 'r') as config_file:
            config = json.load(config_file)

        package_manager_commands = config.get(package_manager)

        if package_manager_commands is None:
            return jsonify({'error': f'No list command found for package manager: {package_manager}'}), 500

        # Spuštění příkazu pro výpis nainstalovaných balíčků
        list_command = package_manager_commands.get('list', [])
        if list_command:
            result_list = subprocess.run(list_command, capture_output=True, text=True, shell=True)
        else:
            result_list = {'returncode': -1, 'output': '', 'error': 'No list command provided'}

        # Vytvoření odpovědi
        response = {
            'list_result': {
                "returncode": result_list.returncode,
                "output": result_list.stdout,
                "error": result_list.stderr
            }
        }

        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
