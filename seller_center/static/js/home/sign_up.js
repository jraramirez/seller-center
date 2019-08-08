function enableSignUpButton() {
  var username = document.getElementById("username").value;
  var password = document.getElementById("password").value;
  var reenterPassword = document.getElementById("reenter-password").value;
  var signUpButton = document.getElementById("signup");
  var checkboxTerms = document.getElementById("checkboxTerms");

  if (username.length > 0 && password.length > 0 && reenterPassword.length > 0 && checkboxTerms.checked == true) {
    signUpButton.disabled = false;
  } else {
    signUpButton.disabled = true;
  }
}