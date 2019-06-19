// Keeps track of which content view we are on
var currentView = null;

// Dialogue view DOM element id's
var dialogueViewUttNodeId = "dialogue-view-utterances";
var dialogueViewBtnBarNodeId = "dialogue-view-buttons";

// Current dialogue and stats
var dataset = null;
var numDialogues = null;
var currentDialogue = null;
var currentDialogueIndex = null;
var currentUtt = null;
var currentUttIndex = null;

// To keep track of when the dialogue/utterance labelling started
var dialogueStartTime = null;
var utteranceStartTime = null;

// Default labels
var defaultApLabel = "AP-Label";
var defaultDaLabel = "DA-Label";

///// Actions /////
// Control bar
function prevBtnClick() {
    console.log("Prev button clicked...");

    // Call save dialogue function
    saveDialogue(currentDialogue);

    // Clear the dialogue view
    clearAllChildren(document.getElementById("dialogue-view-utterances"));

    // Call prev dialogue function
    $.ajax({
        url: "/get_prev_dialogue.do",
        dataType: "text",
        success: function (result) {

            // Rebuild dialogue view with new current dialogue
            buildDialogueViewUtterances(document.getElementById(dialogueViewUttNodeId));
            return result;
        }
    });
}

function nextBtnClick() {
    console.log("Next button clicked...");

    // Call save dialogue function
    saveDialogue(currentDialogue);

    // Clear the dialogue view
    clearAllChildren(document.getElementById(dialogueViewUttNodeId));

    // Call next dialogue function
    $.ajax({
        url: "/get_next_dialogue.do",
        dataType: "text",
        success: function (result) {

            // Rebuild dialogue view with new current dialogue
            buildDialogueViewUtterances(document.getElementById("dialogue-view-utterances"));
            return result;
        }
    });
}

// Dialogue view utterances
function utteranceBtnClick() {
    console.log("Utterance button clicked");
    console.log(this);

    // Get the index of the button that was clicked
    let index = parseInt(this.id.split("_")[1]);

    // If this is the currently selected button unselect it
    if (index === currentUttIndex) {
        toggleButtonSelectedState(this, false);
        endUtteranceTimer();
        currentUttIndex = null;

    } else {
        // Otherwise remove the currently selected button state and select this one
        let currentUttBtn = document.getElementById("utt-btn_" + currentUttIndex);
        if (currentUttBtn) {
            toggleButtonSelectedState(currentUttBtn, false);
            endUtteranceTimer();
            currentUttIndex = null;
        }

        toggleButtonSelectedState(this, true);
        currentUttIndex = index;
        startUtteranceTimer();
    }
}

function uttClearBtnClick() {
    console.log("Clear button clicked...");
    console.log(this);

    // Get the index of the button that was clicked
    let index = parseInt(this.id.split("_")[1]);

    // Set label elements to default
    let apLabel = document.getElementById("ap-label_" + index);
    apLabel.innerHTML = defaultApLabel;
    let daLabel = document.getElementById("da-label_" + index);
    daLabel.innerHTML = defaultDaLabel;

    // Remove the labelled state
    let uttBtn = document.getElementById("utt-btn_" + index);
    toggleButtonLabelledState(uttBtn, false);

    // Set the utterance labels to default on the current dialogue and labelled to false
    currentDialogue.utterances[index].ap_label = defaultApLabel;
    currentDialogue.utterances[index].da_label = defaultDaLabel;
    currentDialogue.utterances[index].is_labelled = false;

    // Check if the timer is stopped i.e this dialogue was fully labelled before
    if (dialogueStartTime === null) {
        // If so, start the timer
        startDialogueTimer()
    }
}

// Dialogue view label button bar
function labelBtnClick() {
    console.log(this.id + " button clicked...");

    // Get the label text and its type (DA or AP)
    let labelText = this.innerHTML;
    let labelType = this.id.split("_")[0];

    // Check there is a button selected
    if (currentUttIndex !== null && currentUtt !== null) {

        // Select the appropriate element and set its label
        let label = document.getElementById(labelType + "_" + currentUttIndex);
        label.innerHTML = labelText;

        // Also update the current dialogue
        if (labelType === "ap-label") {
            currentUtt.ap_label = labelText;
        } else if (labelType === "da-label") {
            currentUtt.da_label = labelText;
        }

        // Check if this utterance is now completely labelled
        // If so then set it to labelled and increment to next utterance
        if (checkUtteranceLabels(currentUtt)) {

            // Get the currently selected utterance button and set to labelled
            let uttBtn = document.getElementById("utt-btn_" + currentUttIndex);
            toggleButtonLabelledState(uttBtn, true);
            currentUtt.is_labelled = true;

            // Unselect this utterance
            toggleButtonSelectedState(uttBtn, false);
            endUtteranceTimer();

            // Get the next unlabelled utterance starting from the current index
            if (getUnlabelledUttIndex(currentDialogue, currentUttIndex)) {
                currentUttIndex = getUnlabelledUttIndex(currentDialogue, currentUttIndex);
            } else {
                // Otherwise try and get any unlabelled utterance index
                currentUttIndex = getUnlabelledUttIndex(currentDialogue, 0);
            }

            // If there was an unlabelled utterance set the new current utterance button
            if (currentUttIndex !== null) {
                let uttBtn = document.getElementById("utt-btn_" + currentUttIndex);
                toggleButtonSelectedState(uttBtn, true);
                startUtteranceTimer();
            }
        }
    } else {
        alert("No current utterance selected!");
    }

    // Check if the current dialogue is now fully labelled
    if (checkDialogueLabels(currentDialogue)) {
        // Set the current dialogue to labelled
        currentDialogue.is_labelled = true;

        // If it wasn't already fully labelled, stop the timer
        if (dialogueStartTime !== null) {
            endDialogueTimer();
        }
    }
}

///// Build Functions /////
// Builds the dialogue view utterance list and updates the stats
function buildDialogueViewUtterances(target) {

    // Make call for current dialogue
    $.ajax({
        url: "/get_current_dialogue.do",
        dataType: "json",
        success: function (dialogue_data) {
            console.log(dialogue_data);

            // Get the current dialogue and stats from response
            dataset = dialogue_data.dataset;
            numDialogues = dialogue_data.num_dialogues;
            currentDialogue = dialogue_data.current_dialogue;
            currentDialogueIndex = dialogue_data.current_dialogue_index;

            // Create button/labels list for current dialogue
            let utterance_list = createUtteranceList(currentDialogue);
            // Append to target
            target.appendChild(utterance_list);

            // Update the stats
            updateCurrentStats();

            // Start the timer for this dialogue if it is not labelled
            if (!checkDialogueLabels(currentDialogue)) {
                startDialogueTimer();
            }

            return dialogue_data;
        }
    });
}

// Creates buttons for the utterances and DA/AP labels
function createUtteranceList(dialogue) {

    // Get the first unlabelled utterance index
    currentUttIndex = getUnlabelledUttIndex(dialogue, 0);

    // Build the utterance list
    let utteranceList = document.createElement("ul");
    utteranceList.id = "dialogue-utterance-list";
    utteranceList.className = "utterance-list";

    // For each utterance in the dialogue
    for (let i = 0; i < dialogue.utterances.length; i++) {

        // Get an utterance
        let utterance = dialogue.utterances[i];

        // Create list element
        let utteranceNode = document.createElement("li");
        utteranceNode.id = "utt_" + i;

        // Create the button
        let utteranceBtn = document.createElement("button");
        utteranceBtn.id = "utt-btn_" + i;
        utteranceBtn.className = "utt-btn";
        // Check if this utterance is already labelled or the current unlabelled
        if (utterance.is_labelled) {
            toggleButtonLabelledState(utteranceBtn, true);
        } else if (i === currentUttIndex && currentUttIndex !== null) {
            toggleButtonSelectedState(utteranceBtn, true);
            startUtteranceTimer();
        }

        utteranceBtn.innerHTML = utterance.speaker + ": " + utterance.text;
        utteranceBtn.addEventListener("click", utteranceBtnClick);

        // Create the AP label
        let apText = document.createElement("label");
        apText.id = "ap-label_" + i;
        apText.className = "label-container";
        if (utterance.ap_label === "") {
            apText.innerText = defaultApLabel;
        } else {
            apText.innerText = utterance.ap_label;
        }

        // Create the DA label
        let daText = document.createElement("label");
        daText.id = "da-label_" + i;
        daText.className = "label-container";
        if (utterance.da_label === "") {
            daText.innerText = defaultDaLabel;
        } else {
            daText.innerText = utterance.da_label;
        }

        // Create clear button
        let clearBtn = document.createElement("button");
        clearBtn.id = "clear-btn_" + i;
        clearBtn.className = "clear-btn";
        clearBtn.addEventListener("click", uttClearBtnClick);

        // Append all to the list
        utteranceNode.appendChild(utteranceBtn);
        utteranceNode.appendChild(apText);
        utteranceNode.appendChild(daText);
        utteranceNode.appendChild(clearBtn);

        // Append to the target
        utteranceList.appendChild(utteranceNode);
    }
    return utteranceList;
}

// Builds the dialogue view label button bars
function buildDialogueViewButtonBars(target) {

    // Create AP button bar div
    let apBtnBar = document.createElement("div");
    apBtnBar.className = "btn-bar";
    apBtnBar.id = "ap-btn-bar";

    // Get and build the labels
    createLabelBtns('ap_labels', "ap-label", apBtnBar);

    // Append to the target
    target.appendChild(apBtnBar);

    // Create DA button bar div
    let daBtnBar = document.createElement("div");
    daBtnBar.className = "btn-bar";
    daBtnBar.id = "da-btn-bar";

    // Get and build the labels
    createLabelBtns('da_labels', "da-label", daBtnBar);

    // Append to the target
    target.appendChild(daBtnBar);

}

// Creates button groups for the DA or AP labels and appends it to the target
function createLabelBtns(labelGroup, groupType, target) {

    $.ajax({
        url: "get_labels/" + labelGroup,
        dataType: "json",
        success: function (labelGroups) {

            // For each label group
            for (let i = 0; i < labelGroups.length; i++) {
                let group = labelGroups[i];

                // Create label group div
                let labelGroupDiv = document.createElement("div");
                labelGroupDiv.className = "label-group";

                // For each label
                for (let j = 0; j < group.length; j++) {

                    // Create button for label
                    let labelBtn = document.createElement("button");
                    labelBtn.className = "label-button";
                    labelBtn.id = groupType + "_" + group[j];
                    labelBtn.innerHTML = group[j];
                    labelBtn.addEventListener("click", labelBtnClick);

                    // Append to group
                    labelGroupDiv.appendChild(labelBtn);
                }

                // Append to target
                target.append(labelGroupDiv);
            }
        }
    });
}




