function data_validation() {
    var contribution_name = document.getElementById('contribution_name');
    if (contribution_name.value == "") {
        // window.alert("Please enter the contribution name.");
        contribution_name.focus();
        var x = document.getElementById("contribution_name_div");
        // x.querySelector(".error_message").innerHTML = "This is required!";
        contribution_name.required = true;
        return false;
    }

    var contribution_des = document.getElementById('contribution_description');
    if (contribution_des.value == "") {
        // window.alert("Please enter the contribution description.");
        contribution_des.focus();
        contribution_des.required = true;
        return false;
    }
    var capability_name = document.getElementById('capability_name');
    var talent_name = document.getElementById('talent_name');
    if (capability_name.value == "" && talent_name.value == "") {
        document.getElementById('select-contribution').focus();
        document.getElementById('select-contribution').required = true;
        window.alert("Please enter either a capability or a talent.");
        return false;
    }
    //use capability's validation setting
    if (capability_name.value != "") {
        var capability_description = document.getElementById('capability_description');
        if (capability_description.value == "") {
            // window.alert("Please enter either a capability description.");
            capability_description.focus();
            capability_description.required = true;
            return false;
        }
        // var capability_opensource = document.getElementById('open_source');
        // if (capability_opensource.value == "") {
        //     // window.alert("Please enter if this capability is open-souced.");
        //     capability_opensource.required = true;
        //     capability_opensource.focus();
        //     return false;
        // }
        var deploy_location = document.getElementsByName('deploymentDetails_location')

        var deploy_internal = document.getElementById('deploy_internal')
        var deploy_external = document.getElementById('deploy_external')
        if (!deploy_internal.checked && !deploy_external.checked) {
            window.alert("Please select deployed location.");
            deploy_internal.focus();
            deploy_external.focus();
            return false;
        }
        var dockerimage = document.getElementById('docker_img');
        if (dockerimage.value == "") {
            // window.alert("Please enter the docker image.");
            dockerimage.focus();
            dockerimage.required = true;
            return false;
        }

        var db = document.getElementById('db-detail');
        if (db.value == "") {
            // window.alert("Please enter the database details. ");
            db.focus();
            db.required = true;
            return false;
        }
        var version = document.getElementById('version');
        if (version.value == "") {
            // window.alert("Please enter the version. ");
            version.focus();
            version.required = true;
            return false;
        }
        var health_check = document.getElementById('health');
        if (health_check.value == "") {
            // window.alert("Please enter the health check url. ");
            health_check.focus();
            health_check.required = true;
            return false;
        }
        var authmethod = document.getElementById('auth');
        if (authmethod.value == "") {
            // window.alert("Please enter the auth method. ");
            authmethod.focus();
            authmethod.required = true;
            return false;
        }
        var datadel_endpoint = document.getElementById("datadel_endpoint");
        if (datadel_endpoint.value == "") {
            // window.alert("Please enter the data deletion endpoint. ");
            datadel_endpoint.focus();
            datadel_endpoint.required = true;
            return false;
        }
        var datadel_api = document.getElementById("datadel_api");
        if (datadel_api.value == "") {
            // window.alert("Please enter the data deletion api. ");
            datadel_api.focus();
            datadel_api.required = true;
            return false;
        }
    } else {
        var talent_des = document.getElementById("talent_description");
        if (talent_des.value == "") {
            // window.alert("Please enter the talent description. ");
            talent_des.focus();
            talent_des.required = true;
            return false;
        }
    }

    //success
    // window.location.href = "/contribute";
    var x = document.getElementById('submit-pop').innerHTML = "Your Contribution is being submitted. Please wait!";
}