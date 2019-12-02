# Open access publishing service
## Python Flask
### Depending:
* python3
* flask
* flask-wtf
* flask-sqlalchemy
* flask-mail
* flask-login
* flask-uploads
* pillow

### [Project address:http://jinmingyi.xin:8080](http://jinmingyi.xin:8080 "abc")

### Function Implemented:
* #### Email
1. Users should ***validate*** their email address before publish and comment.
2. Server will send email to ***validate*** and ***notificate*** user about their action such as publishing and making comment.
3. **_Bad users will be banned_** by email.
* #### Publishing
1. Upload a pdf file to publish an article **_with a validated email_**
* #### Searching
1. Users can search articles by title, subject, author, email.
* #### Reading Article
1. People can see information and download the pdf file.
* #### Comment
1. Make a comment **_with a validated email address_** under an article.
* #### Vote
1. Users can vote up or down to an article or a comment.
2. Each ip address can **_only vote once_** to an article or a comment.
* #### Other
1. Bad Ip address will be banned to access the website.