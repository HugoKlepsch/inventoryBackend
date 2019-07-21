var signup_form = document.getElementById('signup form');

// username field checking
var username = document.getElementById('username');
validateAndDisplayHelp([username], 'Username must be between 4 & 30 alphanumeric characters');

// name field checking
var name_input = document.getElementById('name_input');
validateAndDisplayHelp([name_input], 'Name must be between 1 & 50 alphabetic characters, spaces or hyphens');

// email field checking
var email = document.getElementById('email');
var confirm_email = document.getElementById('confirm_email');
validateAndDisplayHelp([email], 'Must be an email address');
validateAndDisplayHelp([confirm_email], 'Must be an email address', [
  function() {
    return checkValidityInputsSameValue(email, confirm_email, 'Email');
  }
]);

// password field checking
var password = document.getElementById('password');
var confirm_password = document.getElementById('confirm_password');
validateAndDisplayHelp([password], 'Password must be at least 4 characters');
validateAndDisplayHelp([confirm_password], 'Password must be at least 4 characters', [
  function() {
    return checkValidityInputsSameValue(password, confirm_password, 'Password');
  }
]);

// function called when Sign up button is clicked
// if signup is valid then post signup form to web api
function signup() {
  if (!username.checkValidity()) { return; }
  if (!password.checkValidity()) { return; }
  if (!confirm_password.checkValidity()) { return; }
  if (!email.checkValidity()) { return; }
  if (!confirm_email.checkValidity()) { return; }
  signup_form.submit();
}
