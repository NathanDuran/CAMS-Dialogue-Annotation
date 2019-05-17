// Dialogue view DOM element id's
var dialogue_view_utt_node = "dialogue-view-utterances";
var dialogue_view_btn_bar_node = "dialogue-view-buttons";

///// Actions /////
// Dialogue view utterances
function utterance_btn_click() {
    console.log(this);
}

function utterance_clear_btn_click() {
    console.log(this);
}

function prev_btn_click() {
    console.log("Prev button clicked...");
    console.log(this);
    // Save the current dialogue TODO

    // Clear the dialogue view
    clearAllChildren(document.getElementById("dialogue-view-utterances"));

    // Call prev dialogue function
    $.ajax({
        url: "/prev_dialogue/",
        dataType: "text",
        success: function (result) {

            // Rebuild dialogue view with new current dialogue
            buildDialogueViewUtterances(document.getElementById(dialogue_view_utt_node));
            return result;
        }
    });
}

function next_btn_click() {
    console.log("Next button clicked...");
    console.log(this);
    // Save the current dialogue TODO

    // Clear the dialogue view
    clearAllChildren(document.getElementById(dialogue_view_utt_node));

    // Call next dialogue function
    $.ajax({
        url: "/next_dialogue/",
        dataType: "text",
        success: function (result) {

            // Rebuild dialogue view with new current dialogue
            buildDialogueViewUtterances(document.getElementById("dialogue-view-utterances"));
            return result;
        }
    });
}

// Dialogue view label button bar
function label_btn_click() {
    console.log(this);
}

///// Build Functions /////

// Builds the dialogue view next/prev buttons and utterance list
function buildDialogueViewUtterances(target) {

    // Make call for current dialogue
    $.ajax({
        url: "/get_current_dialogue/",
        dataType: "json",
        success: function (dialogue_data) {

            // Build the utterance list
            var utterance_list = document.createElement("ul");
            utterance_list.id = "utterance-list";
            // Call create button/labels function
            createUtteranceList(dialogue_data, utterance_list);
            // Append to target
            target.appendChild(utterance_list);

            return dialogue_data;
        }
    });
}

// Creates buttons for the utterances and DA/AP labels and appends it to the target
function createUtteranceList(dialogue, target) {

    // For each utterance in the dialogue
    for (var i = 0; i < dialogue.utterances.length; i++) {

        // Get current utterance
        var utterance = dialogue.utterances[i];

        // Create list element
        var utterance_node = document.createElement("li");
        utterance_node.id = "utt_" + i;

        // Create the button
        var utterance_btn = document.createElement("button");
        utterance_btn.className = "utt-btn";
        utterance_btn.id = "utt-btn_" + i;
        utterance_btn.innerHTML = utterance.speaker + ": " + utterance.text;
        utterance_btn.addEventListener("click", utterance_btn_click);

        // Create the AP label
        var ap_text = document.createElement("label");
        ap_text.className = "utt-label-container";
        ap_text.id = "ap-label_" + i;
        if (utterance.ap_label === "") {
            ap_text.innerText = "AP-label";
        } else {
            ap_text.innerText = utterance.ap_label;
        }

        // Create the DA label
        var da_text = document.createElement("label");
        da_text.className = "utt-label-container";
        ap_text.id = "da-label_" + i;
        if (utterance.da_label === "") {
            da_text.innerText = "DA-label";
        } else {
            da_text.innerText = utterance.da_label;
        }

        // Create clear button
        var clear_btn = document.createElement("button");
        clear_btn.className = "clear-btn";
        clear_btn.id = "clear-btn_" + i;
        clear_btn.innerHTML = '<img src="../static/images/delete.png" alt="Clear" width="15" height="15"/>';
        clear_btn.addEventListener("click", utterance_clear_btn_click);

        // Append all to the list
        utterance_node.appendChild(utterance_btn);
        utterance_node.appendChild(ap_text);
        utterance_node.appendChild(da_text);
        utterance_node.appendChild(clear_btn);

        // Append to the target
        target.appendChild(utterance_node);

    }
}

// Builds the dialogue view label button bars
function buildDialogueViewButtonBars(target) {

    // Create AP button bar div
    var ap_btn_bar = document.createElement("div");
    ap_btn_bar.className = "btn-bar";
    ap_btn_bar.id = "ap-btn-bar";

    // Get and build the labels
    createLabelBtns('ap_labels', ap_btn_bar);

    // Append to the target
    target.appendChild(ap_btn_bar);

    // Create DA button bar div
    var da_btn_bar = document.createElement("div");
    da_btn_bar.className = "btn-bar";
    da_btn_bar.id = "da-btn-bar";

    // Get and build the labels
    createLabelBtns('da_labels', da_btn_bar);

    // Append to the target
    target.appendChild(da_btn_bar);

}

// Creates button groups for the DA or AP labels and appends it to the target
function createLabelBtns(label_group, target) {

    $.ajax({
        url: "get_labels/" + label_group,
        dataType: "json",
        success: function (label_groups) {

            // For each label group
            for (var i = 0; i < label_groups.length; i++) {
                var group = label_groups[i];

                // Create label group div
                var label_group = document.createElement("div");
                label_group.className = "label-group";

                // For each label
                for (var j = 0; j < group.length; j++) {

                    // Create button for label
                    var label_btn = document.createElement("button");
                    label_btn.className = "label-button";
                    label_btn.id = group[j];
                    label_btn.innerHTML = group[j];
                    label_btn.addEventListener("click", label_btn_click);

                    // Append to group
                    label_group.appendChild(label_btn);
                }

                // Append to target
                target.append(label_group);
            }
        }
    });
}




