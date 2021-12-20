//=========Tokens=========
var idToken = localStorage.getItem("idToken");
var accessToken = localStorage.getItem("accessToken");


// Glabal Var
var selected_group_name = null;

function load_groups(){
    // TODO: Get Group Info API
    var idToken = localStorage.getItem("idToken");
    var accessToken = localStorage.getItem("accessToken");

    var API_addr = "https://k9wj046mrd.execute-api.us-east-1.amazonaws.com/6998FirstTry/group";

    $.ajax({
        url: API_addr + "?accessToken=" + accessToken,
        headers: {"Token": idToken},
        type: "GET",
        cache: false,
        processData: false,
        contentType: 'application/json',
        success: function (r) {
            console.log(r);
            console.log("Groups loaded");
            var res = JSON.stringify(r);
            res = JSON.parse(res);
            
            // Hide the Loading text
            document.getElementById("loading_text").style.display = "none";

            for (i=0; i<res.length; i++){
                // Load Groups info from API response
                var group_info = res[i];
                //TODO: change double m teammates in the backend
                var time = group_info["time"];
                var departure = group_info["departure"];
                var team_size = group_info["team_size"];
                var first_user_coordinate = group_info["first_user_coordinate"];

                var input = document.createElement("input");
                var label = document.createElement("label");
                
                input.type = "checkbox";
                input.id = first_user_coordinate
                input.name = "groups";
                $(input).click( function() { select_one(this) } );
                label.innerHTML = "  " + time + "/ " + departure + "/ " + "Group Size: (" + team_size + ")"
                label.htmlFor = first_user_coordinate;

                var form = document.getElementById("group_form");
                console.log(form);
                form.append(input);
                form.append(label);
                // Append a line break 
                form.append(document.createElement("br"));
                form.append(document.createElement("br"));
            }
        }
    })

    var group_form = document.getElementById("group_form");
}



function select_one(checkbox) {
    var checkboxes = document.getElementsByName("groups")
    console.log(checkboxes);
    checkboxes.forEach((item) => {
        if (item !== checkbox){
            item.checked = false
        } else {
            selected_group_name = item.id;
            console.log(selected_group_name);
        }

    })
    
}

function select_group(){
    if (selected_group_name == null){
        alert("Please select a group to continues")
    } else {
        var body = JSON.stringify({
            "first_user_coordinate": selected_group_name,
            "create_new_group": "JOIN"
        })

        var API_addr = "https://k9wj046mrd.execute-api.us-east-1.amazonaws.com/6998FirstTry/group";

        $.ajax({
            url: API_addr + "?accessToken=" + accessToken,
            headers: {"Token": idToken},
            type: 'POST',
            data: body,
            cache: false,
            processData: false,
            contentType: 'application/json',
            success: function (r) {
                console.log(r);
                alert("Group Selected!");
            }
        })
        // Jump to ready page
        window.location.assign("ready.html");
    }
}


function create_group(){
    // if (selected_group_name == null){
    //     alert("Please select a group to continues")
    // } else {
        var body = JSON.stringify({
            "first_user_coordinate": selected_group_name,
            "create_new_group": "CREATE"
        })

        var API_addr = "https://k9wj046mrd.execute-api.us-east-1.amazonaws.com/6998FirstTry/group";

        $.ajax({
            url: API_addr + "?accessToken=" + accessToken,
            headers: {"Token": idToken},
            type: 'POST',
            data: body,
            cache: false,
            processData: false,
            contentType: 'application/json',
            success: function (r) {
                console.log(r);
                alert("Group Created!");
            }
        })
        // Jump to ready page
        window.location.assign("ready.html");
    }

// }