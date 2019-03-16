/**
 * Renders a nice play button and ui around it
 */
function renderPlayButton() {
    const playContainer = document.getElementById('demo-play-container');
    const playButton = document.getElementById('demo-play-button');
    const demoVideo = document.getElementById('demo-video');

    demoVideo.controls = false;

    /**
     * Plays video, returns video control tools back
     */
    function playVideo() {
        demoVideo.play();

        playContainer.style.display = 'none';
        demoVideo.controls = true;
    }

    playContainer.addEventListener('click', playVideo);

    playButton.addEventListener('keypress', function (e) {
        if (e.keyCode == 13) {
            playVideo();
        }
    });
}

window.onload = function () {
    renderPlayButton();
};