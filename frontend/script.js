document.getElementById('open-explorer').addEventListener('click', () => {
    window.api.openFileExplorer();
}); 

// Lyssnare för att hantera den valda mappens sökväg
window.api.onDirectorySelected((event, path) => {
    localStorage.setItem('selectedDirectory', path);
    
    // Uppdatera textfältet med den valda sökvägen
    document.getElementById('path-display').value = path;
});

// Funktion för att hämta den sparade mappens sökväg
function getSavedDirectory() {
    return localStorage.getItem('selectedDirectory');
}

let selectedFramework = '';
document.getElementById('framework-selector').addEventListener('change', (event) => {
    const selectedFramework = event.target.value;
    // Visa/Dölj "additional-options" baserat på valt framework
    const optionsDiv = document.getElementById('framework-options');
    
    // Rensa befintliga options
    optionsDiv.innerHTML = '';

    // Definiera de olika valen för varje ramverk
    const frameworkOptions = {
        flask: ["SQLAlchemy", "SQLite"],
        pyqt: ["Pipenv","PyQt5-tools", "PyQt5-stubs", "PyQt5-sip"],
        tkinter: ["Turtle", "Pillow", "PyInstaller", "PyAutoGUI", "PyMsgBox", "PyScreeze", "PyTweening", "PyGetWindow", "PyRect", "PyDirectInput", "PyWin32"],
        commandline: ["Argparse", "Logging"]
    };

    // Skapa checkboxes baserat på valt ramverk
    if (frameworkOptions[selectedFramework]) {
        frameworkOptions[selectedFramework].forEach(option => {
            const label = document.createElement('label');
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.value = option.toLowerCase();
            checkbox.name = 'options';
            label.appendChild(checkbox);
            label.appendChild(document.createTextNode(option));
            optionsDiv.appendChild(label);
            optionsDiv.appendChild(document.createElement('br'));
        });
    }
});

document.getElementById('create-project').addEventListener('click', () => {
    // Samla in data
    const projectName = document.getElementById('project-name').value;
    const selectedFramework = document.getElementById('framework-selector').value;
    const selectedDirectory = localStorage.getItem('selectedDirectory');
    const checkedOptions = Array.from(document.querySelectorAll('#framework-options input:checked')).map(el => el.value);

    // Kontrollera att all information är ifylld
    if (!projectName || !selectedDirectory || !selectedFramework) {
        console.error("All information är inte ifylld");
        return;
    }

    // Skapa dataobjekt för POST-begäran
    const projectData = {
        project_type: selectedFramework,
        project_name: projectName,
        project_path: selectedDirectory,
        project_options: checkedOptions
    };

    // Skicka POST-begäran till Flask-servern
    fetch('http://127.0.0.1:5000/create_project', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(projectData),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        // Uppdatera HTML-elementet med serverns svar
        document.getElementById('server-response').innerText = data.message;
    })
    .catch(error => {
        console.error('Error:', error);
        // Visa felmeddelande
        document.getElementById('server-response').innerText = 'Ett fel uppstod: ' + error.message;
    });
});
