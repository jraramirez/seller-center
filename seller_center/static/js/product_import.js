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

    max_var=20;
    for(i=0; i<max_var; i++){
        var el='#prod_var_'+i+'_img';
        var rmv_el='#rmv_prod_var_'+i+'_img'
        if($(el).attr('src') != ''){
            $(el).show();
            $(rmv_el).show();
        }
    }

    $('.trash_can').click(function(e){
        e.preventDefault();
        remove_img('#'+$(this).attr('rmv_img'), '#'+$(this).attr('id'));
    });

    $('.img_file').change(function(){
        update_img($('#'+$(this).attr('id')), '#'+$(this).attr('imgdisplay'), '#'+$(this).attr('img_rmv'));
    });

    $(".img_container").on('dragenter', function(e){
        e.preventDefault();
        $(this).css('border', '#39b311 1px dashed');
        $(this).css('background', '#f1ffef');
    });

    $(".img_container").on('dragleave', function(e){
        e.preventDefault();
        $(this).css('border', '#07c6f1 1px dashed');
        $(this).css('background', '#FFF');
    });

    $(".img_container").on('dragover', function(e){
        e.preventDefault();
    });

    $(".img_container").on('drop', function(e){
        e.preventDefault();
        $(this).css('border', '#07c6f1 1px dashed');
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
            case 'var-drop-container':
                ctr=$(this).attr('var_ctr');
                found_img='#product-variation-'+ctr+'-image';
                $('#prod_var_'+ctr+'_img').show();
                $('#rmv_prod_var_'+ctr+'_img').show();
                break;
        }
        $(found_img).prop('files', e.originalEvent.dataTransfer.files);
        var image=e.originalEvent.dataTransfer;
        var imgdisplay=$('#'+$(this).find(found_img).attr('imgdisplay'));
        read_img_file(image, imgdisplay);
    });

    function remove_img(img_src, img_rmv){
        $(img_src).attr('src', '');
        $(img_src).hide();
        $(img_rmv).hide();
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
                $(imgdisplay).attr('src', e.target.result);
            };
            reader.readAsDataURL(input.files[0]);
        }
    }
});
