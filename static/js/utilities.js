function loadContent(content) {
    // On first page load content will be undefined
    if (typeof content == "undefined") {
        content = 'home';
    }

    // Load the specified content
    $("#content-container").load("/" + content);

    // Check if we need to change the active nav button
    changeActiveNavBtn(content);
}

function changeActiveNavBtn(content) {

    // Get the currently active and target button based on content
    var currentBtn = document.getElementsByClassName("active-nav-menu-btn")[0];
    var targetBtn = document.getElementById(content);

    // If we are not on the right page then swap active state
    if (currentBtn.id !== targetBtn.id) {
        currentBtn.classList.remove("active-nav-menu-btn");
        targetBtn.className = "active-nav-menu-btn";
    }
}

function login() {

    console.log("Login");
    var user_name = document.getElementById("user_name").value;
    console.log(user_name);
    $.ajax({
        type: 'post',
        url: "/login.do",
        data: user_name,
        dataType: "json",
        success: function (result) {
            if (result.success) {
                console.log("Logged in as: " + user_name);
                loadContent('annotate')
            } else {
                console.log("Failed to login: " + user_name);
                alert("failed to login!")
            }
            return result;
        }
    });
}

function logout() {

    console.log("Logout");
    var user_name = document.getElementById("user_name").value;
    console.log(user_name);
    $.ajax({
        type: 'post',
        url: "/login.do",
        data: user_name,
        dataType: "json",
        success: function (result) {
            if (result.success) {
                console.log("Logged in as: " + user_name);
                loadContent('annotate')
            } else {
                console.log("Failed to login: " + user_name);
                alert("failed to login!")
            }
            return result;
        }
    });
}

// Saves the current dialogue to the server model
function saveDialogue(dialogue) {

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

// Get the next unlabeled utterance
function getUnlabeledUttIndex(dialogue) {

    var uttIndex = null;
    for (var i = 0; i < dialogue.utterances.length; i++) {
        if (!dialogue.utterances[i].is_labeled) {
            uttIndex = i;
            return uttIndex;
        }
    }
    return uttIndex;
}

// Toggles the buttons labeled state
function setButtonLabeledState(button) {
    // Get the index of the button that was clicked
    var index = button.id.split("_")[1];
    if (checkLabels(currentDialogue.utterances[index])) {
        button.className = "utt-btn labeled";
    } else {
        button.className = "utt-btn";
    }
}

// Checks if this utterance is completely labeled
function checkLabels(utterance) {
    return !(utterance.ap_label === default_ap_label || utterance.da_label === default_da_label);
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

