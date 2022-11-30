function copy() {
  var copy_url = document.getElementById("short_link")
  copy_url.select();
// Copy the text inside the text field
  navigator.clipboard.writeText(copy_url.value);
  // Alert the copied text
  alert("Copied the text: " + copy_url.value);
}
