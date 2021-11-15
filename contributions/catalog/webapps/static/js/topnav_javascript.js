function start() {
    var user_name = "{{user}}";
    // var user_name = $('#nav-user-data').data("user");
    //console.log(user_name)
    // alert(user_name)
    var nav_login = document.getElementById('nav_login');
    var nav_greet = document.getElementById('nav_greeting')
    var nav_user = document.getElementById('user_profile')
    var submit_btn = document.getElementById('submit_contribution')
    if (user_name.length > 0) {
        nav_login.style.display = 'none';
        nav_greet.style.display = 'block';
        nav_user.style.display = 'block';
        submit_btn.style.display = 'block';
    } else {
        nav_login.style.display = 'block';
        nav_greet.style.display = 'none';
        nav_user.style.display = 'block';
        submit_btn.style.display = 'none';
    }
}

var user_icon = document.getElementById('user_profile');
user_icon.addEventListener('click', function () {
    if (user_icon.style.display === 'block') {
        document.getElementById("myDropdown").classList.toggle("show");
    }
})

window.onclick = function (event) {
    if (!event.target.matches('.dropbtn')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        for (let i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}

function get_url(c) {
    var cur_url = window.location.href.split('/');
    if (c === "all")
        window.location.href = cur_url[0] + "?show=all"
    if (c === "capability")
        window.location.href = cur_url[0] + "?show=capability"
    if (c === "talent")
        window.location.href = cur_url[0] + "?show=talent"
}

// Add active class to the current button (highlight it)
var btnContainer = document.getElementById("myBtnContainer");
var btns = btnContainer.getElementsByClassName("btn");
for (var i = 0; i < btns.length; i++) {
    btns[i].addEventListener("click", function () {
        var current = document.getElementsByClassName("active");
        current[0].className = current[0].className.replace(" active", "");
        this.className += " active";
    });
}