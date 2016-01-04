from django.contrib import admin

# Register your models here.
from skillsdb.models import Skill
from skillsdb.models import SkillDetail
admin.site.register(Skill)
admin.site.register(SkillDetail)
#admin.site.register(Document)