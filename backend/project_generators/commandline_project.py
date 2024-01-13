import os
import re

# Skapa en funktion som skapar ett command line-projekt
def create_command_line_project(base_path, project_name, project_options):
    # Ta bort ogiltiga tecken från projektets namn och ersätt med "_"
    project_name = re.sub(r'[\/:*?"<>|]', '_', project_name)
    project_path = os.path.join(base_path, project_name)
    # Lägg till denna rad för att printa project_options
    print("Projektalternativ:", project_options)

    # Kontrollera om projektet redan existerar
    if os.path.exists(project_path):
        return False
    
     # Skapa projektstruktur
    os.makedirs(project_path, exist_ok=True)

     # Grundstruktur för 'run.py'
    import_content = "import sys\n"
    main_content = "\n"

    # Lägg till argparse om valt
    if 'argparse' in project_options:
        import_content += "import argparse\n"
        main_content += "def parse_arguments():\n"
        main_content += "    parser = argparse.ArgumentParser()\n"
        main_content += "    # Add arguments here\n"
        main_content += "    return parser.parse_args()\n\n"

    # Lägg till logging om valt
    if 'logging' in project_options:
        import_content += "import logging\n"
        main_content += "logging.basicConfig(level=logging.INFO)\n\n"

    
    if 'argparse' in project_options:
        main_content += "    args = parse_arguments()\n"
    main_content += "    print('Hello from Command Line!')\n"
    if 'logging' in project_options:
        main_content += "    logging.info('Program started')\n"

    # Avsluta 'run.py' med huvudkoden
    main_content += "if __name__ == '__main__':\n"

    # sammanfoga import och huvudkod
    run_py_content = import_content + main_content

    # Anropa funktionen write_file för att skapa och skriva till filer
    write_file(os.path.join(project_path, 'run.py'), run_py_content)
    print('Projekt skapat med tillval:', project_options)
    
    return True

# Skapa en funktion som skriver till filer
def write_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)