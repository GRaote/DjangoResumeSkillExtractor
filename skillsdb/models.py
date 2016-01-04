from django.db import models

# Create your models here.





class SkillsManager(models.Manager):
	def create_entry(self,file_name,file1,candidate_fullname):
		entry = self.create(file_name=file_name,file1=file1,candidate_fullname=candidate_fullname)
		return entry.entry_id

import time
def content_file_name(instance,filename):
	timestamp = time.strftime("%Y%m%d-%H%M%S")
	file_extension = filename.split('.')[1]
	file_name= filename.split('.')[0]
	filename = file_name+timestamp+'.'+file_extension
	#return '/'.join(['documents/resumes/',filename])
	return filename
class Skill(models.Model):
	entry_id= models.AutoField(primary_key=True)
	candidate_fullname = models.CharField(max_length =100,blank = True)
	file_name=models.CharField(max_length = 100)
	file1 = models.FileField(upload_to=content_file_name)
	objects=SkillsManager()
	def __unicode__(self):              
		return self.file_name
	


     	
class SkillDetail(models.Model):
	entry_id=models.ForeignKey(Skill, blank=True, null=True, on_delete=models.SET_NULL)
	skills_name=models.CharField(max_length = 100)
	skill_count = models.IntegerField(max_length =100)
	def __unicode__(self):              
		return self.skills_name

'''class Document(models.Model):
    file1 = models.FileField(upload_to=content_file_name)
    #file2= models.FileField(upload_to='documents/%Y/%m/%d')'''






    


    


