// Creates a button group for the DA and AP labels and appends it to the target
function createLabelBtnsGroup(group, target) {

    // Create label group div
    var label_group = document.createElement("div");
    label_group.className = "label-group";

    for (var i = 0; i < group.length; i++) {

        // Create button for label
        var label_btn = document.createElement("button");
        label_btn.className = "label-button";
        label_btn.innerHTML = group[i];

        // Append to group
        label_group.appendChild(label_btn);
    }

    // Append to target
    target.append(label_group);
}