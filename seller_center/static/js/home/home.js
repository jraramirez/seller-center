let emailForm = document.querySelector('#email-form');
let phoneForm = document.querySelector('#phone-form');
let showPass = document.querySelector('#show-pass');

let emailLogin = document.querySelector('#email-login');
let emailSpinner = document.querySelector('#email-spinner');
let errorEmailLogin = document.querySelector('#error-email-login');

let passwordLogin = document.querySelector('#password-login');
let errorPasswordLogin = document.querySelector('#error-password-login');

let phoneLogin = document.querySelector('#phone-login');
let phoneSpinner = document.querySelector('#phone-spinner');
let errorPhoneLogin = document.querySelector('#error-phone-login');

let otpLogin = document.querySelector('#otp-login');
let errorOtpLogin = document.querySelector('#error-otp-login');

let passwordReset = document.querySelectorAll('.password-reset');


// const blurFunction = (input, textError, spinner) => {
//     if(input.value === ''){
//         textError.textContent = '';
//         textError.textContent = 'Type your email';
//         spinner.classList.remove('d-flex');
//         spinner.classList.add('d-none');
//     } else {
//         textError.textContent = '';
//         spinner.classList.remove('d-flex');
//         spinner.classList.add('d-none');
//     }
// }

if(emailLogin){
    // emailLogin.addEventListener('onblur', blurFunction(emailLogin, errorEmailLogin, emailSpinner, this.event), false);
    // emailLogin.onblur = blurFunction(emailLogin, errorEmailLogin, emailSpinner);
    emailLogin.addEventListener('blur', function(event){
        event.preventDefault();
        if(emailLogin.value === ''){
            errorEmailLogin.textContent = '';
            errorEmailLogin.textContent = 'Type your email';
            emailSpinner.classList.remove('d-flex');
            emailSpinner.classList.add('d-none');
        } else {
            errorEmailLogin.textContent = '';
            emailSpinner.classList.remove('d-flex');
            emailSpinner.classList.add('d-none');
        }
    });
}

if(passwordLogin){
    passwordLogin.addEventListener('blur', function(e){
        if (passwordLogin.value === '' ){
            errorPasswordLogin.textContent = '';
            errorPasswordLogin.textContent = 'Type your password';
        }
        e.preventDefault();
    });
}

if(phoneLogin){
    phoneLogin.addEventListener('blur', function(e){
        if (phoneLogin.value === '' ){
            errorPhoneLogin.textContent = '';
            errorPhoneLogin.textContent = 'Type your phone number';
            phoneSpinner.classList.remove('d-flex');
            phoneSpinner.classList.add('d-none');
        }
        e.preventDefault();
    });
}

if(otpLogin){
    otpLogin.addEventListener('blur', function(e){
        if (otpLogin.value === '' ){
            errorOtpLogin.textContent = '';
            errorOtpLogin.textContent = 'Type your OTP';
        }
        e.preventDefault();
    });
}

if(showPass){
    showPass.addEventListener('click', function(e){
        e.preventDefault();

        if(passwordLogin){
            if(passwordLogin.type === 'text'){
                passwordLogin.type = 'password';
            } else {
                passwordLogin.type = 'text';
            }
        }

        console.log(passwordReset);
        if(passwordReset){
            passwordReset.forEach((element) => {
                if (element.type === 'text') {
                    element.type = 'password';
                } else {
                    element.type = 'text';
                }
            });
        }
    });
}