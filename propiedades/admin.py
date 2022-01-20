from django.contrib import admin
# Register your models here.
from django.utils.html import mark_safe
from .models import FotosPropiedad, TipoPropiedad,Propiedad


@admin.register(TipoPropiedad)
class TipoPropiedadAdmin(admin.ModelAdmin):
    list_display = ('name', 'usado_por')

    def usado_por(self, obj):
        return obj.Propiedades.count()


class FotosEnLinea(admin.TabularInline):
    model = FotosPropiedad


@admin.register(Propiedad)
class PropiedadAdmin(admin.ModelAdmin):
    """Room Admin Definition"""
    inlines = (FotosEnLinea, )
    fieldsets = (
        (
            "Informacion Basica",
            {"fields": ("nombre", "descripcion", "pais",
                        "ciudad", "direccion", "precio")}
        ),
        (
            "Espacio",
            {"fields": ("numMaxHuspedes", "numCuartos", "numCamas"), }
        ),
        (
            "Comodidades",
            {"fields": ("permiteMascotas", "conEstacionamiento", "conCocina",
                        "conSala", "conLavanderia", "conTvCable"), }
        ),
        (
            "Otroas Comodidades",
            {"fields": ("otrasComodidades",), }
        ),

    )
    raw_id_fields = ("host",)
    list_display = (
        'nombre', 'pais', 'ciudad', 'precio', 'numMaxHuspedes', 'numCamas', 'numCuartos', 'numBano', 'count_fotos','host')
    list_filter = ('ciudad', 'tipoPropiedad',
        'pais',)
    search_fields = ['ciudad', '^host__username']
    # filter_horizontal = ('conInternet  ',)
    ordering = ('nombre', 'precio',)

    # def count_amenities(self, obj):
    #     return obj.amenities.count()

    def count_fotos(self, obj):
        return obj.fotos.count()

    # count_amenities.short_descripcion = 'amenities'
    count_fotos.short_descripcion = 'fotos'


@admin.register(FotosPropiedad)
class FotosPropiedadAdmin(admin.ModelAdmin):
    """Photo Admin Definition"""
    list_display = ('__str__', 'get_thumbnail',)
    def get_thumbnail(self, obj):
        return mark_safe(f'<image src="{obj.archivo.url}" width="50px"/>')
    get_thumbnail.short_descripcion = 'Thumbnail'
