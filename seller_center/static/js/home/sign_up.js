
function checkPasswordHelper(password, confirmPassword) {
var passwordPolicy = [];
        passwordPolicy.lowercase = "Password must contain a lower case letter";
        passwordPolicy.uppercase = "Password must contain an upper case letter";
        passwordPolicy.number = "Password must contain a number";
        passwordPolicy.special = "Password must contain a special character";
        var passwordLength = 8;
        passwordPolicy.lengthCheck = "Password must contain at least 8 characters";
        passwordPolicy.match = "Password and Confirm Password must match";


        var requireLowerletter = false;
        var requireUpperletter = false;
        var requireNumber = false;
        var requireSymbol = false;
        var requireLength = false;
        var requireMatch = false;

        if (password) {
            if (true) {
                if (/[a-z]/.test(password)) {
                    $(".check-lowerletter").html("&#10003;");
                    $(".checkPasswordText-lowerletter").html(passwordPolicy.lowercase);
                    $(".checkPassword-lowerletter").addClass("passwordCheck-valid-customizable").removeClass(
                        "passwordCheck-notValid-customizable");
                    requireLowerletter = true;
                } else {
                    $(".check-lowerletter").html("&#10006;");
                    $(".checkPasswordText-lowerletter").html(passwordPolicy.lowercase);
                    $(".checkPassword-lowerletter").addClass("passwordCheck-notValid-customizable").removeClass(
                        "passwordCheck-valid-customizable");
                    requireLowerletter = false;
                }
            } else {
                requireLowerletter = true;
            }
            if (true) {
                if (/[A-Z]/.test(password)) {
                    $(".check-upperletter").html("&#10003;");
                    $(".checkPasswordText-upperletter").html(passwordPolicy.uppercase);
                    $(".checkPassword-upperletter").addClass("passwordCheck-valid-customizable").removeClass(
                        "passwordCheck-notValid-customizable");
                    requireUpperletter = true;
                } else {
                    $(".check-upperletter").html("&#10006;");
                    $(".checkPasswordText-upperletter").html(passwordPolicy.uppercase);
                    $(".checkPassword-upperletter").addClass("passwordCheck-notValid-customizable").removeClass(
                        "passwordCheck-valid-customizable");
                    requireUpperletter = false;
                }
            } else {
                requireUpperletter = true;
            }
            if (true) {
                if (/[-!$%^&*()_|~`{}\[\]:\/;<>?,.@#'"]/.test(password) || password.indexOf('\\') >= 0) {
                    $(".check-symbols").html("&#10003;");
                    $(".checkPasswordText-symbols").html(passwordPolicy.special);
                    $(".checkPassword-symbols").addClass("passwordCheck-valid-customizable").removeClass(
                        "passwordCheck-notValid-customizable");
                    requireSymbol = true;
                } else {
                    $(".check-symbols").html("&#10006;");
                    $(".checkPasswordText-symbols").html(passwordPolicy.special);
                    $(".checkPassword-symbols").addClass("passwordCheck-notValid-customizable").removeClass(
                        "passwordCheck-valid-customizable");
                    requireSymbol = false;
                }
            } else {
                requireSymbol = true;
            }
            if (true) {
                if (/[0-9]/.test(password)) {
                    $(".check-numbers").html("&#10003;");
                    $(".checkPasswordText-numbers").html(passwordPolicy.number);
                    $(".checkPassword-numbers").addClass("passwordCheck-valid-customizable").removeClass(
                        "passwordCheck-notValid-customizable")
                    requireNumber = true;
                } else {
                    $(".check-numbers").html("&#10006;");
                    $(".checkPasswordText-numbers").html(passwordPolicy.number);
                    $(".checkPassword-numbers").addClass("passwordCheck-notValid-customizable").removeClass(
                        "passwordCheck-valid-customizable");
                    requireNumber = false;
                }
            } else {
                requireNumber = true;
            }

            if (password.length < passwordLength) {
                $(".check-length").html("&#10006;");
                $(".checkPasswordText-length").html(passwordPolicy.lengthCheck);
                $(".checkPassword-length").addClass("passwordCheck-notValid-customizable").removeClass(
                    "passwordCheck-valid-customizable");
                requireLength = false;
            } else {
                $(".check-length").html("&#10003;");
                $(".checkPasswordText-length").html(passwordPolicy.lengthCheck);
                $(".checkPassword-length").addClass("passwordCheck-valid-customizable").removeClass(
                    "passwordCheck-notValid-customizable");
                requireLength = true;
            }


            if (password !== confirmPassword) {
                $(".check-match").html("&#10006;");
                $(".checkPasswordText-match").html(passwordPolicy.match);
                $(".checkPassword-match").addClass("passwordCheck-notValid-customizable").removeClass(
                    "passwordCheck-valid-customizable");
                requireMatch = false;
            } else {
                $(".check-match").html("&#10003;");
                $(".checkPasswordText-match").html(passwordPolicy.match);
                $(".checkPassword-match").addClass("passwordCheck-valid-customizable").removeClass(
                    "passwordCheck-notValid-customizable");
                requireMatch = true;
            }
        }

        return requireLowerletter && requireUpperletter && requireNumber && requireSymbol && requireLength && requireMatch;

}

function isEmail(email) {
    var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,6})?$/;
    return regex.test(emailReg);
}

function checkSignUpFormComplete() {
//  if username, password, confirm password and terms is checked enable button

    var username_input = $('input[name="username"]').val() != "";
    var password = $('input[name="password"]').val();
    var confirmPassword = $('input[name="confirm-password"]').val();
    var terms = $('#checkboxTerms').checked;



    if (password == "") {
        $('.checkPasswordContainer').hide("slow");
    } else {
        $('.checkPasswordContainer').show("slow");
    }

    $('button[name="signUpButton"]').prop("disabled", !(checkPasswordHelper(password, confirmPassword) && username_input && terms));
}

function checkPasswordMatch() {
    var username_input = $('input[name="username"]').val() != "";
    var password = $('input[name="password"]').val();
    var confirmPassword = $('input[name="confirm-password"]').val();

    $('button[name="signUpButton"]').prop("disabled", !(checkPasswordHelper(password) && username_input));
}

function checkConfirmForgotPasswordMatch() {
    var password = $('#new_password').val()
    $('button[name="reset_password"]').prop("disabled",!(checkPasswordHelper(password) && password === $('#confirm-password').val()));
}