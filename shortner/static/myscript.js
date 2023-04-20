// Copy url to clipboard
function urlCopy(e) {
  const cb = navigator.clipboard;
  const data = document.querySelector(e);
  cb.writeText(data.innerText).then(() => alert("URL copied"));
}

// Save qr-code
function saveQrCode() {
  const img = document.getElementById("embedImage");
  window.location.href = img.src.replace("image/png", "image/octet-stream");
}
