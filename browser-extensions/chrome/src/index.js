// Defaults
const SERVER_BASE = 'http://localhost:1867';

/* Endpoints */
const endpoints = {
    IS_ALIVE: '/status',
    WEBSITE: '/website',
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
            return resolve(e);
        };

        http.onerror = function(e) {
            return reject(e);
        };

        http.onabort = function(e) {
            return reject(e);
        };


        http.open(requestData.type || 'GET', requestData.url);

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

        document.getElementById('start_server_modal').style.display = 'none';
    }

    function serverIsOff() {
        document.getElementById('start_server_modal').style.display = 'block';
    }


    request({ type: 'GET', url: endpoints.IS_ALIVE })
        .then(serverIsOn)
        .catch(serverIsOff);
}

/**
 * Adds a website to qucklinks
 */
function addWebsiteToQuicklinks() {
    const currentURL = window.location.pathname;

    function success() {
        
    }
    
    function fail() {

    }
    
    request({ type: 'POST', url: endpoints.WEBSITE, data: { url: currentURL } })
        .then(success)
        .catch(fail);
}