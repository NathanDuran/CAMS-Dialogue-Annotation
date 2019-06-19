// Loads the content view on page load
window.onload = function () {

    // Get the content view the user was last looking at
    if (sessionStorage.getItem("currentView")) {
        currentView = sessionStorage.getItem("currentView");
        sessionStorage.removeItem("currentView");
    } else {
        // Else on first page load content will be undefined
        currentView = 'home'
    }

    // Load the content view
    loadContent(currentView);
};

// Saves the content view and current dialogue before page refresh
window.onbeforeunload = function () {

    // Save the current content view the user was on
    sessionStorage.setItem("currentView", currentView);

    // Check if we need to save the current dialogue
    if (currentDialogue) {
        saveDialogue(currentDialogue);

        // Reset current dialogue and stat variables
        dataset = null;
        numDialogues = null;
        currentDialogue = null;
        currentDialogueIndex = null;
        currentUtt = null;
        currentUttIndex = null;
        dialogueStartTime = null;
    }
};

// Loads the specified content to the content container
function loadContent(content) {

    // Check if we need to save the dialogue before navigating away from annotate
    if (currentView === 'annotate') {
        saveDialogue(currentDialogue);
    }

    // Check if we need to change the active nav button
    if (currentView !== content) {
        document.getElementById(currentView).classList.remove("active-nav-menu-btn");
        document.getElementById(content).className = "active-nav-menu-btn"
    } else {
        document.getElementById(content).className = "active-nav-menu-btn"
    }

    // Load the specified content and update the current view
    $("#main-content-container").load("/" + content, function () {
        currentView = content;

        // If we are loading the annotate view then build it
        if (currentView === 'annotate' &&
            document.getElementById(dialogueViewUttNodeId) !== null &&
            document.getElementById(dialogueViewBtnBarNodeId) !== null) {
            buildDialogueViewUtterances(document.getElementById(dialogueViewUttNodeId));
            buildDialogueViewButtonBars(document.getElementById(dialogueViewBtnBarNodeId));
        }
    });
}

function login() {

    // Get the user name from the input box
    let userName = document.getElementById("user-name").value;

    // If it is blank don't bother with POST request
    if (userName !== '') {
        $.ajax({
            type: 'post',
            url: "/login.do",
            data: userName,
            dataType: "json",
            success: function (result) {
                if (result.success) {
                    console.log("Logged in as: " + userName);
                    loadContent('annotate')
                } else {
                    console.log("Failed to login: " + userName);
                    alert("Failed to login: " + userName)
                }
                return result;
            }
        });
    } else {
        alert("Login ID cannot be blank!")
    }
}

function logout() {

    $.ajax({
        type: 'get',
        url: "/logout.do",
        dataType: "json",
        success: function (result) {

            // If they were successfully logged out load home page
            if (result.success) {
                console.log("Logged out: " + result.user_name);
                loadContent('home')
            } else {
                console.log("Failed to logout: " + result.user_name);
                alert("Failed to logout!")
            }
            return result;
        }
    });
}

// Saves the current dialogue to the server model
function saveDialogue(dialogue) {

    if (currentDialogue !== null) {

        // Check if a dialogue timer was started i.e. it isn't/wasn't labelled
        if (dialogueStartTime !== null) {
            endDialogueTimer();
        }
        // Check if an utterance timer was started i.e. it was selected
        if (utteranceStartTime !== null) {
            endUtteranceTimer();
        }

        $.ajax({
            type: 'post',
            url: "/save_current_dialogue.do",
            data: JSON.stringify(dialogue),
            dataType: "json",
            contentType: 'application/json;charset=UTF-8',
            success: function (result) {

                if (result.success) {
                    console.log("Saved dialogue: " + dialogue.dialogue_id);
                } else {
                    console.log("Failed to save dialogue: " + dialogue.dialogue_id);
                }
                return result;
            }
        });
    }
}

// Starts a timer for the current dialogue
function startDialogueTimer() {

    dialogueStartTime = Date.now();
    console.log("Timer started @ " + new Date().toUTCString());
    console.log("Current dialogue time: " + currentDialogue.time);
}

// Ends a timer for the current dialogue
function endDialogueTimer() {

    let timeDelta = Date.now() - dialogueStartTime;
    currentDialogue.time = currentDialogue.time + timeDelta;
    console.log("Timer ended @ " + new Date().toUTCString());
    console.log("Time taken: " + timeDelta);
    console.log("Current dialogue time: " + currentDialogue.time);
    dialogueStartTime = null;
}

// Starts a timer for the current utterance
function startUtteranceTimer() {

    // Make sure we have an utterance selected
    if (currentUttIndex !== null) {
        currentUtt = currentDialogue.utterances[currentUttIndex];

        utteranceStartTime = Date.now();
        console.log("Timer started @ " + new Date().toUTCString());
        console.log("Current utterance time: " + currentUtt.time);
    } else {
        alert("No utterance selected! cannot start timer!")
    }
}

// Ends a timer for the current utterance
function endUtteranceTimer() {
    // Make sure we have an utterance selected
    if (currentUttIndex !== null && currentUtt !== null) {

        let timeDelta = Date.now() - utteranceStartTime;
        currentUtt.time = currentUtt.time + timeDelta;
        console.log("Timer ended @ " + new Date().toUTCString());
        console.log("Time taken: " + timeDelta);
        console.log("Current utterance time: " + currentUtt.time);
        utteranceStartTime = null;
        currentUtt = null;
    } else {
        alert("No utterance selected! cannot start timer!")
    }
}

// Updates the current dialogue stats
function updateCurrentStats() {

    // Dataset
    document.getElementById('dataset-lbl').innerText = dataset.split('_')[1];

    // Dialogue
    document.getElementById('current-dialogue-id-lbl').innerText = currentDialogue.dialogue_id;
    document.getElementById('current-dialogue-index-lbl').innerText = currentDialogueIndex + 1;
    document.getElementById('num-dialogues-lbl').innerText = numDialogues;
}


// Gets the next unlabelled utterance index
function getUnlabelledUttIndex(dialogue, index) {

    let uttIndex = null;
    for (let i = index; i < dialogue.utterances.length; i++) {
        if (!dialogue.utterances[i].is_labelled) {
            uttIndex = i;
            return uttIndex;
        }
    }
    return uttIndex;
}

// Toggles the utterance buttons selected state
function toggleButtonSelectedState(button) {
    if (!button.className.includes('selected')) {
        button.className += " selected";
    } else if (button.className.includes('selected')) {
        button.className = button.className.replace(' selected', '')
    }
}

// Toggles the utterance buttons labelled state
function toggleButtonLabelledState(button) {
    if (!button.className.includes('labelled')) {
        button.className += " labelled";
    } else if (button.className.includes('labelled')) {
        button.className = button.className.replace(' labelled', '')
    }
}

// Checks if this utterance is completely labelled
function checkUtteranceLabels(utterance) {
    return !(utterance.ap_label === defaultApLabel || utterance.da_label === defaultDaLabel);
}

// Checks if this dialogue is completely labelled
function checkDialogueLabels(dialogue) {

    // For each utterance in the dialogue
    for (let i = 0; i < dialogue.utterances.length; i++) {
        if (!checkUtteranceLabels(dialogue.utterances[i])) {
            return false;
        }
    }
    return true;
}

// Clears all children from current node
function clearAllChildren(target) {
    while (target.firstChild) {
        target.removeChild(target.firstChild);
    }
}

function insertAfter(newNode, referenceNode) {
    referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
}

// Updates the selected item of the range slider
function updateSlider(element) {
    console.log(element);

    // Get the id of the slider and/or list that was clicked
    let groupId = null;
    if(element.nodeName === 'LI') {
            groupId = element.parentNode.id.split("_")[1];

    }else if (element.nodeName === 'INPUT'){
        groupId = element.id.split("_")[1];
    }

    // Get the slider labels list
    let labelsList = document.getElementById("slider-labels_" + groupId).getElementsByTagName("li");

    // Get the index of the current slider selection depending on what was clicked (list or slider)
    let index = null;
    if(element.nodeName === 'LI'){
        for (let i = 0; i < labelsList.length; i++) {
            if(labelsList[i] === element){
                index = i + 1;
            }
        }
    }else if (element.nodeName === 'INPUT'){
        index = element.value;
    }

    // Remove the currently active
    for (let i = 0; i < labelsList.length; i++) {
        if (labelsList[i].className.includes('active')) {
            labelsList[i].classList.remove("active");
        }
    }

    // Set the new active
    labelsList[index - 1].className = 'active';
    document.getElementById("slider_" + groupId).value = index;
}