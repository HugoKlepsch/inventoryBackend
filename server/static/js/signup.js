var username = document.getElementById("username");
var signup_form = document.getElementById("signup form");

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
var password = document.getElementById("password"),
  confirm_password = document.getElementById("confirm_password");

function validatePassword() {
  if (password.value.length <= 5) {
    password.setCustomValidity("Must have a passward of length greater then 5");
    confirm_password.setCustomValidity('');
    return false;
  } else {
    password.setCustomValidity('');
  }

  // does the password satisfy other requirements?

  if (password.value != confirm_password.value) {
    confirm_password.setCustomValidity("Passwords Don't Match");
    return false;
  } else {
    confirm_password.setCustomValidity('');
    return (password.checkValidity() && confirm_password.checkValidity());
  }
}
password.onchange = validatePassword;
confirm_password.onkeyup = validatePassword;

//email confrim
var email = document.getElementById("email"),
  confirm_email = document.getElementById("confirm_email");

function validateEmail() {
  if (email.value != confirm_email.value) {
    confirm_email.setCustomValidity("Email Doesn't Match");
    return false;
  } else {
    confirm_email.setCustomValidity('');
    return (email.checkValidity() && confirm_email.checkValidity());
  }
}

email.onchange = validateEmail;
confirm_email.onkeyup = validateEmail;

// function called when Sign up button is clicked
// if signup is valid then post signup form to web api
function signup() {
  if (!validateUsername())
    return;
  if (!validatePassword())
    return;
  if (!validateEmail())
    return;
  signup_form.submit();
}
