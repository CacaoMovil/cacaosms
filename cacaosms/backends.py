

class InvalidSMSBackend(Exception):
    print "Invalid SMS Backend"
    pass


class BaseSMSBackend(object):

    def send_sms(self):
        raise NotImplementedError()


import logging

class DummySMSBackend(object):

    def send_sms(self, phone_number_to, message, from_str=None, to_str=None, id_str=None):
        message = "to=%s, message=%s, from_str=%s, to_str=%s id_str=%s" % (phone_number_to, message, from_str, to_str, id_str)
        logger = logging.getLogger(__name__)
        logger.info(message)


class MensatekSMSBackend(object):

    def __init__(self, username, password, phone_number_from, url):
        self.username = username
        self.password = password
        self.phone_number_from = phone_number_from
        self.url = url

    def send_sms(self, phone_number_to, message, from_str=None, to_str=None, id_str=None):
        from cacaosms.models import Bitacora
        import urllib, urllib2

        if from_str and to_str and id_str:
            entrada = Bitacora(de=from_str, para=to_str, de_numero=self.phone_number_from, para_numero=phone_number_to, envio_id=id_str, mensaje=message)
        else:
            entrada = Bitacora(de_numero=self.phone_number_from, para_numero=phone_number_to, mensaje=message)
        entrada.save()

        values = {'Correo' : self.username,
          'Passwd' : self.password,
          'Remitente' : self.phone_number_from,
          'Destinatarios' : phone_number_to,
          'Mensaje' : message,
          'Resp' : 'JSON' }

        data = urllib.urlencode(values)
        req = urllib2.Request(self.url, data)
        response = urllib2.urlopen(req)
        print response.geturl()
        print response.info()
        respuesta = response.read()
        print respuesta
        return respuesta


class TwilioSMSBackend(object):

    def __init__(self, account_sid, auth_token, phone_number_from, status_callback):
        from twilio.rest import Client
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.phone_number_from = phone_number_from
        self.status_callback = status_callback
        self.client = Client(self.account_sid, self.auth_token)

    def send_sms(self, phone_number_to, message, from_str=None, to_str=None, id_str=None):
        from twilio.rest import Client
        from cacaosms.models import Bitacora

        if from_str and to_str and id_str:
            entrada = Bitacora(de=from_str, para=to_str, de_numero=self.phone_number_from, para_numero=phone_number_to, envio_id=id_str, mensaje=message)
        else:
            entrada = Bitacora(de_numero=self.phone_number_from, para_numero=phone_number_to, mensaje=message)
        entrada.save()
        status_callback = "%s/%s" % (self.status_callback, entrada.id)

        return self.client.messages.create(to=phone_number_to, from_=self.phone_number_from, body=message, status_callback=status_callback)


def get_sms_backend_client():
    from .models import SMSConfiguration
    config = SMSConfiguration.get_solo()
    backend = config.SMSBackend.nombre
    key = config.SMSBackend.key
    secret = config.SMSBackend.secret
    phone = config.SMSBackend.phone
    callback = config.SMSBackend.callback
    url = config.SMSBackend.url


    if backend == 'dummy':
        return DummySMSBackend()

    elif backend  == 'mensatek':
        return MensatekSMSBackend(username=key, password=secret, phone_number_from=phone, url=url)

    elif backend == 'twilio':
        return TwilioSMSBackend(account_sid=key, auth_token=secret, phone_number_from=phone, status_callback=callback)

    else:
        raise InvalidSMSBackend

def send_sms(phone_number_to, message, from_str=None, to_str=None, id_str=None):

    backend = get_sms_backend_client()
    return backend.send_sms(phone_number_to, message, from_str, to_str, id_str)
