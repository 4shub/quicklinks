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
        if (e.keyCode === 13) {
            playVideo();
        }
    });
}

const COPY_SUCCESS_CLASS = 'copySuccess';

function copyTextInElement(copyEl) {
    const inputEl = copyEl.parentNode.childNodes[1];

    inputEl.select();

    copyEl.innerText = 'Copied!';
    copyEl.classList.add(COPY_SUCCESS_CLASS);

    try {
        document.execCommand('copy');
    } catch(err) {
    }

    setTimeout(function () {
        copyEl.innerText = 'Copy';
        copyEl.classList.remove(COPY_SUCCESS_CLASS)
    }, 800)
}

function enableCopyOnCode() {
    const copyFunctions = document.getElementsByClassName('copy');

    Array.from(copyFunctions).forEach(function (el) {
       el.addEventListener('keydown', function (e) {
           if (e.keyCode === 13) {
               copyTextInElement(el);
           }
       });

        el.addEventListener('click', copyTextInElement.bind(null, el));
    });
}

window.onload = function () {
    renderPlayButton();
    enableCopyOnCode();
};