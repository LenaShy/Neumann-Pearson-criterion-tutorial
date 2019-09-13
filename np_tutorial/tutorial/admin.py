from django.contrib import admin
from .models import Matrix, Row


class MatrixRowInline(admin.TabularInline):
    model = Row


class MatrixAdmin(admin.ModelAdmin):
    inlines = [
        MatrixRowInline,
    ]


admin.site.register(Matrix, MatrixAdmin)
admin.site.register(Row)
