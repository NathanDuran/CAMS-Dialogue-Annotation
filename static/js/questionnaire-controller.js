// Get the questionnaire div id
let questionnaireViewNodeId = "questionnaire-popup";
let questionnaireViewUtterancesId = "questionnaire-view-utterances";

// Opens the questionnaire popup
function openQuestionnaire() {

    // Generate the utterance list first
    if (currentDialogue !== null && currentDialogue.is_labelled) {
        // Create button/labels list for current dialogue
        let utterance_list = createQuestionnaireUtteranceList(currentDialogue);
        // Append to target
        document.getElementById(questionnaireViewUtterancesId).appendChild(utterance_list);
    }
    // Open the popup
    document.getElementById(questionnaireViewNodeId).style.display = "block";
}

// Closes the questionnaire popup
function closeQuestionnaire() {
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

function questionnaireUtteranceBtnClick(){
    // Todo Replace with general toggle selected state function??
    if (!this.className.includes('selected')) {
        this.className += " selected";
    } else if (this.className.includes('selected')) {
        this.className = this.className.replace(' selected', '')
    }
}

// Creates buttons for the utterances and DA/AP labels for the questionnaire
function createQuestionnaireUtteranceList(dialogue) {

    // Build the utterance list
    let utteranceList = document.createElement("ul");
    utteranceList.id = "questionnaire-utterance-list";
    utteranceList.className = "utterance-list";

    // For each utterance in the dialogue
    for (let i = 0; i < dialogue.utterances.length; i++) {

        // Get an utterance
        let utterance = dialogue.utterances[i];

        // Create list element
        let utteranceNode = document.createElement("li");
        utteranceNode.id = "qst-utt_" + i;

        // Create the button
        let utteranceBtn = document.createElement("button");
        utteranceBtn.id = "qst-utt-btn_" + i;
        utteranceBtn.className = "utt-btn";

        utteranceBtn.innerHTML = utterance.speaker + ": " + utterance.text;
        utteranceBtn.addEventListener("click", questionnaireUtteranceBtnClick);

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

        // Append all to the list
        utteranceNode.appendChild(utteranceBtn);
        utteranceNode.appendChild(apText);
        utteranceNode.appendChild(daText);

        // Append to the target
        utteranceList.appendChild(utteranceNode);
    }
    return utteranceList;
}