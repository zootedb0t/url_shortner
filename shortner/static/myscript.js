// WIP copy url to database
getrow = function(val) {
  db.transaction(function(transaction) {
    transaction.executeSql("SELECT * FROM url where id =" + parseInt(val, 10)) +
      ";";
  });
};

function urlCopy(e) {
  const cb = navigator.clipboard;
  const data = document.querySelector(e);
  cb.writeText(data.innerText).then(() => alert("URL copied"));
}
