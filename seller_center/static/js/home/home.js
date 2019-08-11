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



 if(showPass){
     showPass.addEventListener('click', function(e){
         e.preventDefault();

         if(passwordLogin){
             if(passwordLogin.type === 'text'){
             showPass.value = 'show'

             showPass.text = 'show'
                 passwordLogin.type = 'password';
             } else {
                showPass.value = 'hide'
             showPass.text = 'hide'
                 passwordLogin.type = 'text';
             }
         }

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