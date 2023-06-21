# URL Shortener App ![GitHub](https://img.shields.io/github/license/zootedb0t/url_shortner) [![CodeQL](https://github.com/zootedb0t/url_shortner/actions/workflows/codeql.yml/badge.svg)](https://github.com/zootedb0t/url_shortner/actions/workflows/codeql.yml) [![Pylint](https://github.com/zootedb0t/url_shortner/actions/workflows/pylint.yml/badge.svg)](https://github.com/zootedb0t/url_shortner/actions/workflows/pylint.yml)

A url-shortner built using flask and Bitly api. It has following dependencies:

- Flask - Core dependency
- SQLAlchemy - For working with database
- requests - For sending GET and POST request
- PyQRCode - For generating QR code of URL

For using bitly api go to [Bitly](https://bitly.com/) website and get a free account to get authentication key and group id. Use these credentials in the applications.

To find out `guid` for your account. Make a GET request to
`https://api-ssl.bitly.com/v4/groups` you can use Postman, Curl, Node or Python request module.

While making request pass your Authorization token to header. In curl you can do this

```
curl \
-H 'Authorization: Bearer {TOKEN}' \
-X GET \
https://api-ssl.bitly.com/v4/groups
```
This returns a json object containing `guid`.
For more [info](https://dev.bitly.com/api-reference/#getGroups)

## Running App Locally
- Clone the repo:
``` 
git clone https://github.com/zootedb0t/url_shortner && cd url_shortner
```
- Create a python virtual environment:
``` 
python -m venv venv
```
- Activate virtual environment:
```
source venv/bin/activate
```
- Install required modules:
```
pip install -r requirements.txt
```
- Run app:
``` 
flask run
```

## App in action

### App home page

![Screenshot_2023-02-09-09-15-41_1920x1080](https://user-images.githubusercontent.com/62596687/217713743-eec20961-bc2d-4bf8-8cfc-c5a548e608de.png)

### Add Api Keys

![Screenshot_2023-02-09-09-18-09_1920x1080](https://user-images.githubusercontent.com/62596687/217714137-37eb9f0f-c7fa-45a5-9e3e-2b1f378593e6.png)

### User database containing urls

![Screenshot_2023-03-24-01-54-00_1920x1080](https://user-images.githubusercontent.com/62596687/227464959-4840ac87-7ebe-48ae-b7aa-4208f9ea0481.png)

### Short-URL generated through api

![Screenshot_2023-03-17-11-46-59_1920x1080](https://user-images.githubusercontent.com/62596687/225827693-0fb0b78b-46ec-4f1b-bfb0-1fa19f24beb1.png)

### Short-URL QR Code

![Screenshot_2023-03-17-11-43-27_1920x1080](https://user-images.githubusercontent.com/62596687/225827304-4635c979-2da5-46fb-98af-a4c94ce7c0a0.png)
