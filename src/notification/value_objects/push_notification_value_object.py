class PushNotificationValueObject():
    def __init__(self, body: str, title: str = ''):
        self.title = title
        self.body = body
