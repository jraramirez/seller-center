$(function(){
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function(e) {
                $('.image-upload-wrap').hide();
                $('.file-upload-image').attr('src', e.target.result);
                $('.file-upload-content').show();
                $('.image-title').html(input.files[0].name);
            };
            reader.readAsDataURL(input.files[0]);
        } else {
            removeUpload();
        }
    }
    function removeUpload() {
      $('.file-upload-input').replaceWith($('.file-upload-input').clone());
      $('.file-upload-content').hide();
      $('.image-upload-wrap').show();
    }

    $('.image-upload-wrap').bind('dragover', function () {
            $('.image-upload-wrap').addClass('image-dropping');
        });
        $('.image-upload-wrap').bind('dragleave', function () {
            $('.image-upload-wrap').removeClass('image-dropping');
    });

    $('#drop-container').hover(function(){
        $('#rmv_cover_img').css({'opacity': 1})
    }, function(){
        $('#rmv_cover_img').css({'opacity': 0})
    });

    $('#drop-container1').hover(function(){
        $('#rmv_img_1').css({'opacity': 1})
    }, function(){
        $('#rmv_img_1').css({'opacity': 0})
    });

    $('#drop-container2').hover(function(){
        $('#rmv_img_2').css({'opacity': 1})
    }, function(){
        $('#rmv_img_2').css({'opacity': 0})
    });

    $('#drop-container3').hover(function(){
        $('#rmv_img_3').css({'opacity': 1})
    }, function(){
        $('#rmv_img_3').css({'opacity': 0})
    });

    $('#drop-container4').hover(function(){
        $('#rmv_img_4').css({'opacity': 1})
    }, function(){
        $('#rmv_img_4').css({'opacity': 0})
    });

    $('#drop-container5').hover(function(){
        $('#rmv_img_5').css({'opacity': 1})
    }, function(){
        $('#rmv_img_5').css({'opacity': 0})
    });

    $('#rmv_cover_img').click(function(e){
        e.preventDefault();
        remove_img('#cover_img', $(this));
    });

    $('#rmv_img_1').click(function(e){
        e.preventDefault();
        remove_img('#img_1', $(this));
    });

    $('#rmv_img_2').click(function(e){
        e.preventDefault();
        remove_img('#img_2', $(this));
    });

    $('#rmv_img_3').click(function(e){
        e.preventDefault();
        remove_img('#img_3', $(this));
    });

    $('#rmv_img_4').click(function(e){
        e.preventDefault();
        remove_img('#img_4', $(this));
    });

    $('#rmv_img_5').click(function(e){
        e.preventDefault();
        remove_img('#img_5', $(this));
    });

    $('#product_cover_img').change(function(){
        update_img($(this), '#cover_img', '#rmv_cover_img');
    });

    $('#product_img_1').change(function(){
        update_img($(this), '#img_1', '#rmv_img_1');
    });

    $('#product_img_2').change(function(){
        update_img($(this), '#img_2', '#rmv_img_2');
    });

    $('#product_img_3').change(function(){
        update_img($(this), '#img_3', '#rmv_img_3');
    });

    $('#product_img_4').change(function(){
        update_img($(this), '#img_4', '#rmv_img_4');
    });

    $('#product_img_5').change(function(){
        update_img($(this), '#img_5', '#rmv_img_5');
    });

    $(".img_container").on('dragenter', function(e){
        e.preventDefault();
        $(this).css('border', '#39b311 2px dashed');
        $(this).css('background', '#f1ffef');
    });

    $(".img_container").on('dragleave', function(e){
        e.preventDefault();
        $(this).css('border', '#07c6f1 2px dashed');
        $(this).css('background', '#FFF');
    });

    $(".img_container").on('dragover', function(e){
        e.preventDefault();
    });

    $(".img_container").on('drop', function(e){
        e.preventDefault();
        $(this).css('border', '#07c6f1 2px dashed');
        $(this).css('background', '#FFF');
        var found_img='';
        switch($(this).attr('id')){
            case 'drop-container':
                found_img='#product_cover_img';
                $('#cover_img').show();
                $('#rmv_cover_img').show();
                break;
            case 'drop-container1':
                found_img='#product_img_1';
                $('#img_1').show();
                $('#rmv_img_1').show();
                break;
            case 'drop-container2':
                found_img='#product_img_2';
                $('#img_2').show();
                $('#rmv_img_2').show();
                break;
            case 'drop-container3':
                found_img='#product_img_3';
                $('#img_3').show();
                $('#rmv_img_3').show();
                break;
            case 'drop-container4':
                found_img='#product_img_4';
                $('#img_4').show();
                $('#rmv_img_4').show();
                break;
            case 'drop-container5':
                found_img='#product_img_5';
                $('#img_5').show();
                $('#rmv_img_5').show();
                break;
        }
        var image=e.originalEvent.dataTransfer;
        var imgdisplay=$('#'+$(this).find(found_img).attr('imgdisplay'));
        read_img_file(image, imgdisplay);
    });

    function remove_img(img_src, img_rmv){
        $(img_src).attr('src', '');
        $(img_src).hide();
        img_rmv.hide();
    }

    function update_img(img_file, img_src, img_rmv){
        var ctr=1;
        var imgdisplay=$('#'+img_file.attr('imgdisplay'));
        read_img_file(img_file[0], imgdisplay);
        if(ctr == 1 || $(img_src).attr('src')){
            $(img_src).show();
            $(img_rmv).show();
        }
    }

    function read_img_file(input, imgdisplay){
        if (input.files && input.files[0]){
            var reader=new FileReader();
            reader.onload=function(e){
                $(imgdisplay).attr('src', e.target.result).width(170).height(120);
            };
            reader.readAsDataURL(input.files[0]);
        }
    }
});