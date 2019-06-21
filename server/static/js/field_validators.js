function validateAndDisplayHelp(inputs, help_text, additional_validation_functions) {
    for (const input of inputs) {
        input.oninput = function() {
            input.setCustomValidity('');
            input.checkValidity();
            if (additional_validation_functions != null && Array.isArray(additional_validation_functions)) {
                for (const fn of additional_validation_functions) {
                    var fn_output = fn();
                    if (fn_output !== '') {
                        input.setCustomValidity(fn_output);
                        break;
                    }
                }
            }
        }
        input.oninvalid = function() {
            input.setCustomValidity(help_text);
        }
    }
}

function checkValidityInputsSameValue(input_a, input_b, input_name) {
    if (input_a.value != input_b.value) {
        return input_name + 's must match';
    } else {
        return '';
    }
}
