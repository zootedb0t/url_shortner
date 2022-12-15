function urlCopy(e) {
  const cb = navigator.clipboard;
  const data = document.querySelector(e);
  cb.writeText(data.innerText).then(() => alert("URL copied"));
}

/* Removing flash messages */
function removeFlash() {
  const element = document.getElementById("div_flash");
  element.remove();
}

setTimeout(function() {
  removeFlash();
}, 4000);
