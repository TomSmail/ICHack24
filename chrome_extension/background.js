OPEN_AI_API_KEY='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'

whiteListedUrls = ["https://chrome", "chrome://extensions/", "https://www.google.com/", "chrome://newtab/", "chrome://extensions/?errors=ngamojokpcaedomjpobibdiieeopibcb"]
// workflow : new tab created -> read tab url -> run request to open ai -> if no close tab. 

async function callApi(message, tab) {
    console.log("API key:" + OPEN_AI_API_KEY)
    console.log("Type of Work " + message.typeOfWork);
    console.log("URL " + message.url);

    data = JSON.stringify({
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": "only respond 'yes' or 'no' to my next question"}, 
        {"role": "user", "content": "can the following url be used to study : " + message.typeOfWork +  " " + message.url }],
        "temperature": 1.0
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
    .then(resp => interpretJson(resp, tab))
    .catch(error => {
        throw(error);
    })
}


// Listens for a new tab being opened and sends a message to 
// This should trigger the workflow
chrome.tabs.onUpdated.addListener((tab) => {
    console.log("In background listener");
    main(tab);
  });

function main(tab) {
    // Query current URL and call API 
    chrome.tabs.query({ active: true, lastFocusedWindow: true }, tabs => {
        let currentUrl = tabs[0].url;
        if (whiteListedUrls.includes(currentUrl)) {
            console.log("Whitelisted URL, all is good!");
        } else {
            message = {typeOfWork: 'physics', url: currentUrl}
            result = callApi(message, tab)
        }
        
    });
}

function interpretJson(json, tab) {
    console.log("json:" + json);
    console.log("choices: " + json.choices[0].message.content);
    answer = (json.choices[0].message.content).toLowerCase();
    if (answer === "no" | answer === "no." ) {
        console.log(answer);
        console.log("CLOSE TAB: " + tab);
        chrome.tabs.remove(tab, function() {
            console.log('Tab closed:', tab);
          });
    } else {
        console.log("Seems legit, move along.");
    }
}