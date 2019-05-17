// Get the current unlabeled utterance
function getUnlabeledUttIndex(dialogue) {

    var uttIndex = 0;
    for (var i = 0; i < dialogue.utterances.length; i++) {
        if (!dialogue.utterances[i].is_labeled){
            uttIndex = i;
            break;
        }
    }
    return uttIndex;
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

