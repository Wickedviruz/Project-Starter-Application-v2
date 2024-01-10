import os
import re

# Skapa en funktion som skriver till filer
def write_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

# Skapa en funktion som skapar ett tkinter-projekt
def create_pyQT_project(base_path, project_name):
    # Ta bort ogiltiga tecken från projektets namn och ersätt med "_"
    project_name = re.sub(r'[\/:*?"<>|]', '_', project_name)
    project_path = os.path.join(base_path, project_name)

    # Kontrollera om projektet redan existerar
    if os.path.exists(project_path):
        return False
    
     # Skapa projektstruktur
    os.makedirs(project_path, exist_ok=True)

     # Anropa funktionen write_file för att skapa och skriva till filer
    write_file(os.path.join(project_path, 'app.py'),"import sys\n\
import os\n\
from PyQt5.QtQml import QQmlApplicationEngine\n\
from PyQt5.QtWidgets import QApplication\n\
\n\
if __name__ == '__main__':\n\
    app = QApplication(sys.argv)\n\
    engine = QQmlApplicationEngine()\n\
    \n\
    #get folder structure for project\n\
    app_path = os.path.dirname(os.path.abspath(__file__))\n\
    \n\
    #load main.qml\n\
    main_qml_path = os.path.join(app_path, 'main.qml')\n\
    \n\
    engine.load(main_qml_path)\n\
    sys.exit(app.exec_())")
    write_file(os.path.join(project_path, 'main.qml'),"//main.qml\n\
import QtQuick 2.15\n\
import QtQuick.Window 2.12\n\n\
Window {\n\
    id: window\n\
    visible: true\n\
    width: 800\n\
    height: 600\n\
    title: 'Hello World'\n\
    color: 'lightgray'\n\
}")
    
    return True