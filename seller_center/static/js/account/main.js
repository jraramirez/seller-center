$(function(){
    $('#email-login').keyup(function(){
        if($(this).val() != ''){
            $('#verify_user_btn').removeAttr('disabled');
            $('#verify_user_btn').removeClass('disabled');
        } else{
            $('#verify_user_btn').attr('disabled', true);
            $('#verify_user_btn').addClass('disabled');
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
        var veri_code=$('#veri_code').val();
        var password=$('#new_pw').val();
        var confirmPassword=$('#repeat_pw').val();
        if(password == ''){
            $('.checkPasswordContainer').hide('slow');
        } else{
            $('.checkPasswordContainer').show('slow');
        }
        $('#reset_pw_btn').prop('disabled', !(checkPasswordHelper(password, confirmPassword)));
        if(veri_code != '' && checkPasswordHelper(password, confirmPassword)){
            $('#reset_pw_btn').removeClass('disabled');
        } else{
            $('#reset_pw_btn').addClass('disabled');
        }
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