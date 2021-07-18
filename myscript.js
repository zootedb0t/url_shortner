function results() {
  var url = document.getElementById("inputurl").value;
  // document.write(url);
  // document.getElementById(
  //   "shorturl"
  // ).innerHTML = `URL entered by you is ${url}`;
  console.log(url); //For debug
}

var requests = require('request')
var headers = {
  'Authorization': 'c531e773c3ee0a030671198ad503b16e4e214ada',
  'Content-Type' : 'application/json'
};

var dataString = '{ "long_url": url, }'
