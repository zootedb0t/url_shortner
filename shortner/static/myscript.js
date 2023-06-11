// Copy url to clipboard
function urlCopy(e) {
  const cb = navigator.clipboard;
  const data = document.querySelector(e);
  cb.writeText(data.innerText).then(() => alert("URL copied"));
}

// Save qr-code
function saveQr() {
  var link = document.createElement("a");
  const img = document.getElementById("embedImage");
  link.setAttribute("href", img.src);
  link.setAttribute("download", "qr-code");
  link.click();
}
