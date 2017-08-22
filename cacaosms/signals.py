from datetime import datetime, timedelta

from django.db.models.signals import post_save
from django.dispatch import receiver

from cacaosms.taskapp.celery import send_sms_task
from cacaosms.models import Envios, Contacto


@receiver(post_save, sender=Envios, dispatch_uid="send_sms_to_queue")
def send_sms_to_queue(sender, instance, **kwargs):

    task = None
    para_list = filter(None, (instance.para, instance.para_contacto, instance.para_contactotipo, instance.para_pais, instance.para_grupo))
    para = ', '.join([str(x) for x in para_list])

    if instance.estado == 'P': # Programado
        when = instance.programada
    else:
        when = datetime.now()

    #
    # send sms to specific users
    #
    if instance.para:
        #task = send_sms.delay(para, instance.message, from_str=instance.de, to_str=para, id_str=instance.pk)
        task = send_sms_task.apply_async((para, instance.message), {'from_str': instance.de, 'to_str': para, 'id_str': instance.pk}, eta=when)

    if instance.para_contacto:
        contact = instance.para_contacto
        #task = send_sms.delay(contact.full_number, instance.message, from_str=instance.de, to_str=para, id_str=instance.pk)
        task = send_sms_task.apply_async((contact.full_number, instance.message), {'from_str': instance.de, 'to_str': para, 'id_str': instance.pk}, eta=when)

    #
    # apply / combine filters
    #
    contacts = Contacto.objects.all()
    if instance.para_contactotipo:
        contacts = Contacto.objects.filter(contactotipo=instance.para_contactotipo)

    if instance.para_pais:
        contacts = contacts.filter(pais=instance.para_pais)

    if instance.para_grupo:
        contacts = contacts.filter(grupo=instance.para_grupo)

    for contact in contacts:
        task = send_sms_task.apply_async((contact.full_number, instance.message), {'from_str': instance.de, 'to_str': para, 'id_str': instance.pk}, eta=when)
