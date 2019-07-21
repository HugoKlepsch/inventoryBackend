var username = document.getElementById('username');
var login_form = document.getElementById('login form');

// username field checking
validateAndDisplayHelp([username], 'Username must be between 4 & 30 alphanumeric characters');

// password field checking
var password = document.getElementById('password');

validateAndDisplayHelp([password], 'Password must be at least 4 characters');

// function called when Sign up button is clicked
function login() {
  if (!username.checkValidity()) { return; }
  if (!password.checkValidity()) { return; }
  login_form.submit();
}
