import subprocess
import json
from flask import Blueprint, request, jsonify
from config import settings

install = Blueprint('install', __name__)

@install.route('/packages/install', methods=['POST'])
def install_packages():
    try:
        data = request.json
        packages = data.get('packages', [])
        
        if not packages:
            return jsonify({'error': 'No packages provided in the request.'}), 400

        # Zjistíme balíčkovací systém z API požadavku, pokud není uveden, použijeme hodnotu z settings.py
        package_manager = data.get('package_manager', settings.PACKAGE_MANAGER)

        # Načtení příkazů pro balíčkovací systém z config.json
        with open('config/config.json', 'r') as config_file:
            config = json.load(config_file)

        package_manager_commands = config.get(package_manager)

        if package_manager_commands is None:
            return jsonify({'error': f'No installation commands found for package manager: {package_manager}'}), 500

        # Spuštění příkazů pro instalaci balíčků pro daný balíčkovací systém
        results = {}
        for command in package_manager_commands:
            command_to_run = [command] + packages  # Upravený způsob spojení příkazu s balíčky
            result = subprocess.run(command_to_run, capture_output=True, text=True)

            # Přidání výsledku operace do slovníku
            results[command] = {
                "returncode": result.returncode,
                "output": result.stdout,
                "error": result.stderr
            }

        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
