/**
    Chrome Specific Code
**/

function getCurrentUrl() {
    return new Promise(function (resolve) {
        chrome.tabs.query({'active': true, 'lastFocusedWindow': true}, function (tabs) {
            resolve(tabs[0].url)
        });
    })
}
