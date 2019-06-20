function validateUsername(username) {
    if (username.value.length <= 0) {
        username.setCustomValidity('Must have a username');
        username.reportValidity();
        return false;
    } else {
        username.setCustomValidity('');
        return true;
    }
}

function validatePassword(password) {
    if (password.value.length < 4) {
        password.setCustomValidity('Must have a password length of at least 4');
        password.reportValidity();
        return false;
    } else {
        password.setCustomValidity('');
        return true;
    }
}

function validateSignupPasswords(password, confirm_password) {
    if (!validatePassword(password)) { return false; }

    // does the password satisfy other requirements?

    if (password.value != confirm_password.value) {
        confirm_password.setCustomValidity('Passwords must match');
        confirm_password.reportValidity();
        return false;
    } else {
        confirm_password.setCustomValidity('');
        return true;
    }
}

function validateSignupEmails(email, confirm_email) {
    if (email.value != confirm_email.value) {
        confirm_email.setCustomValidity('Emails must match');
        confirm_email.reportValidity();
        return false;
    } else {
        confirm_email.setCustomValidity('');
        return true;
    }
}
