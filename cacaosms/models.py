# -*- coding: utf-8 -*-

from datetime import datetime

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
#from django.utils.translation import ugettext as _

#FIXME: no translations (celery doesn't like them?)
def _(str):
    return str

@python_2_unicode_compatible
class ContactoTipo(models.Model):

    nombre = models.CharField(max_length=100, verbose_name=u"Nombre")


    class Meta:
        ordering = ['nombre',]
        verbose_name = _(u'ContactoTipo')
        verbose_name_plural = _(u'ContactoTipo')


    def __str__(self):
        return "%s " % (self.nombre, )



@python_2_unicode_compatible
class Pais(models.Model):

    nombre = models.CharField(max_length=100, verbose_name=u"Nombre")
    codigo = models.IntegerField(verbose_name=u"Código telefónico")


    class Meta:
        ordering = ['nombre',]
        verbose_name = _(u'Pais')
        verbose_name_plural = _(u'Pais')


    def __str__(self):
        return "%s " % (self.nombre, )



@python_2_unicode_compatible
class Grupo(models.Model):

    nombre = models.CharField(max_length=100, verbose_name=u"Nombre")


    class Meta:
        ordering = ['nombre',]
        verbose_name = _(u'Agrupación')
        verbose_name_plural = _(u'Agrupación')


    def __str__(self):
        return "%s " % (self.nombre, )



@python_2_unicode_compatible
class Bitacora(models.Model):

    de_numero = models.CharField(max_length=32)
    para_numero = models.CharField(max_length=32)
    de = models.CharField(max_length=32, null=True, blank=True)
    para = models.CharField(max_length=32, null=True, blank=True)
    envio_id = models.IntegerField(null=True, blank=True)
    mensaje = models.CharField(max_length=160)
    fecha_envio = models.DateTimeField(auto_now_add=True)
    fecha_resultado = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=64, default='nuevo')
    resultado = models.CharField(max_length=64, null=True, blank=True)


    class Meta:
        ordering = []
        verbose_name = _(u'Bitacora')
        verbose_name_plural = _(u'Bitacora')


    def __str__(self):
        return "%s %s %s " % (self.de, self.para, self.fecha_envio, )



@python_2_unicode_compatible
class Respuesta(models.Model):

    nombre = models.CharField(max_length=32, unique=True)
    mensaje = models.CharField(max_length=160, verbose_name=u"Mensaje de respuesta")
    descripcion = models.CharField(max_length=200, null=True, blank=True)
    is_trivia = models.BooleanField()


    class Meta:
        ordering = ['nombre',]
        verbose_name = _(u'Respuesta')
        verbose_name_plural = _(u'Respuesta')


    def __str__(self):
        return "%s " % (self.nombre, )

    def save(self, force_insert=False, force_update=False):
        self.nombre = self.nombre.lower()
        super(Respuesta, self).save(force_insert, force_update)


@python_2_unicode_compatible
class TriviaEstado(models.Model):

    fecha = models.DateTimeField(auto_now_add=True)
    de = models.CharField(max_length=32, unique=True, verbose_name=u"Número de teléfono")
    respuesta = models.ForeignKey('Respuesta')
    trivia = models.ForeignKey('Trivia', null=True, blank=True)

    class Meta:
        ordering = ['fecha', 'de']
        verbose_name = _(u'Trivia Estado')
        verbose_name_plural = _(u'Trivia Estado')

    def __str__(self):
        return "%s %s" % (self.fecha, self.de, )


@python_2_unicode_compatible
class Trivia(models.Model):

    respuesta = models.ForeignKey(Respuesta)
    nombre = models.CharField(max_length=32, verbose_name=u"Mensaje recibido")
    mensaje = models.CharField(max_length=160, verbose_name=u"Mensaje de respuesta")
    super = models.ForeignKey('self', null=True, blank=True)

    class Meta:
        ordering = ['respuesta','nombre',]
        verbose_name = _(u'Trivia')
        verbose_name_plural = _(u'Trivia')

    def __str__(self):
        return "%s " % (self.nombre, )

    def save(self, force_insert=False, force_update=False):
        self.nombre = self.nombre.lower()
        super(Trivia, self).save(force_insert, force_update)


@python_2_unicode_compatible
class Estado(models.Model):

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()


    class Meta:
        ordering = ['nombre',]
        verbose_name = _(u'Estado de envío')
        verbose_name_plural = _(u'Estado de envío')


    def __str__(self):
        return "%s " % (self.nombre, )



@python_2_unicode_compatible
class Contacto(models.Model):

    nombre = models.CharField(max_length=200, verbose_name=u"Nombre")
    telefono = models.BigIntegerField(verbose_name=u"Teléfono")
    pais = models.ForeignKey(Pais, verbose_name=u"País")
    contactotipo = models.ForeignKey('ContactoTipo', null=True, blank=True, verbose_name=u"Tipo")
    grupo = models.ManyToManyField(Grupo, verbose_name=u"Grupos")
    recibidos = models.IntegerField(null=True, blank=True)


    class Meta:
        ordering = ['nombre',]
        verbose_name = _(u'Contacto')
        verbose_name_plural = _(u'Contacto')


    def __str__(self):
        return "%s %s " % (self.nombre, self.telefono, )

    def _get_full_number(self):
        "Returns the person's full phone number."
        return '+%s%s' % (self.pais.codigo, self.telefono)
    full_number = property(_get_full_number)



@python_2_unicode_compatible
class Mensaje(models.Model):

    nombre = models.CharField(max_length=100)
    mensaje = models.CharField(max_length=160)
    enviados = models.IntegerField(null=True, blank=True)


    class Meta:
        ordering = ['nombre',]
        verbose_name = _(u'Mensaje')
        verbose_name_plural = _(u'Mensaje')


    def __str__(self):
        return "%s " % (self.nombre, )



@python_2_unicode_compatible
class Envios(models.Model):

    de = models.CharField(max_length=100, verbose_name=u"Quién envía")
    para = models.IntegerField(verbose_name=u"Para teléfono específico", null=True, blank=True)
    para_pais = models.ForeignKey(Pais, null=True, blank=True, verbose_name=u"Para todo un país")
    para_contactotipo = models.ForeignKey('ContactoTipo', null=True, blank=True, verbose_name=u"Para todo un tipo de contacto")
    para_contacto = models.ForeignKey(Contacto, null=True, blank=True, verbose_name=u"Para un número específico")
    para_grupo = models.ForeignKey(Grupo, null=True, blank=True, verbose_name=u"Para un grupo")
    texto = models.CharField(max_length=160, null=True, blank=True, verbose_name=u"Mensaje personalizado")
    mensaje = models.ForeignKey(Mensaje, null=True, blank=True, verbose_name=u"Mensaje")
    finalizada = models.DateTimeField(null=True, blank=True, verbose_name=u"Fecha real finalizada")
    programada = models.DateTimeField(verbose_name=u"Fecha programada", default=datetime.now)
    envios_programados = models.IntegerField(null=True, blank=True)
    envios_realizados = models.IntegerField(null=True, blank=True)
    estado = models.CharField(max_length=1, choices=(('N', 'Nuevo'), ('P', 'Programado'), ('S', 'Enviado'), ('I', 'En Proceso'), ('E', 'Error')))


    class Meta:
        ordering = []
        verbose_name = _(u'Envíos')
        verbose_name_plural = _(u'Envíos')


    def __str__(self):
        return "%s " % (self.de, )

    def _get_message(self):
        "Returns the message"
        if self.texto:
            return self.texto
        if self.mensaje:
            return self.mensaje.mensaje
        return '%s' % (self.de)
    message = property(_get_message)


@python_2_unicode_compatible
class Permisos(models.Model):

    nombre = models.CharField(max_length=100, verbose_name=u"Nombre")
    user = models.OneToOneField('users.User')
    pais = models.ManyToManyField(Pais, blank=True, verbose_name=u"Para todo un país")
    contactotipo = models.ManyToManyField(ContactoTipo, blank=True, verbose_name=u"Para todo un tipo de contacto")
    contacto = models.ManyToManyField(Contacto, blank=True, verbose_name=u"Para un número específico")
    grupo = models.ManyToManyField(Grupo, blank=True, verbose_name=u"Para un grupo")


    class Meta:
        ordering = ['nombre',]
        verbose_name = _(u'Permisos')
        verbose_name_plural = _(u'Permisos')


    def __str__(self):
        return "%s : %s" % (self.user, self.nombre, )


@python_2_unicode_compatible
class Backend(models.Model):

    nombre = models.CharField(max_length=100, verbose_name=u"Nombre", primary_key=True)
    descripcion = models.CharField(max_length=256, verbose_name=u"Descripción")
    key = models.CharField(max_length=256, verbose_name=u"Llave",  blank=True, null=True)
    secret = models.CharField(max_length=256, verbose_name=u"Secreto",  blank=True, null=True)
    phone = models.CharField(max_length=256, verbose_name=u"De", blank=True, null=True)
    callback = models.CharField(max_length=256, verbose_name=u"Callback", blank=True, null=True)
    url = models.CharField(max_length=256, verbose_name=u"URL", blank=True, null=True)


    class Meta:
        ordering = ['nombre',]
        verbose_name = _(u'Backend')
        verbose_name_plural = _(u'Backends')


    def __str__(self):
        return self.descripcion


from solo.models import SingletonModel

@python_2_unicode_compatible
class SMSConfiguration(SingletonModel):
    SMSBackend = models.ForeignKey(Backend, null=True)

    def __str__(self):
        return u"Configuración SMS"

    class Meta:
        verbose_name = "Configuración SMS"
