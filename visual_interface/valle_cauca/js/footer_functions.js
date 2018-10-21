document.getElementById("lookfor").onchange = function() {//We need to change the background and colors of
    // the LOOK_FOR list and label so we can guide the user more easily through the process.

    var tocheck = document.getElementById("lookfor").value
    // Each of the next clausules checks which restriction was selected and then adjusts the colors.
    if (tocheck == 'references'){
    document.getElementById("lookfor").style.background = "cyan";
    document.getElementById("lookfor_label").style.background = "cyan";
    document.getElementById("lookfor").style.color = "red";
    document.getElementById("lookfor_label").style.color = "red";}

    else if (tocheck == 'coauthorship') {
    document.getElementById("lookfor").style.background = "magenta";
    document.getElementById("lookfor_label").style.background = "magenta";
    document.getElementById("lookfor").style.color = "#1aff1a";
    document.getElementById("lookfor_label").style.color = "#1aff1a";}

    else if (tocheck == 'citations') {
    document.getElementById("lookfor").style.background = "yellow";
    document.getElementById("lookfor_label").style.background = "yellow";
    document.getElementById("lookfor").style.color = "blue";
    document.getElementById("lookfor_label").style.color = "blue";
    }
};

nodeTagger();