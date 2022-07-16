from wagtail.contrib.modeladmin.options import (
    modeladmin_register,
    ModelAdmin,
    ModelAdminGroup,
)
from .models import Sample


class SampleAdmin(ModelAdmin):
    model = Sample
    menu_label = "Sample"
    menu_icon = "fa-folder"
    ordering = []
    menu_order = 1
    list_display = ("title",)
    search_fields = ("title",)
    add_to_settings_menu = False


class SampleAdminGroup(ModelAdminGroup):
    items = [SampleAdmin]
    menu_label = "File"
    menu_order = 900
    menu_icon = "fa-folder"


modeladmin_register(SampleAdminGroup)