var signup_form = document.getElementById('signup form');

// username field checking
var username = document.getElementById('username');

username.onchange = function() {
    validateUsername(username);
}

// password field checking
var password = document.getElementById('password'),
var confirm_password = document.getElementById('confirm_password');

password.onchange = function() {
    validatePassword(password);
}
confirm_password.onchange = function() {
    validateSignupPasswords(password, confirm_password);
}

// email field checking
var email = document.getElementById('email'),
var confirm_email = document.getElementById('confirm_email');

confirm_email.onkeyup = function() {
    validateSignupEmails(email, confirm_email);
}

// function called when Sign up button is clicked
// if signup is valid then post signup form to web api
function signup() {
    if (!validateUsername(username)) { return; }
    if (!validateSignupPasswords(password, confirm_password)) { return; }
    if (!validateSignupEmails(email, confirm_email)) { return; }
    signup_form.submit();
}
