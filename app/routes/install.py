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
        for command in package_manager_commands.get('install', []):  # Přístup k příkazům pro instalaci balíčků
            command_to_run = [command] + packages  # Seznam s příkazem a balíčky
            command_to_run_str = ' '.join(command_to_run)  # Spojení prvků do jednoho řetězce
            print("Command to run:", command_to_run_str)
            result = subprocess.run(command_to_run_str, capture_output=True, text=True, shell=True)  # Spuštění příkazu

            # Přidání výsledku operace do slovníku
            results[command] = {
                "returncode": result.returncode,
                "output": result.stdout,
                "error": result.stderr
            }

            # Pokud byl balíček úspěšně nainstalován (návratový kód 0), odešleme úspěšnou odpověď
            if result.returncode == 0:
                return jsonify({'success': f'Package {packages} was successfully installed.'}), 200

        # Pokud se balíček nepodaří nainstalovat, pošleme kompletní výsledek operace
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
