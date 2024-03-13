import subprocess
from flask import Blueprint, jsonify
import json

bp = Blueprint('list', __name__)

# Načtení konfiguračního souboru
with open('../config/config.json') as config_file:
    config = json.load(config_file)

@bp.route('/packages/list', methods=['GET'])
def list_packages():
    try:
        # Získání informací o distribuci
        distribution = subprocess.run(['lsb_release', '-si'], capture_output=True, text=True).stdout.strip().lower()

        # Získání příkazu pro aktuální distribuci
        command = config['distributions'].get(distribution, None)

        if command is None:
            return jsonify({"error": f"Unsupported distribution: {distribution}"}), 500

        # Spuštění příkazu a získání nainstalovaných balíčků
        result = subprocess.run(command.split(), capture_output=True, text=True)

        # Získání seznamu nainstalovaných balíčků ze výstupu příkazu
        installed_packages = [line.split()[0] for line in result.stdout.split('\n') if line]

        return jsonify({"installed_packages": installed_packages})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

