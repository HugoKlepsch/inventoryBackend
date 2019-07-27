import { Vue, Component } from 'vue-property-decorator';

@Component
export default class FieldValidators extends Vue {
  public validateAndDisplayHelp(
    inputs: Array<HTMLInputElement | null>,
    helpText: string,
    additionalValidationFunctions?: any[],
  ) {
    for (const input of inputs) {
      if ( input !== null ) {
        input.onchange = () => {
          input.setCustomValidity('');
          input.checkValidity();
          if (additionalValidationFunctions != null && Array.isArray(additionalValidationFunctions)) {
            for (const fn of additionalValidationFunctions) {
              const fnOutput = fn();
              if (fnOutput !== '') {
                input.setCustomValidity(fnOutput);
                break;
              }
            }
          }
        };
        input.oninvalid = () => {
          input.setCustomValidity(helpText);
        };
      }
    }
  }
}
