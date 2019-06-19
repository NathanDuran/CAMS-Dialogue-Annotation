// Get the questionnaire div id
let questionnaireViewNodeId = "questionnaire-popup";
let questionnaireViewUtterancesId = "questionnaire-view-utterances";

// Keeps track of number of range sliders and the default value
let numRangeSliders = 3;
let rangeSliderDefaultValue = 4;

// Opens the questionnaire popup
function openQuestionnaire() {

    // Generate the utterance list and range slider values
    if (currentDialogue !== null && currentDialogue.is_labelled) {

        // Set the sliders values
        setSlidersValues(currentDialogue);

        // Create button/labels list for current dialogue
        let utterance_list = createQuestionnaireUtteranceList(currentDialogue);
        // Append to target
        document.getElementById(questionnaireViewUtterancesId).appendChild(utterance_list);

        // Open the popup
        document.getElementById(questionnaireViewNodeId).style.display = "block";
    }
}

// Closes the questionnaire popup
function closeQuestionnaire() {

    // Save the state of the range sliders
    currentDialogue.questions = getSlidersValues();

    // Set back to invisible
    document.getElementById(questionnaireViewNodeId).style.display = "none";
    // Clear the utterance list
    clearAllChildren(document.getElementById(questionnaireViewUtterancesId));
}

// When the user clicks anywhere outside of the questionnaire, close it
window.onclick = function (event) {
    if (event.target === document.getElementById(questionnaireViewNodeId)) {
        closeQuestionnaire();
    }
};

// Toggles label selected and updates utterance labelled flag
function questionnaireLabelBtnClick() {
    console.log("Questionnaire label button clicked...");

    // Get the label/button type (AP or DA) and utterances index
    let btnType = this.id.split("_")[0];
    let index = this.id.split("_")[1];
    let utterance = currentDialogue.utterances[index];

    // Determine if we are selecting or un-selecting
    let selected = null;
    if (this.className.includes('selected')) {
        selected = false;
    } else if (!this.className.includes('selected')) {
        selected = true;
    }

    // Toggle the buttons state and set the utterances label flag
    toggleButtonSelectedState(this, selected);

    if (btnType === 'ap-btn') {
        utterance.ap_flag = selected;
    } else if (btnType === 'da-btn') {
        utterance.da_flag = selected;
    }
}

// Updates the selected item of the range slider on interaction
function updateSlider(element) {

    // Get the id of the slider and/or list that was clicked
    let groupId = null;
    if (element.nodeName === 'LI') {
        groupId = element.parentNode.id.split("_")[1];

    } else if (element.nodeName === 'INPUT') {
        groupId = element.id.split("_")[1];
    }

    // Get the slider labels list
    let labelsList = document.getElementById("slider-labels_" + groupId).getElementsByTagName("li");

    // Get the index of the current slider selection depending on what was clicked (list or slider)
    let index = null;
    if (element.nodeName === 'LI') {
        for (let i = 0; i < labelsList.length; i++) {
            if (labelsList[i] === element) {
                index = i + 1;
            }
        }
    } else if (element.nodeName === 'INPUT') {
        index = element.value;
    }

    // Remove the currently active
    for (let i = 0; i < labelsList.length; i++) {
        if (labelsList[i].className.includes('active')) {
            labelsList[i].classList.remove("active");
        }
    }

    // Set the new active
    if (index) {
        labelsList[index - 1].className = 'active';
        document.getElementById("slider_" + groupId).value = index;
    }
    console.log("Slider" +groupId + " value: " + document.getElementById("slider_" + groupId).value)
}

// Sets the range slider values to those of the current dialogue, else to default
function setSlidersValues(dialogue) {

    // Get the state of the range sliders/questions from the dialogue
    let questions = [];
    if (dialogue.questions && dialogue.questions.length) {
        questions = dialogue.questions;
    } // Otherwise just use default values
    else {
        for (let i = 0; i < numRangeSliders; i++) {
            questions[i] = rangeSliderDefaultValue;
        }
    }

    // Set each sliders values
    for (let i = 0; i < questions.length; i++) {
        let currentSlider = document.getElementById("slider_" + (i + 1));
        currentSlider.value = questions[i];
        updateSlider(currentSlider);
    }
}

// Gets the current values of the range sliders as a list
function getSlidersValues() {

    // Create a list to hold the slider values
    let questions = [];
    for (let i = 0; i < numRangeSliders; i++) {
        questions[i] = document.getElementById("slider_" + (i + 1)).value;
    }

    // Return the current values
    return questions;
}

function createQuestionnaireUtteranceList(dialogue) {

    // Build the utterance list
    let utteranceList = document.createElement("ul");
    utteranceList.id = "questionnaire-utterance-list";
    utteranceList.className = "questionnaire-utterance-list";

    // For each utterance in the dialogue
    for (let i = 0; i < dialogue.utterances.length; i++) {

        // Get an utterance
        let utterance = dialogue.utterances[i];

        // Create list element
        let utteranceNode = document.createElement("li");
        utteranceNode.id = "qst-utt_" + i;

        // Create the utterance text label
        let utteranceTxtLabel = document.createElement("label");
        utteranceTxtLabel.id = "qst-utt-lbl_" + i;
        utteranceTxtLabel.className = "qst-utt-lbl";
        utteranceTxtLabel.innerHTML = utterance.speaker + ": " + utterance.text;

        // Create the AP button
        let apBtn = document.createElement("button");
        apBtn.id = "ap-btn_" + i;
        apBtn.className = "qst-label-btn";
        apBtn.innerHTML = utterance.ap_label;
        // Set to selected if it was already flagged in questionnaire
        if (utterance.ap_flag === true) {
            toggleButtonSelectedState(apBtn, true);
        }
        apBtn.addEventListener("click", questionnaireLabelBtnClick);

        // Create the DA label
        let daBtn = document.createElement("button");
        daBtn.id = "da-btn_" + i;
        daBtn.className = "qst-label-btn";
        daBtn.innerHTML = utterance.da_label;
        // Set to selected if it was already flagged in questionnaire
        if (utterance.da_flag === true) {
            toggleButtonSelectedState(daBtn, true);
        }
        daBtn.addEventListener("click", questionnaireLabelBtnClick);

        // Append all to the list
        utteranceNode.appendChild(utteranceTxtLabel);
        utteranceNode.appendChild(apBtn);
        utteranceNode.appendChild(daBtn);

        // Append to the target
        utteranceList.appendChild(utteranceNode);
    }
    return utteranceList;
}

///THIS VERSION IS FOR UTTERANCES AS BUTTONS
// Creates buttons for the utterances and DA/AP labels for the questionnaire
// function createQuestionnaireUtteranceList(dialogue) {
//
//     // Build the utterance list
//     let utteranceList = document.createElement("ul");
//     utteranceList.id = "questionnaire-utterance-list";
//     utteranceList.className = "questionnaire-utterance-list";
//
//     // For each utterance in the dialogue
//     for (let i = 0; i < dialogue.utterances.length; i++) {
//
//         // Get an utterance
//         let utterance = dialogue.utterances[i];
//
//         // Create list element
//         let utteranceNode = document.createElement("li");
//         utteranceNode.id = "qst-utt_" + i;
//
//         // Create the button
//         let utteranceBtn = document.createElement("button");
//         utteranceBtn.id = "qst-utt-btn_" + i;
//         utteranceBtn.className = "utt-btn";
//
//         utteranceBtn.innerHTML = utterance.speaker + ": " + utterance.text;
//         utteranceBtn.addEventListener("click", questionnaireLabelBtnClick);
//
//         // Create the AP label
//         let apText = document.createElement("label");
//         apText.id = "ap-label_" + i;
//         apText.className = "label-container";
//         if (utterance.ap_label === "") {
//             apText.innerText = defaultApLabel;
//         } else {
//             apText.innerText = utterance.ap_label;
//         }
//
//         // Create the DA label
//         let daText = document.createElement("label");
//         daText.id = "da-label_" + i;
//         daText.className = "label-container";
//         if (utterance.da_label === "") {
//             daText.innerText = defaultDaLabel;
//         } else {
//             daText.innerText = utterance.da_label;
//         }
//
//         // Append all to the list
//         utteranceNode.appendChild(utteranceBtn);
//         utteranceNode.appendChild(apText);
//         utteranceNode.appendChild(daText);
//
//         // Append to the target
//         utteranceList.appendChild(utteranceNode);
//     }
//     return utteranceList;
// }