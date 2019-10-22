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

$('#id_file').change(function() {
  var file = $('#id_file')[0].files[0].name;
  console.log(file);
  $('#id_file_label').text(file);
});

$(function(){
    $('#birthday').datepicker({
      dateFormat: 'yy-mm-dd',
      onSelect: function(birthday){
        var bday_split=birthday.split('-');
        var bday_obj=new Date(bday_split[0] + '-' + bday_split[1] + '-' + bday_split[2]);
        var date_today=new Date();
        var checker=true;
        if((date_today.getFullYear() - bday_obj.getFullYear()) < 18){
          checker=false;
        }
        if(date_today.getFullYear() - bday_obj.getFullYear() == 18){
          if(date_today.getMonth() < bday_obj.getMonth()){
            checker=false;
          }
          if(date_today.getMonth() == bday_obj.getMonth()){
            if(date_today.getDate() < bday_obj.getDate()){
              checker=false;
            }
          }
        }
        if(!checker){
          $(this).val('');
          alert('Invalid birthday. 18 years old and above only.');
        }
      }
    });

    // validate date
    var dateToday = new Date();
    var prod_dates = $("#product_start_date, #product_end_date").datepicker({
        dateFormat: 'yy-mm-dd',
        defaultDate: "+1w",
        changeMonth: true,
        numberOfMonths: 1,
        minDate: dateToday,
        onSelect: function(selectedDate) {
            var option = this.id == "product_start_date" ? "minDate" : "maxDate",
                instance = $(this).data("datepicker"),
                date = $.datepicker.parseDate(instance.settings.dateFormat || $.datepicker._defaults.dateFormat, selectedDate, instance.settings);
            prod_dates.not(this).datepicker("option", option, date);
        }
    });

    var var_dates = $("#variation_start_date, #variation_end_date").datepicker({
        dateFormat: 'yy-mm-dd',
        defaultDate: "+1w",
        changeMonth: true,
        numberOfMonths: 1,
        minDate: dateToday,
        onSelect: function(selectedDate) {
            var option = this.id == "variation_start_date" ? "minDate" : "maxDate",
                instance = $(this).data("datepicker"),
                date = $.datepicker.parseDate(instance.settings.dateFormat || $.datepicker._defaults.dateFormat, selectedDate, instance.settings);
            var_dates.not(this).datepicker("option", option, date);
        }
    });

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

    // $('.nav-link').click(function(){
    //     if($(this).attr('id') == 'to-ship-tab' || $(this).attr('id') == 'return-refund-tab'){
    //         $('.btn-outline-primary').removeClass('active');
    //         $('#all2').addClass('active');
    //         $('#process').show();
    //     } else{
    //         $('#process').hide();
    //     }
    // });

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
  validate_input(e, 'number_only');
});

$('.number_n_spec_char_only').keypress(function(e){
  validate_input(e, 'number_n_spec_char_only');
});

$('.alpha_n_number_only').keypress(function(e){
  validate_input(e, 'alpha_n_number_only');
});

function validate_input(e, type){
  var theEvent=e||window.event;
  if(theEvent.type === 'paste'){
      key=event.clipboardData.getData('text/plain');
  } else{
      var key=theEvent.keyCode||theEvent.which;
      key=String.fromCharCode(key);
  }
  var regex=/[*]/;
  if(type == 'number_only'){
    regex=/[0-9]/;
  } else if(type == 'number_n_spec_char_only'){
    regex=/[0-9]|\W|_/;
  } else if(type == 'alpha_n_number_only'){
    regex=/^[a-z0-9]+$/i;
  }
  if(!regex.test(key)){
    theEvent.returnValue=false;
    if(theEvent.preventDefault){
      theEvent.preventDefault();
    }
  }
}

var placeSearch, autocomplete, autocomplete1;

var componentForm = {
  street_number: 'short_name',
  route: 'long_name',
  locality: 'long_name',
  administrative_area_level_1: 'short_name',
  country: 'long_name',
  postal_code: 'short_name',
  street_number_1: 'short_name',
  route_1: 'long_name',
  locality_1: 'long_name',
  administrative_area_level_1_1: 'short_name',
  country_1: 'long_name',
  postal_code_1: 'short_name'
};
var componentForm1 = {
  street_number_1: 'short_name',
  route_1: 'long_name',
  locality_1: 'long_name',
  administrative_area_level_1_1: 'short_name',
  country_1: 'long_name',
  postal_code_1: 'short_name'
};

function initAutocomplete() {
  // Create the autocomplete object, restricting the search predictions to
  // geographical location types.
  autocomplete = new google.maps.places.Autocomplete(
      document.getElementById('autocomplete'), {types: ['geocode']});
  autocomplete1 = new google.maps.places.Autocomplete(document.getElementById('autocomplete1'), {types: ['geocode']});
  // Avoid paying for data that you don't need by restricting the set of
  // place fields that are returned to just the address components.
  autocomplete.setFields(['address_component']);
  autocomplete1.setFields(['address_component']);
  // When the user selects an address from the drop-down, populate the
  // address fields in the form.
  autocomplete.addListener('place_changed', fillInAddress);
  autocomplete1.addListener('place_changed', fillInAddress);
}

function fillInAddress() {
  // Get the place details from the autocomplete object.
  var place = autocomplete.getPlace();
  var place1 = autocomplete1.getPlace();

  // Get each component of the address from the place details,
  // and then fill-in the corresponding field on the form.
  if(typeof place !== 'undefined'){
    for (var component in componentForm) {
      document.getElementById(component).value = '';
      document.getElementById(component).disabled = false;
    }
    for (var i = 0; i < place.address_components.length; i++) {
      var addressType = place.address_components[i].types[0];
      if (componentForm[addressType]) {
        var val = place.address_components[i][componentForm[addressType]];
        document.getElementById(addressType).value = val;
      }
    }
  }
  if(typeof place1 !== 'undefined'){
    for (var component in componentForm1) {
      document.getElementById(component).value = '';
      document.getElementById(component).disabled = false;
    }
    for (var i = 0; i < place1.address_components.length; i++) {
      var addressType = place1.address_components[i].types[0]+'_1';
      if (componentForm1[addressType]) {
        var val = place1.address_components[i][componentForm1[addressType]];
        document.getElementById(addressType).value = val;
      }
    }
  }
}

// Bias the autocomplete object to the user's geographical location,
// as supplied by the browser's 'navigator.geolocation' object.
function geolocate() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      var geolocation = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
      };
      var circle = new google.maps.Circle(
          {center: geolocation, radius: position.coords.accuracy});
      autocomplete.setBounds(circle.getBounds());
      autocomplete1.setBounds(circle.getBounds());
    });
  }
}