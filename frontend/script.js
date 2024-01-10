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
    console.log("Valt alternativ:", selectedFramework);

    // Här kan du göra ytterligare handlingar beroende på det valda alternativet
    // Till exempel skicka detta val till din Flask-backend eller hantera det på annat sätt
});

document.getElementById('create-project').addEventListener('click', () => {
    // Samla in data
    const projectName = document.getElementById('project-name').value;
    const selectedFramework = document.getElementById('framework-selector').value;
    const selectedDirectory = localStorage.getItem('selectedDirectory');

    // Kontrollera att all information är ifylld
    if (!projectName || !selectedDirectory || !selectedFramework) {
        console.error("All information är inte ifylld");
        return;
    }

    // Skapa dataobjekt för POST-begäran
    const projectData = {
        project_type: selectedFramework,
        project_name: projectName,
        project_path: selectedDirectory
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
