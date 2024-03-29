import os
from flask import request, jsonify
from project_generators.tkinter_project import create_tkinter_project
from project_generators.pyQT_project import create_pyQT_project
from project_generators.flask_project import create_flask_project
from project_generators.commandline_project import create_command_line_project

def routes(app):
    @app.route('/create_project', methods=['POST'])
    def create_project():
        data = request.json
        project_type = data['project_type']
        project_name = data['project_name']
        project_options = data['project_options']
        
        # Hantera 'file:///'-prefix och konvertera till absolut sökväg
        project_path = data['project_path']
        if project_path.startswith('file:///'):
            project_path = project_path[8:]
        project_path = os.path.abspath(project_path)

        # Bygg fullständig sökväg till projektet
        full_project_path = os.path.join(project_path, project_name)

        # Logik för att skapa projekt baserat på mottagen data
        success = False
        if project_type == 'tkinter':
            success = create_tkinter_project(full_project_path, project_name, project_options)
        elif project_type == 'pyqt':
            success = create_pyQT_project(full_project_path, project_name, project_options)
        elif project_type == 'flask':
            success = create_flask_project(full_project_path, project_name, project_options)
        elif project_type == 'commandline':
            success = create_command_line_project(full_project_path, project_name, project_options)
        else:
            return jsonify({'status': 'error', 'message': 'Okänd projekttyp'}), 400

        if success:
            return jsonify({'status': 'success', 'message': 'Projekt skapat!'})
        else:
            return jsonify({'status': 'error', 'message': 'Kunde inte skapa projektet'}), 500
