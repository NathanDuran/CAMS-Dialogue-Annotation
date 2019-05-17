// Saves the current dialogue to the server model
function saveDialogue(dialogue) {

    $.ajax({
        type: 'post',
        url: "/save_current_dialogue/",
        data: JSON.stringify(dialogue),
        dataType: "json",
        contentType: 'application/json;charset=UTF-8',
        success: function (result) {

            if (result.success){
                console.log("Saved dialogue: " + dialogue.dialogue_id)
            }
            else {
                console.log("Failed to save dialogue: " + dialogue.dialogue_id)
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

