// Defaults
const SERVER_BASE = 'http://localhost:1867';

/* Endpoints */
const endpoints = {
    IS_ALIVE: '/status',
    WEBSITE: '/website'
};

/**
 * Request function
 * @param requestData
 * @returns {Promise}
 */
function request(requestData) {
    return new Promise(function (resolve, reject) {
        const http = new XMLHttpRequest();

        http.onload = function(e) {
            const statusCode = e.target.status;
            var data = e.target.response;

            try {
                data = JSON.parse(data);
            } catch (e) {

            }

            if (statusCode === 200 || statusCode === 201) {
                return resolve(data);
            }

            return reject(e);
        };

        http.onerror = function(e) {
            return reject(e);
        };

        http.onabort = function(e) {
            return reject(e);
        };


        http.open(requestData.type || 'GET', SERVER_BASE + requestData.url);

        http.responseType = 'application/json';

        if (requestData.type === 'POST') {
            http.setRequestHeader('Content-type', 'application/json');

            http.send(JSON.stringify(requestData.data));
            return;
        }

        http.send();
    });
}

/**
 * Checks if the quicklinks server is on
 */
function checkForServerExistence() {
    function serverIsOn(e) {
        if (e.status !== 'online') {
            return serverIsOff();
        }

        document.getElementById('not-connected').style.display = 'none';
        document.getElementById('connected').style.display = 'flex';
    }

    function serverIsOff() {
        document.getElementById('connected').style.display = 'none';
        document.getElementById('not-connected').style.display = 'flex';
    }


    request({ type: 'GET', url: endpoints.IS_ALIVE })
        .then(serverIsOn)
        .catch(serverIsOff);
}

/**
 * Adds a website to qucklinks
 */
function saveQuicklink() {
    const key = document.getElementById('link-name').value;
    const currentURL = document.getElementById('current-url').value;

    const saveQuickLinkButtonEl = document.getElementById('save-quicklink');

    function updateQuicklinkButtonText(text, disabledStatus) {
        saveQuickLinkButtonEl.innerText = text;
        saveQuickLinkButtonEl.disabled = disabledStatus || false;
    }

    function success() {
        updateQuicklinkButtonText('Saved Quicklink');
    }

    function onfinally() {
        setTimeout(function () {
            updateQuicklinkButtonText('Save Quicklink');
        }, 2500);
    }

    function fail() {
        updateQuicklinkButtonText('Saving Quicklink Failed!');
    }

    updateQuicklinkButtonText('Saving Quicklink...', true);
    
    request({ type: 'POST', url: endpoints.WEBSITE, data: { url: currentURL, key: key } })
        .then(success)
        .catch(fail)
        .finally(onfinally)
}

window.onload = function (ev) {
    checkForServerExistence();

    setInterval(function () {
        checkForServerExistence();
    }, 2500);

    getCurrentUrl().then(function (urlName) {
        document.getElementById("current-url").value = urlName;
    });

    // bind elements
    document.getElementById('save-quicklink').addEventListener('click', saveQuicklink);
}