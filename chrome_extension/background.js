// workflow : new tab created -> read tab url -> run request to open ai -> if no close tab. 

// Listens for a new tab being opened and sends a message to 
// This should trigger the workflow

OPEN_AI_API_KEY = ''


async function callApi(message) {
    console.log("API key:" + OPEN_AI_API_KEY)
    console.log("Type of Work " + message.typeOfWork);
    console.log("URL " + message.url);

    data = JSON.stringify({
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": "only respond yes or no to my next question"}, 
        {"role": "user", "content": "is this url related to " + message.typeOfWork + ": " + message.url  }],
        "temperature": 0.7
    });

    console.log(data);

    fetch( 'https://api.openai.com/v1/chat/completions', {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${OPEN_AI_API_KEY}`
        },
        body: data
    })
    .then(response => response.json())
    .then(console.log)
    .catch(error => {
        throw(error);
    })
}

chrome.tabs.onUpdated.addListener((tab) => {
    console.log("In background listener");
    main();
  });

function main() {
    // Query current URL and call API 
    chrome.tabs.query({ active: true, lastFocusedWindow: true }, tabs => {
        let currentUrl = tabs[0].url;
        message = {typeOfWork: 'physics', url: currentUrl}
        result = callApi(message)
    });
}