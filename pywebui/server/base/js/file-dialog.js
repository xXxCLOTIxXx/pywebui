const socket = io.connect('http://' + document.domain + ':' + location.port);


function requestFileSelection() {
    return new Promise((resolve) => {
        const requestId = generateUniqueId();
        socket.emit('pywebui_file_dialog_request', { id: requestId });

        socket.on('pywebui_filepath_response', (data) => {
            if (data.id === requestId) {
                resolve(data.filePath);
            }
        });
    });
}




function generateUniqueId() {
    return Math.random().toString(36).substr(2, 9);
}