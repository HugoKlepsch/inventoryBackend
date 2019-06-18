var username = document.getElementById("username");
var login_form = document.getElementById("login form");

function validateUsername() {
  if (username.value.length <= 0) {
    username.setCustomValidity("Must have a username");
    return false;
  } else {
    username.setCustomValidity("");
    return username.checkValidity();
  }
}
username.onchange = validateUsername;

//password confirm
var password = document.getElementById("password");

function validatePassword() {
  if (password.value.length <= 5) {
    password.setCustomValidity("Must have a passward of length greater then 5");
    return false;
  } else {
    password.setCustomValidity('');
  }

  // does the password satisfy other requirements?

  return password.checkValidity();
}
password.onchange = validatePassword;

// function called when Sign up button is clicked
function login() {
  if (!validateUsername())
    return;
  if (!validatePassword())
    return;

  // log in
  login_form.submit();
}
