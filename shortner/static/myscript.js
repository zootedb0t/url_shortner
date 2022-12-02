function urlCopy(e) {
  const cb = navigator.clipboard;
  const data = document.querySelector(e)
  cb.writeText(data.innerText).then(() => alert('URL copied'))
}
