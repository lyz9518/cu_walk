// Glabal Var
var selected_group_name = null;

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
        // API Call here
        console.log(selected_group_name);

        // Jump to ready page
        window.location.href = "ready.html";
    }
}