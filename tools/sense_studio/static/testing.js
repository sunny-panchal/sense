
function addTerminalMessage(message) {
    let terminal = document.getElementById('testTerminal');
    terminal.insertAdjacentHTML('beforeend', `<div class='monospace-font'><b>${message}</b></div>`);
    terminal.scrollTop = terminal.scrollHeight;
}

function streamVideo(message) {
    let frame = document.getElementById('frame');
    frame.src = message.image;
}

async function editInputVideoPath() {
    let inputVideoPathLabel = document.getElementById('inputVideoPathLabel');
    let inputVideoPath = document.getElementById('inputVideoPath');
    let project = document.getElementById('project');

    let name = project.value;
    let path = inputVideoPath.value;

    let directoriesResponse = await browseDirectory(path, name);

    // Check that input video path is filled and exists
    if (path === '') {
        setFormWarning(inputVideoPathLabel, inputVideoPath, '');
    } else if (!directoriesResponse.path_exists) {
        setFormWarning(inputVideoPathLabel, inputVideoPath, 'This path does not exist');
    } else if (!path.endsWith('.mp4')) {
        setFormWarning(inputVideoPathLabel, inputVideoPath, 'Please provide a valid .mp4 file');
    } else {
        setFormWarning(inputVideoPathLabel, inputVideoPath, '');
    }
}

async function startTesting(url) {
    let classifier = document.getElementById('classifier').value;
    let webcamInput = document.getElementsByName('inputSource')[0];
    let saveVideo = document.getElementById('saveVideo');
    let inputVideoPath = document.getElementById('inputVideoPath');
    let inputVideoPathValue = (webcamInput.checked) ? '' : inputVideoPath.value;
    let inputVideoPathLabel = document.getElementById('inputVideoPathLabel');
    let outputVideoName = document.getElementById('outputVideoName');
    let outputVideoNameValue = (saveVideo.checked) ? outputVideoName.value : '';
    let outputVideoNameLabel = document.getElementById('outputVideoNameLabel');
    let path = document.getElementById('path').value;
    let title = document.getElementById('title').value;
    let buttonTest = document.getElementById('btnTest');
    let buttonCancelTest = document.getElementById('btnCancelTest');
    let frame = document.getElementById('frame');

    if (!inputVideoPathValue || !inputVideoPathValue.endsWith('.mp4')) {
        setFormWarning(inputVideoPathLabel, inputVideoPath, 'Please provide a valid .mp4 file');
        return false;
    }

    if (saveVideo.checked && !outputVideoNameValue) {
        setFormWarning(outputVideoNameLabel, outputVideoName, 'Please provide a video name');
        return false;
    }

    data = {
        classifier: classifier,
        inputVideoPath: inputVideoPathValue,
        outputVideoName: outputVideoNameValue,
        path: path,
        title: title,
    };

    buttonTest.disabled = true;
    buttonCancelTest.disabled = false;

    await asyncRequest(url, data);

    let socket = io.connect('/stream-video');
    socket.on('connect', function() {
        console.log('Socket Connected');
        socket.emit('stream_video', {status: 'Socket Connected'});
    });

    socket.on('stream_frame', function(message) {
        streamVideo(message);
    });

    socket.on('success', function(message) {
        if (message.status === 'Complete') {
            frame.removeAttribute('src');
            socket.disconnect();
            console.log('Socket Disconnected');

            buttonTest.disabled = false;
            buttonCancelTest.disabled = true;
        }
    });

    socket.on('testing_logs', function(message) {
        addTerminalMessage(message.log);
    });

    addTerminalMessage('Starting Inference...');
}

async function cancelTesting(url) {
    addTerminalMessage('Stopping Inference...');
    await asyncRequest(url);

    document.getElementById('btnTest').disabled = false;
    document.getElementById('btnCancelTest').disabled = true;
}

function toggleInputVideoField() {
    let inputVideoDiv = document.getElementById('inputVideoDiv');
    let webcamInput = document.getElementsByName('inputSource')[0];

    if (webcamInput.checked) {
        inputVideoDiv.classList.add('uk-hidden');
    } else {
        inputVideoDiv.classList.remove('uk-hidden');
    }
}

function toggleOutputVideoField() {
    let outputVideoDiv = document.getElementById('outputVideoDiv');
    let saveVideo = document.getElementById('saveVideo');

    if (saveVideo.checked) {
        outputVideoDiv.classList.remove('uk-hidden');
    } else {
        outputVideoDiv.classList.add('uk-hidden');
    }
}