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

        # Spuštění příkazu pro aktualizaci balíčků pro daný balíčkovací systém
        results = {}
        for command in package_manager_commands.get('update', []):  
            result = subprocess.run(command, capture_output=True, text=True, shell=True) 

            # Přidání výsledku operace do slovníku
            results[command] = {
                "returncode": result.returncode,
                "output": result.stdout,
                "error": result.stderr
            }

        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
