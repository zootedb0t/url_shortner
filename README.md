# URL Shortener App

A url-shortner built using flask and Bitly api. It has following dependencies:

- Flask - Core dependency
- SQLAlchemy - For working with database
- requests - For sending GET and POST request
- PyQRCode - For generating QR code of URL

For using bitly api go to [Bitly](https://bitly.com/) website and get a free account to get authentication key and group id. Use these credentials in the applications.

To find out group_guid for your account. Make a GET request to
`https://api-ssl.bitly.com/v4/groups` you can use Postman, Curl, Node or Python request module.

While making request pass your Authorization token to header. In curl you can do this

```
curl \
-H 'Authorization: Bearer {TOKEN}' \
-X GET \
https://api-ssl.bitly.com/v4/groups
```

For more [info](https://dev.bitly.com/api-reference/#getGroups)

## Running App Locally
- Clone the repo `git clone https://github.com/zootedb0t/url_shortner && cd url_shortner`.
- Create a python virtual environment using `python -m venv venv`.
- Install required modules `pip install -r requirements.txt`.
- Run app using `flask run`

## App in action

### App home page

![Screenshot_2023-02-09-09-15-41_1920x1080](https://user-images.githubusercontent.com/62596687/217713743-eec20961-bc2d-4bf8-8cfc-c5a548e608de.png)

### Add Api Keys

![Screenshot_2023-02-09-09-18-09_1920x1080](https://user-images.githubusercontent.com/62596687/217714137-37eb9f0f-c7fa-45a5-9e3e-2b1f378593e6.png)

### User database containing urls

![Screenshot_2023-02-09-09-16-26_1920x1080](https://user-images.githubusercontent.com/62596687/217713936-6fb3137f-c4c5-46ec-a2d9-16a16fa2c8c4.png)

### Short-URL generated through api

![short_url](https://user-images.githubusercontent.com/62596687/213624495-397bd74b-41bc-4e3b-8a13-06681c1aa7e8.png)

### Short-URL QR Code
![Screenshot_2023-02-09-09-17-06_1920x1080](https://user-images.githubusercontent.com/62596687/217714025-910f286e-ecf2-4557-9d42-339e66724014.png)
