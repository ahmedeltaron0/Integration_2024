// fileUpload.js

function updateVideo(input) {
    const video = document.getElementById('uploaded_video');
    const file = input.files[0];
    const objectURL = URL.createObjectURL(file);
    video.src = objectURL;
    video.style.display = 'block';
}

function updateAudio(input) {
    const audio = document.getElementById('uploaded_audio');
    const file = input.files[0];
    const objectURL = URL.createObjectURL(file);
    audio.src = objectURL;
    audio.style.display = 'block';
}

function updateAudioTTS(input) {
    const audio = document.getElementById('uploaded_audio');
    const file = input.files[0];
    const objectURL = URL.createObjectURL(file);
    audio.src = objectURL;
    audio.style.display = 'block';
}
