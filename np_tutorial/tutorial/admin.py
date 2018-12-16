from django.contrib import admin
from .models import Matrix, MatrixRow


class MatrixRowInline(admin.TabularInline):
    model = MatrixRow


class MatrixAdmin(admin.ModelAdmin):
    inlines = [
        MatrixRowInline,
    ]


admin.site.register(Matrix, MatrixAdmin)
admin.site.register(MatrixRow)
