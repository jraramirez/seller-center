function readURL(input) {
  if (input.files && input.files[0]) {

    var reader = new FileReader();

    reader.onload = function(e) {
      $('.image-upload-wrap').hide();

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
