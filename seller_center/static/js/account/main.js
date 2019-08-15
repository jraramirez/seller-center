$(function(){
    $('#email-login').keyup(function(){
        if($(this).val() != ''){
            $('#verify_user_btn').removeAttr('disabled');
        } else{
            $('#verify_user_btn').attr('disabled', true);
        }
    });

    $('#new_pw').keyup(function(){
        checkSignUpFormComplete();
    });

    $('#repeat_pw').keyup(function(){
        checkSignUpFormComplete();
    });

    $('#show_hide_pw').click(function(){
        show_hide_pw($('#new_pw'), $(this).attr('id'));
    });

    $('#show_hide_repeat_pw').click(function(){
        show_hide_pw($('#repeat_pw'), $(this).attr('id'));
    });

    function checkSignUpFormComplete(){
        var password=$('#new_pw').val();
        var confirmPassword=$('#repeat_pw').val();
        if(password == ''){
            $('.checkPasswordContainer').hide('slow');
        } else{
            $('.checkPasswordContainer').show('slow');
        }
        $('#reset_pw_btn').prop('disabled', !(checkPasswordHelper(password, confirmPassword)));
    }

    function show_hide_pw(el, id){
        pw=el[0];
        show_hide='#'+id;
        if(pw.type === 'password'){
            pw.type='text';
            $(show_hide).text('hide');
        } else{
            pw.type='password';
            $(show_hide).text('show');
        }
    }
});