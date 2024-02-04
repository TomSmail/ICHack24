NOTHING_TO_SEE_HERE='YXdkajl6dlFTcHB5eW5wRklrY3hKRmtibEIzVE5zSFVXSlpTZVZsRkFjanZNYzRxLWtz'
OPEN_AI_API_KEY = atob(NOTHING_TO_SEE_HERE).toString().split("").reverse().join("")

whiteListedUrls = ["https://chrome", "chrome://extensions/", "https://www.google.com/", "chrome://newtab/", "chrome://extensions/?errors=bmfmjblgbhgonchjepiileeljppdhegf"]

async function callApi(message, tab) {
    data = JSON.stringify({
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": "only respond 'yes' or 'no' to my next question"}, 
        {"role": "user", "content": "can the following url be used to study?" + message.url }],
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
chrome.tabs.onUpdated.addListener((tabId, info) => {
    console.log("In background listener");    
    if (info.status === 'complete') {
        console.log(info.status)
        main(tabId);
    }
  });

function main(tab) {
    // Query current URL and call API 
    is_supposed_to_be_studying().then((is_studying) => {if (is_studying) {
        chrome.tabs.query({ active: true, lastFocusedWindow: true }, tabs => {
            let currentUrl = tabs[0].url;
            if (whiteListedUrls.includes(currentUrl)) {
                console.log("Whitelisted URL, all is good!");
            } else {
                message = {url: currentUrl}
                result = callApi(message, tab)
            }
            
        });
    }})
}

function interpretJson(json, tab) {
    console.log("json:" + json);
    console.log("choices: " + json.choices[0].message.content);
    answer = (json.choices[0].message.content).toLowerCase();
    if (answer === "no" || answer === "no." ) {
        console.log(answer);
        console.log("CLOSE TAB: " + tab);
        chrome.tabs.remove(tab, function() {
            console.log('Tab closed:', tab);
          });
    } else {
        console.log("Seems legit, move along.");
    }
}

function is_supposed_to_be_studying() {
    return new Promise((resolve, reject) => {
        chrome.storage.sync.get("timetable", (obj) => {
            if (chrome.runtime.lastError) {
                reject(chrome.runtime.lastError);
            } else {
                if (obj.timetable == undefined) {
                    resolve(false);
                } else {
                    let t = obj.timetable;
                    let mini = new Date(t["start_date"] + " " + t["start_time"]);
                    let maxi = new Date(t["end_date"] +" " + t["end_time"]);
                    console.log(mini)
                    console.log(maxi)
                    resolve(new Date() <= maxi && new Date() >= mini);
                }
            }
        });
    });
}
