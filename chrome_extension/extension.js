// Save it using the Chrome extension storage API.
chrome.storage.sync.get("timetable", function (obj) {  
    let timetable = obj.timetable;
    if (typeof timetable === "undefined") {
        document.getElementById("setup_panel").hidden = false 
        document.getElementById("update_panel").hidden = true
      } else {
        document.getElementById("setup_panel").hidden = true 
        document.getElementById("update_panel").hidden = false
      }
});

function setup() {
    let session_length = parseFloat(document.getElementById("session_length").value)
    let start_date = document.getElementById("start_date").value
    let start_time = document.getElementById("start_time").value
    let end_time = document.getElementById("end_time").value

    let subjects = (Array.from(document.getElementById("subjects").children).map((subjectDiv) => 
        ({
            "name": subjectDiv.children[0].textContent,
            "activities": Array.from(subjectDiv.children).filter(ele => ele.classList.contains("activity")).map(ele => ({
                "name":ele.children[0].id,
                "max_time":parseInt(ele.children[1].value),
                "min_time":parseInt(ele.children[2].value)
            }))
        })
    ))

    let jsonObj = {
       "session_length": session_length,
       "start_date": start_date,
       "start_time": start_time,
       "end_time": end_time,
       "subjects": subjects
    }
    chrome.storage.sync.set({'timetable': jsonObj});
    document.getElementById("url_data").textContent = "done" // sendToBackend(jsonObj)
}

function update() {
    let subject = document.getElementById("subject_to_update").value
    let activity_chosen = Array.from(document.getElementsByClassName("activity")).filter((ele) => ele.checked).map(ele => ele.id)[0]
    let time_delta = parseInt(document.getElementById("hours_done").value)
    chrome.storage.sync.get("timetable", function (obj) {  
        var timetable = obj.timetable;
        let subj = timetable.subjects.filter(subj => subj.name == subject)[0]
        let act = subj.activities.filter(act => act.name == activity_chosen)[0]

        console.log(timetable.subjects.filter(subj => subj.name == subject)[0])
        timetable = {
            "subjects" : [
                ...timetable.subjects.filter(subj => subj.name != subject),
                {
                    "name": subject,
                    "activities": [
                        ...subj.activities.filter(act => act.name != activity_chosen),
                        {
                            "name": activity_chosen,
                            "min_time": act.min_time - time_delta,
                            "max_time": act.max_time - time_delta
                        }
                    ]
                }
            ]
        }
        chrome.storage.sync.set({'timetable': timetable});
        sendToBackend(timetable)
        document.getElementById("update_status").textContent = "Successfully Updated!"
    });
}

function sendToBackend(timetable_data) {
    chrome.storage.sync.get("id", function (obj) {  
        let id = obj.id
        if (id == undefined) {
            id = Date.now() * 1000000 + Math.floor(Math.random() * 1000000);
            chrome.storage.sync.set({"id": id})
        }
        
        let body_data = {"file_id":id, timetable_data:timetable_data}
        console.log(body_data)
        fetch("https://ichack-e82c16304232.herokuapp.com/calculate_timetable", {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(body_data)
        }).then(res => {
            console.log(res)
        })
    });
}

function addsubject(name) {
    // Create subject container
    let subjectContainer = document.createElement('div');
    subjectContainer.classList.add('subject');

    // Create subject title
    let subjectTitle = document.createElement('h3');
    subjectTitle.textContent = name;
    subjectContainer.appendChild(subjectTitle);

    // Create activities
    let activities = ['notes', 'textbook', 'pastpapers'];
    activities.forEach(function(activityName) {
        let activityContainer = document.createElement('div');
        activityContainer.classList.add('activity');

        let activityLabel = document.createElement('span');
        activityLabel.textContent = activityName + ' (hrs):';
        activityLabel.id = activityName
        activityContainer.appendChild(activityLabel);

        let minTimeInput = document.createElement('input');
        minTimeInput.setAttribute('type', 'number');
        minTimeInput.classList.add('min_time');
        minTimeInput.setAttribute('required', true);
        activityContainer.appendChild(minTimeInput);

        let maxTimeInput = document.createElement('input');
        maxTimeInput.setAttribute('type', 'number');
        maxTimeInput.classList.add('max_time');
        maxTimeInput.setAttribute('required', true);
        activityContainer.appendChild(maxTimeInput);

        subjectContainer.appendChild(activityContainer);
    });

    // Append subject container to the document body or any desired parent element
    document.getElementById("subjects").appendChild(subjectContainer);
}

document.getElementById("setup_form").addEventListener("submit", (event) => {  event.preventDefault(); setup()})
document.getElementById("update_timetable").onclick = update
document.getElementById("addsubject").onclick = (event) => {addsubject(document.getElementById("subject_name").value)}
