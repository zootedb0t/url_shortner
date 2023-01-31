# URL Shortener App

A url-shortner built using flask and Bitly api. It has following dependencies:

* Flask - Core dependency
* SQLAlchemy - For working with database
* requests - For sending GET and POST request
* PyQRCode - For generating QR code of URL

For using bitly api go to [Bitly](https://bitly.com/) 
website and get a free account to get authentication key and group id. Use these credentials in the applications. Create a file for storing these api keys
and add that to gitignore for privacy.

To find out group_guid for your account. Make a GET request to
`https://api-ssl.bitly.com/v4/` you can use Postman, Curl, Node or Python request module.

While making request pass your Authorization token to header. In curl you can do this

```
curl \
-H 'Authorization: Bearer {TOKEN}' \
-X GET \
https://api-ssl.bitly.com/v4/
```
For more [info](https://dev.bitly.com/api-reference/#getGroups)

If you don't want to modify code then make a file `api.py` and put your **Authorization** and **group_guid** in it like
```
Authorization="your authentication key"
group_guid="your group_guid key"
```

## App in action

### App home page
![home](https://user-images.githubusercontent.com/62596687/213624221-bba14f00-35dd-4381-820d-adfa641485a6.png)

### User database containing urls
![database](https://user-images.githubusercontent.com/62596687/213624333-9453182c-7081-42b0-abe0-c6e26ad26370.png)

### Short-URL generated through api
![short_url](https://user-images.githubusercontent.com/62596687/213624495-397bd74b-41bc-4e3b-8a13-06681c1aa7e8.png)

### Short-URL QR Code
![qrcode](https://user-images.githubusercontent.com/62596687/213624400-816bd8a3-d673-4d5d-8b15-016a56c1d020.png)
