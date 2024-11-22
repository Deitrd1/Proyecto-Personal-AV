let blobs = [];
let stream;
let rec;
let recordUrl;
let audioResponseHandler;

/**
 * Configurar el URL y el callback que procesará las respuestas
 * @param {string} url - URL del endpoint para enviar el audio.
 * @param {function} handler - Callback para manejar la respuesta del backend.
 */
function recorder(url, handler) {
    recordUrl = url;
    if (typeof handler !== "undefined") {
        audioResponseHandler = handler;
    }
}

/**
 * Iniciar la grabación de audio
 */
async function record() {
    try {
        updateUIRecordingStart();

        blobs = [];
        stream = await navigator.mediaDevices.getUserMedia({ audio: true, video: false });
        rec = new MediaRecorder(stream);

        rec.ondataavailable = e => {
            if (e.data) blobs.push(e.data);
        };

        rec.onstop = doPreview;

        rec.start();
    } catch (e) {
        showError(
            "No fue posible iniciar el grabador de audio. Verifica que tengas los permisos necesarios y estés usando HTTPS."
        );
    }
}

/**
 * Manejar el evento onstop del MediaRecorder
 * Procesar el audio grabado y enviarlo al servidor
 */
function doPreview() {
    if (!blobs.length) {
        showError("No se pudo capturar ningún audio.");
    } else {
        const blob = new Blob(blobs);
        const fd = new FormData();
        fd.append("audio", blob, "audio");

        fetch(recordUrl, {
            method: "POST",
            body: fd,
        })
            .then(response => response.json())
            .then(audioResponseHandler)
            .catch(err => {
                showError("Ocurrió un error al procesar el audio. Intenta nuevamente.");
                console.error("Error en fetch:", err);
            });
    }
}

/**
 * Detener la grabación de audio
 */
function stop() {
    if (rec && rec.state !== "inactive") {
        updateUIRecordingStop();
        rec.stop();
    }
}

/**
 * Mostrar un mensaje de error en la interfaz
 * @param {string} message - Mensaje de error para el usuario.
 */
function showError(message) {
    const errorDiv = document.getElementById("error");
    if (errorDiv) {
        errorDiv.style.display = "block";
        errorDiv.innerText = message;
    }
    updateUIReset();
}

/**
 * Actualizar la interfaz al iniciar la grabación
 */
function updateUIRecordingStart() {
    document.getElementById("text").innerHTML = "<i>Grabando...</i>";
    document.getElementById("record").style.display = "none";
    document.getElementById("stop").style.display = "";
    document.getElementById("record-stop-label").style.display = "block";
    document.getElementById("record-stop-loading").style.display = "none";
    document.getElementById("stop").disabled = false;
}

/**
 * Actualizar la interfaz al detener la grabación
 */
function updateUIRecordingStop() {
    document.getElementById("record-stop-label").style.display = "none";
    document.getElementById("record-stop-loading").style.display = "block";
    document.getElementById("stop").disabled = true;
}

/**
 * Restablecer la interfaz a su estado inicial
 */
function updateUIReset() {
    document.getElementById("record").style.display = "";
    document.getElementById("stop").style.display = "none";
}

/**
 * Manejar la respuesta del backend
 * @param {object} response - Respuesta JSON del backend.
 */
function handleAudioResponse(response) {
    if (!response) {
        showError("No se recibió ninguna respuesta del servidor.");
        return;
    }

    updateUIReset();

    if (audioResponseHandler != null) {
        audioResponseHandler(response);
    }
}
