// Copy url to clipboard
function urlCopy(e) {
  const cb = navigator.clipboard;
  const data = document.querySelector(e);
  cb.writeText(data.innerText).then(() => alert("URL copied"));
}

// Save qr-code
function saveQrCode() {
  window.addEventListener("click", () => {
    const img = document.getElementById("embedImage");

    const button = document.getElementById("saveImg");
    button.addEventListener("click", () => {
      window.location.href = img.src.replace("image/png", "image/octet-stream");
    });
  });
}
