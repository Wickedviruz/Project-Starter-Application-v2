const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
let flaskProcess = null;

function createFlaskProcess() {
    flaskProcess = spawn('python', ['../backend/server.py']);

    flaskProcess.stdout.on('data', (data) => {
        console.log(`Flask: ${data}`);
    });

    flaskProcess.stderr.on('data', (data) => {
        console.error(`Flask Error: ${data}`);
    });

    flaskProcess.on('close', (code) => {
        console.log(`Flask process exited with code ${code}`);
    });
}

function createWindow() {
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            nodeIntegration: true,
            contextIsolation: true  // Viktigt för IPC
        },
    });

    win.loadURL('http://localhost:5000');
    win.loadFile('index.html');
}

// Hantera IPC-anrop för att öppna filväljaren
ipcMain.on('open-file-explorer', async (event) => {
    const result = await dialog.showOpenDialog({
        properties: ['openDirectory']  // Ändrat till 'openDirectory' för att välja mappar
    });
    if (!result.canceled && result.filePaths.length > 0) {
        // Spara sökvägen till den valda mappen
        const selectedDirectory = result.filePaths[0];
        console.log("Vald mapp:", selectedDirectory);

        // Skicka sökvägen tillbaka till renderer-processen om det behövs
        event.reply('selected-directory', selectedDirectory);
    }
});

app.whenReady().then(() => {
    createFlaskProcess();
    createWindow();
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        flaskProcess.kill();
        app.quit();
    }
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});
