import datetime
from firebase_admin import exceptions
from firebase_admin import messaging
from firebase_admin.messaging import WebpushNotification, WebpushFCMOptions
from django.conf import settings


class FCMBeam(object):
    def __init__(self, title, message, type, user_id=None, event_id=None, thumbnail=None, obj=None):
        self.title = title
        self.message = message
        self.type = type
        self.user_id = user_id
        self.event_id = event_id
        self.thumbnail = thumbnail
        self.obj = obj


def notification_setup(title, subtitle, thumb=None):
    android = messaging.AndroidConfig(
        ttl=datetime.timedelta(seconds=3600),
        priority='high',
        notification=messaging.AndroidNotification(title=title,
                                                   body=subtitle,
                                                   image=str(thumb) if thumb else None)
    )
    apns = messaging.APNSConfig(
        headers={"apns-priority": "10"},
        payload=messaging.APNSPayload(aps=messaging.Aps(content_available=True,
                                                        sound='default',
                                                        alert=messaging.ApsAlert(title=title,
                                                                                 body=subtitle,
                                                                                 launch_image=str(
                                                                                     thumb) if thumb else None))))
    webpush = messaging.WebpushConfig(
        notification=WebpushNotification(title=title, body=subtitle, icon=str(thumb) if thumb else None),
        fcm_options=WebpushFCMOptions(link='https://www.google.com/'))
    return android, apns, webpush


def fcm_send_single(data):
    android, apns, webpush = notification_setup(data.title, data.message, data.thumbnail)
    message = messaging.Message(
        android=android,
        apns=apns,
        webpush=webpush,
        data=data.__dict__,
    )
    print(data.__dict__)
    try:
        response = messaging.send(message)
        print(f'{response} messages were sent successfully')
    except exceptions.FirebaseError as ex:
        print('fcm error single', str(ex))
    except Exception as e:
        print('fcm error exception', str(e))
