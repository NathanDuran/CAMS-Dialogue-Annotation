// Keeps track of which content view we are on
var currentView = null;

// Dialogue view DOM element id's
var dialogueViewUttNodeId = "dialogue-view-utterances";
var dialogueViewBtnBarNodeId = "dialogue-view-buttons";
var dialogueCompleteBtn = "dialogue-complete-btn";

// Current dialogue and stats
var dataset = null;
var numDialogues = null;
var numCompleteDialogues = null;
var currentDialogue = null;
var currentDialogueIndex = null;
var currentUtt = null;
var currentUttIndex = null;

// To keep track of when the dialogue/utterance labelling started
var dialogueStartTime = null;
var utteranceStartTime = null;

// Default labels data
var labels = null;
var defaultApLabel = "AP-Label";
var defaultDaLabel = "DA-Label";

///// Actions /////
// Control bar
function prevBtnClick() {
    console.log("Prev button clicked...");

    // Check if we need to open the questionnaire because it is labelled but not is_complete
    if (checkDialogueLabels(currentDialogue) && !currentDialogue.is_complete) {
        openQuestionnaire();
    } else {
        // Clear the dialogue view
        clearAllChildren(document.getElementById(dialogueViewUttNodeId));

        // Call prev dialogue function
        $.ajax({
            type: 'post',
            url: "/get_prev_dialogue.do",
            data: JSON.stringify(currentDialogue),
            dataType: "json",
            contentType: 'application/json;charset=UTF-8',
            success: function (result) {

                // Rebuild dialogue view with new current dialogue
                buildDialogueViewUtterances(document.getElementById(dialogueViewUttNodeId));
                return result;
            }
        });
    }
}

function nextBtnClick() {
    console.log("Next button clicked...");

    // Check if we need to open the questionnaire because it is labelled but not is_complete
    if (checkDialogueLabels(currentDialogue) && !currentDialogue.is_complete) {
        openQuestionnaire();
    } else {
        // Clear the dialogue view
        clearAllChildren(document.getElementById(dialogueViewUttNodeId));

        // Call next dialogue function
        $.ajax({
            type: 'post',
            url: "/get_next_dialogue.do",
            data: JSON.stringify(currentDialogue),
            dataType: "json",
            contentType: 'application/json;charset=UTF-8',
            success: function (result) {

                // Rebuild dialogue view with new current dialogue
                buildDialogueViewUtterances(document.getElementById(dialogueViewUttNodeId));
                return result;
            }
        });
    }
}

function dialogueCompleteBtnClick() {
    console.log("Revise dialogue button clicked...");

    // If the current dialogue is labelled and completed set to incomplete
    if (currentDialogue.is_labelled && currentDialogue.is_complete) {
        // Set is_complete flag back to false and decrement number of complete
        currentDialogue.is_complete = false;
        numCompleteDialogues -= 1;
        // Toggle all of the utterances back to enabled
        toggleDialogueDisabledState(currentDialogue, false);
        // Change button to incomplete dialogue state
        toggleDialogueCompleteBtnState(false, false);
        // Update stats
        updateCurrentStats();
    } // Else if it is labelled but incomplete, open the questionnaire
    else if (currentDialogue.is_labelled && !currentDialogue.is_complete) {
        openQuestionnaire();
    } // Otherwise just alert user
    else if (!currentDialogue.is_labelled && !currentDialogue.is_complete) {
        alert("Please label all utterances first!")
    }
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
    let apLabel = document.getElementById("ap-labels_" + index);
    apLabel.innerHTML = defaultApLabel;
    let daLabel = document.getElementById("da-labels_" + index);
    daLabel.innerHTML = defaultDaLabel;

    // Remove the labelled state
    let uttBtn = document.getElementById("utt-btn_" + index);
    toggleButtonLabelledState(uttBtn, false);
    toggleDialogueCompleteBtnState(false, true);

    // Set the utterance labels to default on the current dialogue and labelled to false
    currentDialogue.utterances[index].ap_label = defaultApLabel;
    currentDialogue.utterances[index].da_label = defaultDaLabel;
    currentDialogue.utterances[index].is_labelled = false;
    currentDialogue.is_labelled = false;


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
    let labelText = this.innerText.split("\n")[0];
    let labelType = this.id.split("_")[0];

    // Check there is a button selected
    if (currentUttIndex !== null && currentUtt !== null) {

        // Select the appropriate element and set its label
        let label = document.getElementById(labelType + "_" + currentUttIndex);
        label.innerHTML = labelText;

        // Also update the current dialogue
        if (labelType === "ap-labels") {
            currentUtt.ap_label = labelText;
        } else if (labelType === "da-labels") {
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

        // And activate the dialogue complete button
        toggleDialogueCompleteBtnState(false, false);

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
            numDialogues = dialogue_data.num_dialogues;
            numCompleteDialogues = dialogue_data.num_complete;
            currentDialogue = dialogue_data.current_dialogue;
            currentDialogueIndex = dialogue_data.current_dialogue_index;

            if (currentDialogue !== null) {
                // Create button/labels list for current dialogue
                let utteranceList = createUtteranceList(currentDialogue);
                // Append to target
                target.appendChild(utteranceList);

                // Update the stats
                updateCurrentStats();

                // Get the new current dialogues labelled state
                let is_labelled = checkDialogueLabels(currentDialogue);

                // Start the timer for this dialogue if it is not labelled or is_complete
                if (!is_labelled && !currentDialogue.is_complete) {
                    startDialogueTimer();
                    // Also enable is_complete dialogue  button state
                    toggleDialogueCompleteBtnState(false, true);

                } // If it is labelled and is_complete disable the buttons
                else if (is_labelled && currentDialogue.is_complete) {
                    toggleDialogueDisabledState(currentDialogue, true);

                    // Also enable the revise dialogue button state
                    toggleDialogueCompleteBtnState(true, false);

                } // Else just make sure is_complete dialogue button is enabled
                else if (is_labelled && !currentDialogue.is_complete) {
                    toggleDialogueCompleteBtnState(false, false);
                }
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
        apText.id = "ap-labels_" + i;
        apText.className = "label-container";
        if (utterance.ap_label === "") {
            apText.innerText = defaultApLabel;
        } else {
            apText.innerText = utterance.ap_label;
        }

        // Create the DA label
        let daText = document.createElement("label");
        daText.id = "da-labels_" + i;
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

    $.ajax({
        url: "get_labels.do",
        dataType: "json",
        success: function (labels_data) {

            // Save to the global var
            labels = labels_data;

            // Create AP button bar and group divs
            let apBtnBar = document.createElement("div");
            apBtnBar.className = "btn-bar";
            apBtnBar.id = "ap-btn-bar";

            let apBtnBarGroup = document.createElement("div");
            apBtnBarGroup.className = "btn-bar-group";
            apBtnBarGroup.id = "ap-btn-bar-group";

            let apBtnBarLabel = document.createElement("label");
            apBtnBarLabel.innerHTML = "Adjacency<br>Pairs (AP)";
            apBtnBarGroup.appendChild(apBtnBarLabel);

            // Get and build the labels
            createLabelBtns("ap-labels", apBtnBarGroup);

            // Append to the target
            apBtnBar.appendChild(apBtnBarGroup);
            target.appendChild(apBtnBar);

            // Create DA button bar and group divs
            let daBtnBar = document.createElement("div");
            daBtnBar.className = "btn-bar";
            daBtnBar.id = "da-btn-bar";

            let daBtnBarGroup = document.createElement("div");
            daBtnBarGroup.className = "btn-bar-group";
            daBtnBarGroup.id = "da-btn-bar-group";

            let daBtnBarLabel = document.createElement("label");
            daBtnBarLabel.innerHTML = "Dialogue<br>Acts (DA)";
            daBtnBarGroup.appendChild(daBtnBarLabel);

            // Get and build the labels
            createLabelBtns("da-labels", daBtnBarGroup);

            // Append to the target
            daBtnBar.appendChild(daBtnBarGroup);
            target.appendChild(daBtnBar);
        }
    });
}

// Creates button groups for the DA or AP labels and appends it to the target
function createLabelBtns(labelType, target) {

    // Get the correct label group
    let labelGroups = labels[labelType];

    // For each label group
    for (let i = 0; i < labelGroups.length; i++) {
        let group = labelGroups[i]['group'];

        // Create label group div
        let labelGroupDiv = document.createElement("div");
        labelGroupDiv.className = "label-group";

        // For each label
        for (let j = 0; j < group.length; j++) {

            // Get label text from data
            let labelText = group[j]['name'];

            // Create button for label
            let labelBtn = document.createElement("button");
            labelBtn.className = "label-button";
            labelBtn.id = labelType + "_" + labelText;
            labelBtn.innerText = labelText;
            labelBtn.addEventListener("click", labelBtnClick);
            labelBtn.addEventListener("mouseover", openTooltip);
            labelBtn.addEventListener("mouseout", closeTooltip);

            // Append to group
            labelGroupDiv.appendChild(labelBtn);
        }

        // Append to target
        target.append(labelGroupDiv);
    }
}




