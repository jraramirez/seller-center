function toggleL2(event) {
  var btnID = event.target.className;
  var divID = event.target.getAttribute("aria-controls");
  var level2Buttons = document.getElementsByClassName("btn-level-2");
  var level3Divs = document.getElementsByClassName("level-3");

  for (let l2btn of level2Buttons) {
    if(l2btn.getAttribute("aria-expanded")){
      l2btn.setAttribute("aria-expanded", false)
    }
  }
  for (let div of level3Divs) {
    if(div.id != divID)
    div.classList.remove("show");
  }
}

function toggleL3(event) {
  var btnID = event.target.className;
  var level3Buttons = document.getElementsByClassName("btn-level-3");

  for (let l3btn of level3Buttons) {
    if(l3btn.getAttribute("aria-expanded")){
      l3btn.setAttribute("aria-expanded", false);
    }
  }
}

function showVariation(event, i) {
  event.target.style.display = 'none';
  var nextVariation = document.getElementsByClassName("variation-" + String(i))[0];
  nextVariation.style.display = 'block';
  var id = 'variation-container-' + String(i);
  goToByScroll(id)
}


function goToByScroll(id){
      // Reove "link" from the ID
    id = id.replace("link", "");
      // Scroll
    $('html,body').animate({
        scrollTop: $("#"+id).offset().top},
        '50');
}

function startProgressBar() {
  var files = document.getElementById("id_file").files; 
  f = files[0];
  Papa.parse(f, {
    header: true,
    dynamicTyping: true,
    complete: function(results) {
      data = results;
      var progressBar = document.getElementById("progress-bar"); 
      var progressBarSubtitle = document.getElementById("progress-bar-subtitle"); 
      progressBar.style.display = "block";
      progressBarSubtitle.style.display = "block";
      var width = 0;
      var count = 0;
      var nRows = data.data.length
      if(nRows>=500){
        nRows = 500;
      }
      var id = setInterval(frame, 22);
      function frame() {
        if (count >= nRows) {
          clearInterval(id);
        } 
        else {
          count++;
          width = count/nRows*100
          progressBar.style.width = width + '%'; 
          progressBarSubtitle.innerHTML = count * 1 + ' / '+ String(nRows) + ' rows processed.';
        }
      }
    }
  });
}

$(function(){
    var hash = window.location.hash;
    hash && $('ul.nav a[href="' + hash + '"]').tab('show');

    $('.nav a').click(function (e) {
      $(this).tab('show');
      var scrollmem = $('body').scrollTop();
      window.location.hash = this.hash;
      $('html,body').scrollTop(scrollmem);
    });


  $('textarea').each(function () {
    this.setAttribute('style', 'height:' + (this.scrollHeight) + 'px;overflow-y:hidden;');
  }).on('input', function () {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
  });

    $('.nav-link').click(function(){
        if($(this).attr('id') == 'to-ship-tab' || $(this).attr('id') == 'return-refund-tab'){
            $('.btn-outline-primary').removeClass('active');
            $('#all2').addClass('active');
            $('#process').show();
        } else{
            $('#process').hide();
        }
    });

    $('.custom-file-input').change(function(){
      $('#'+$(this).attr('file_lbl')).text($(this)[0].files[0].name);
    })

    $('#holiday').change(function(){
      if($(this).is(':checked')){
        $('.holiday_date_time').removeAttr('disabled');
      } else{
        $('.holiday_date_time').attr('disabled', 'disabled');
      }
    });
    
    window.onscroll=function(){
      stick_header();
    };
    var header=$('#header_box')[0];
    var sticky=header.offsetTop;

    function stick_header(){
      if(window.pageYOffset > sticky){
        $(header).addClass('sticky');
        $('#fixed_header').css({'top': '0'});
      } else{
        $(header).removeClass('sticky');
        $('#fixed_header').css({'top': '10%'});
      }
    }
});

$('.number_only').keypress(function(e){
  validate_number(e);
});

function validate_number(e){
  var theEvent=e||window.event;
  if(theEvent.type === 'paste'){
      key=event.clipboardData.getData('text/plain');
  } else{
      var key=theEvent.keyCode||theEvent.which;
      key=String.fromCharCode(key);
  }
  var regex=/[0-9]/;
  if(!regex.test(key)){
    theEvent.returnValue=false;
    if(theEvent.preventDefault){
      theEvent.preventDefault();
    }
  }
}