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

function hideVariation(i) {
    var prevIndex = Math.max(0, i - 1);
    var prevAddButton = 'variation-add-button-' + String(prevIndex);
    var id = 'variation-container-' + String(i);
    var prevContainerId = 'variation-container-' + String(prevIndex);
    $("#"+id).hide();
    $("#"+prevAddButton).show();
    goToByScroll(prevContainerId);
}

function showAddress(event, i) {
  event.target.style.display = 'none';
  var nexAddress = document.getElementsByClassName("address-" + String(i))[0];
  nexAddress.style.display = 'block';
  var id = 'address-container-' + String(i);
  goToByScroll(id)
}

function hideAddress(i) {
    var prevIndex = Math.max(0, i - 1);
    var prevAddButton = 'address-add-button-' + String(prevIndex);
    var id = 'address-container-' + String(i);
    var prevContainerId = 'address-container-' + String(prevIndex);
    $("#"+id).hide();
    $("#"+prevAddButton).show();
    goToByScroll(prevContainerId);
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

	$(".custom-file-input").on("change", function(){
		var fileName=$(this).val().split("\\").pop();
		$(this).siblings(".custom-file-label").addClass("selected").html(fileName);
	});
});

$('textarea').each(function () {
  this.setAttribute('style', 'height:' + (this.scrollHeight) + 'px;overflow-y:hidden;');
}).on('input', function () {
  this.style.height = 'auto';
  this.style.height = (this.scrollHeight) + 'px';
});

( function ($) {
    var activenav,
        matches = document.body.className.match(/(^|\s)page-(\w+)(\s|$)/); //
    if (matches) {
        activenav = matches[2];
        $(".navbar-nav .nav-item").each( function () {
            if( $(this).hasClass(activenav) ) {
                $(this).addClass('active')
                       .find(".nav-link").append(" <span class='sr-only'>(current)></span>");
            }
        });
        $(".navbar-nav .dropdown-item").each( function () {
            if( $(this).hasClass(activenav) ) {
                $(this).addClass('active')
                       .append(" <span class='sr-only'>(current)></span>");
            }
        });
    }

})(jQuery);