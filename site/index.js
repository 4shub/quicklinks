/**
 * Renders a nice play button and ui around it
 */
function renderPlayButton() {
    const playContainer = document.getElementById('demo-play-container');
    const playButton = document.getElementById('demo-play-button');
    const demoVideo = document.getElementById('demo-video');
    const demoContainer = document.getElementById('demo-video-container');

    demoVideo.controls = false;

    /**
     * Plays video, returns video control tools back
     */
    function playVideo() {
        demoVideo.play();

        demoContainer.classList.add('clickedFirstTime');

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