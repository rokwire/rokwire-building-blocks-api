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