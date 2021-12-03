// Glabal Var
var selected_group_name = null;

function load_groups(){
    // TODO: Get Group Info API
    var group_form = document.getElementById("group_form");

    // //TODO: pseudo-code now
    // for (i=0; i<3; i++){
    //     // Create an <input> element, set its type and name attributes
    //     var input = document.createElement("input");
    //     var label = document.createElement("label");
    //     input.type = "checkbox";
    //     input.id = "group_"+i;
    //     input.name = "groups";
    //     input.value = "group_"+i;
    //     label.for = "group_"+i;
    //     container.appendChild(input);
    //     container.appendChild(label);
    //     // Append a line break 
    //     container.appendChild(document.createElement("br"));
    //     container.appendChild(document.createElement("br"));
    // }
    
}



function select_one(checkbox) {
    var checkboxes = document.getElementsByName("groups")
    checkboxes.forEach((item) => {
        if (item !== checkbox){
            item.checked = false
        } else{
            selected_group_name = item.value;
        }

    })
    
}

// TODO: Implement API call
function select_group(){
    if (selected_group_name == null){
        alert("Please select a group to continues")
    } else {
        // TODO: API Call here
        console.log(selected_group_name);

        // Jump to ready page
        window.location.href = "ready.html";
    }
}