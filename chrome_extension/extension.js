function callApi(revising=true, subject='work') {
    
    getCurrentUrl()
    chrome.runtime.sendMessage({ url: getCurrentUrl(), working: revising, typeOfWork: subject }, response => {
        console.log(response)
    })
}

function getCurrentUrl() {
    const currentUrl = window.location.href;
    console.log(currentUrl);
    return currentUrl;
}