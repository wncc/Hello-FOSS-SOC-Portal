from django.contrib import admin
# from django.contrib import admin
from .models import Project, Mentee, MenteePreference, MenteeWishlist


# class MentorInline(admin.TabularInline):
#     model = MentorRequest
#     max_num = 4
#     extra = 1


# class ProjectAdmin(admin.ModelAdmin):
#     model = Project
#     inlines = [MentorInline]

class MenteeAdmin(admin.ModelAdmin):
    list_per_page = 1000  


# Register your models here.
# admin.site.register(Season)
# admin.site.register(Project, ProjectAdmin)
# admin.site.register(Mentor)
admin.site.register(Project)    
admin.site.register(Mentee, MenteeAdmin)
# admin.site.register(ProjectCategory)
admin.site.register(MenteePreference)
admin.site.register(MenteeWishlist)
