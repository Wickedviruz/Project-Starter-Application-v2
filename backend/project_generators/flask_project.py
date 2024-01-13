import os
import re

# Skapa en funktion som skapar ett flask-projekt
def create_flask_project(base_path, project_name, project_options):
    # Ta bort ogiltiga tecken från projektets namn och ersätt med "_"
    project_name = re.sub(r'[\/:*?"<>|]', '_', project_name)
    project_path = os.path.join(base_path, project_name)

    # Kontrollera om projektet redan existerar
    if os.path.exists(project_path):
        return False
    
    # Skapa projektstruktur
    os.makedirs(project_path, exist_ok=True)

    import_content = "from flask import Flask\n"
    main_content = "\n"

    # Lägg till SQLAlchemy om valt
    if 'sqlalchemy' in project_options:
        import_content += "from flask_sqlalchemy import SQLAlchemy\n"
        main_content += "db = SQLAlchemy(app)\n\n"
        requirements['content'] += "SQLAlchemy\n"

    # Lägg till Flask-RESTful om valt
    if 'flask_restful' in project_options:
        import_content += "from flask_restful import Resource, Api\n"
        main_content += "api = Api(app)\n\n"
        requirements['content'] += "Flask-RESTful\n"
  
    # Skapa undermappar
    os.makedirs(os.path.join(project_path, 'app', 'templates'), exist_ok=True)
    os.makedirs(os.path.join(project_path, 'tests'), exist_ok=True)
    os.makedirs(os.path.join(project_path, 'venv'), exist_ok=True)

    # Anropa funktionen write_file för att skapa och skriva till filer
    write_file(os.path.join(project_path, runpy['name']), runpy['content'])
    write_file(os.path.join(project_path, requirements['name']), requirements['content'])
    write_file(os.path.join(project_path, config['name']), config['content'])
    write_file(os.path.join(project_path, error['name']), error['content'])
    write_file(os.path.join(project_path, 'app', init['name']), init['content'])
    write_file(os.path.join(project_path, 'app', routes['name']), routes['content'])
    write_file(os.path.join(project_path, 'app', models['name']), models['content'])
    write_file(os.path.join(project_path, 'tests', '__init__.py'), testinit['content'])

    return True

# Skapa en funktion som skriver till filer
def write_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)


#run file structure
runpy = {
'name': 'run.py',
'content': "from app import app\n\
\n\
if __name__ == '__main__':\n\
    app.run(debug=True)"
}

#requirements file structure
requirements = {
'name': 'requirements.txt',
'content': "Flask\n"
}

#config file structure
config = {
'name': 'config.py',
'content': "class Config(object)\n\
debug = False\n\
TESTING = False\n\
DATABASTE_URI = 'sqldatabas'\n\
class ProductionConfig(Config):\n\
DATABASE_URI = 'sqldatabas'"
}

#error file structure
error = {
'name': 'error.py',
'content': "from app import app\n\
from flask import render_template\n\
\n\
@app.errorhandler(404)\n\
def not_found_error(error):\n\
    return render_template('404.html'), 404\n\
\n\
@app.errorhandler(500)\n\
def internal_error(error):\n\
    return render_template('500.html'), 500"
}

#init file structure
init = {
'name': '__init__.py',
'content': "from flask import Flask\n\
from app import routes\n\
import config\n\
app = Flask(__name__)"
}

#routes file structure
routes = {
'name': 'routes.py',
'content': "from app import app\n\
\n\
@app.route('/')\n\
@app.route('/index')\n\
def index():\n\
    return 'Hello, World!'"
}

#models file structure
models = {
'name': 'models.py',
'content': "from flask_sqlalchemy import SQLAlchemy\n\
db = SQLAlchemy(app)"
}

#testinit file structure
testinit = {
'name': '__init__.py',
'content': "import os\n\
import tempfile\n\
import pytest\n\
from app import app\n\
from app import db\n\
with app.app_context():\n\
    db.create_all()\n\
@pytest.fixture\ndef client():\n\
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()\n\
    app.config['TESTING'] = True\n\
    with app.test_client() as client:\n\
        with app.app_context():\n\
            yield client\n\
    os.close(db_fd)\n\
    os.unlink(app.config['DATABASE'])"
}