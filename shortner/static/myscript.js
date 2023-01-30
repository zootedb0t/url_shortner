function urlCopy(e) {
  const cb = navigator.clipboard;
  const data = document.querySelector(e);
  cb.writeText(data.innerText).then(() => alert("URL copied"));
}

function copyfromdatabase(vars) {
  // var dummy = document.createElement("textarea");
  // to avoid breaking orgain page when copying more words
  // cant copy when adding below this code
  // dummy.style.display = 'none'
  // document.body.appendChild(dummy);
  //Be careful if you use texarea. setAttribute('value', value), which works with "input" does not work with "textarea". – Eduard
  // dummy.value = text;
  // dummy.select();
  // navigator.clipboard.writeText(vars);
  // document.body.removeChild(dummy);
  console.log(vars)
}
