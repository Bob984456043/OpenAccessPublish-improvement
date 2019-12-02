class Config:
    # csrf config
    CSRF_ENABLED = True
    SECRET_KEY = 'qe4v^trRAVVO7s1R7W46C8@d5ft$HY45gr'

    # sqlalchemy config
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///refer.sqlite3'
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://debian-sys-maint:NGHXnGMNUbaoRjWH@localhost/db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Mail config
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'qwe984456043@163.com'
    MAIL_PASSWORD = 'q984456043'
    MAIL_DEFAULT_SENDER = 'qwe984456043@163.com'

    # upload limit 20M
    MAX_CONTENT_LENGTH = 20000000
