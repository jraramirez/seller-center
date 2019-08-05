
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
