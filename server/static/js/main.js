var username = document.getElementById('username');
var login_form = document.getElementById('login form');

// username field checking
username.onchange = function() {
    console.log('username.onchange');
    validateUsername(username);
}

// password field checking
var password = document.getElementById('password');

password.onchange = function() {
    console.log('password.onchange');
    validatePassword(password);
}

// function called when Sign up button is clicked
function login() {
    if (!validateUsername(username)) { return; }
    if (!validatePassword(password)) { return; }
    login_form.submit();
}
