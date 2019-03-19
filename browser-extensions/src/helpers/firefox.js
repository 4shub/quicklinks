/**
 Firefox Specific Code
 **/



function getCurrentUrl() {
    return new Promise(function (resolve) {
        browser.tabs.query({ currentWindow: true, active: true })
            .then((tabs) => {
                resolve(tabs[0].url)
            });
    });
}
