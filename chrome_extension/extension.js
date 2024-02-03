// function callApi(revising=true, subject='work') {
    
//     getCurrentUrl()
//     chrome.runtime.sendMessage({ url: getCurrentUrl(), working: revising, typeOfWork: subject }, response => {
//         console.log(response)
//     })
// }

// function getCurrentUrl() {
//     const currentUrl = window.location.href;
//     console.log(currentUrl);
//     return currentUrl;
// }
// https://ichack-e82c16304232.herokuapp.com/
function run() {
    fetch("https://httpbin.org/post", {
        method: 'POST'
    }).then(res => {
        console.log(res)
    })
}

document.getElementById("run").onclick = run 