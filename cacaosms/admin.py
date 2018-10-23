# -*- coding: utf-8 -*-

from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from .models import *


class ContactoInline(admin.TabularInline):
    model = Contacto.grupo.through



admin.site.register(ContactoTipo)




class PaisAdmin(admin.ModelAdmin):
    list_display = ['nombre','codigo',]

    search_fields = ['nombre',]



    #inlines = [
    #    ContactoInline,
    #]


admin.site.register(Pais, PaisAdmin)




class GrupoAdmin(admin.ModelAdmin):
    list_display = ['nombre',]
    list_filter = ('nombre',)




    inlines = [
        ContactoInline,
    ]


admin.site.register(Grupo, GrupoAdmin)




from django.db.models.functions import Trunc
from django.db.models import DateTimeField

class BitacoraAdmin(admin.ModelAdmin):
    list_display = ['de','para','mensaje','fecha_envio',]
    list_filter = ('de','para','fecha_envio',)
    readonly_fields = ('fecha_envio',)

    def changelist_view(self, request, extra_context=None):
        summary_over_time = qs.annotate(
            period=Trunc(
                'created',
                'day',
                output_field=DateTimeField(),
            ),
        ).values('period').annotate(total=Sum('price')).order_by('period')
        summary_range = summary_over_time.aggregate(
            low=Min('total'),
            high=Max('total'),
        )
        high = summary_range.get('high', 0)
        low = summary_range.get('low', 0)
        response.context_data['summary_over_time'] = [{
            'period': x['period'],
            'total': x['total'] or 0,
            'pct': \
               ((x['total'] or 0) - low) / (high - low) * 100 
               if high > low else 0,
        } for x in summary_over_time]
        return response
admin.site.register(Bitacora, BitacoraAdmin)




class RespuestaAdmin(admin.ModelAdmin):
    list_display = ['nombre','mensaje',]






admin.site.register(Respuesta, RespuestaAdmin)




class TriviaAdmin(admin.ModelAdmin):
    list_display = ['nombre',]

admin.site.register(Trivia, TriviaAdmin)




admin.site.register(TriviaEstado)

admin.site.register(Estado)




class ContactoAdmin(ImportExportModelAdmin):
    list_display = ['nombre','telefono','pais','contactotipo',]
    list_filter = ('pais','contactotipo','grupo',)
    search_fields = ['nombre','telefono',]

    list_per_page = 100


admin.site.register(Contacto, ContactoAdmin)




class MensajeAdmin(admin.ModelAdmin):
    list_display = ['nombre','mensaje',]






admin.site.register(Mensaje, MensajeAdmin)



class EnviosAdmin(admin.ModelAdmin):
    list_display = ['de','texto','mensaje',]
    list_filter = ('de',)
    readonly_fields = ('finalizada','envios_programados','envios_realizados',)

    # Restringe destinatarios según "Permisos" (para non-supers)
    def render_change_form(self, request, context, *args, **kwargs):
        if not request.user.is_superuser:
            try:
                permisos = request.user.permisos
                context['adminform'].form.fields['para_pais'].queryset = permisos.pais.all()
                context['adminform'].form.fields['para_contactotipo'].queryset = permisos.contactotipo.all()
                context['adminform'].form.fields['para_contacto'].queryset = permisos.contacto.all()
                context['adminform'].form.fields['para_grupo'].queryset = permisos.grupo.all()
            except Permisos.DoesNotExist:
                # FIXME raise Error
                print "No Permisos"
        return super(EnviosAdmin, self).render_change_form(request, context, *args, **kwargs)

admin.site.register(Envios, EnviosAdmin)



class PermisosAdmin(admin.ModelAdmin):
    list_display = ['nombre','user',]

admin.site.register(Permisos, PermisosAdmin)


class BackendAdmin(admin.ModelAdmin):
    list_display = ['nombre','descripcion',]

admin.site.register(Backend, BackendAdmin)


# SMS Configuration using django-solo
from solo.admin import SingletonModelAdmin
admin.site.register(SMSConfiguration, SingletonModelAdmin)
