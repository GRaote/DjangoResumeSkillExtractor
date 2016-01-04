from django import forms
from skillsdb.forms import UploadFileForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.template import RequestContext
import pyPdf
from bs4 import BeautifulSoup 
import re
import time
import numpy as np
from nltk.corpus import stopwords
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from prettytable import PrettyTable
from os.path import abspath, dirname
from skillsdb.models import Skill, SkillDetail
from django.db.models import Q
from django.utils.encoding import smart_str
from django.template import Context
from django.http import HttpResponse

try:
    from xml.etree.cElementTree import XML
except ImportError:
    from xml.etree.ElementTree import XML
import zipfile
def upload(request):
    context = RequestContext(request)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file1 = request.FILES['file1']
            file2 = request.FILES['file2']
            candidate_fullname = request.POST['candidate_name']
            #newdoc = Document(file1=file1)
            #newdoc.save()
            #file_name1 = file1.name
            file_name2 = file2.name
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            file_name_first_part= file1.name.split('.')[0]
            file_extension1 = file1.name.split('.')[1]
            file_extension2 = file_name2.split('.')[1]
            file_name1 = file_name_first_part+timestamp+'.'+file_extension1
            if (file_extension1.lower() == 'pdf' and file_name2=='Skills.xlsx'):
                s_id=Skill.objects.create_entry(file_name=file_name1,file1=file1,candidate_fullname=candidate_fullname)
                skill_id = Skill.objects.get(entry_id = s_id)
                train=pd.read_excel(file2)
                str1=handle_uploaded_file(file1)
                skills=get_skills(str1,train)
                for key,value in skills:
                    SkillDetail.objects.create(entry_id=skill_id,skills_name=value,skill_count=key)

                return render_to_response("output.html",{"success_message" :"Success","skills":skills},context)
            elif(file_extension1.lower()=='docx' and file_name2=='Skills.xlsx'):
                s_id=Skill.objects.create_entry(file_name=file_name1,file1=file1,candidate_fullname=candidate_fullname)
                skill_id = Skill.objects.get(entry_id = s_id)
                train=pd.read_excel(file2)
                str1=get_docx_text(file1)
                skills=get_skills(str1,train)
                for key,value in skills:
                    SkillDetail.objects.create(entry_id=skill_id,skills_name=value,skill_count=key)
                return render_to_response("output.html",{"success_message" :"Success","skills":skills},context) 
            else:
                form = UploadFileForm()
                return render_to_response("upload.html",{"error_message" : "Invalid File Format","form":form},context)
        else:
            form = UploadFileForm()
            return render_to_response("upload.html", {"form": form},context) 
    else:
        form = UploadFileForm()
        return render_to_response("upload.html", {"form": form},context)


def get_skills(str1,train):
    cleanedText=review_to_words(str1)
    cleanedText=cleanedText.split()
    train_data=",".join(w for w in train.Skills)
    train_data_new=train_data.lower()
    train_data_new=train_data_new.split(",")
    final=[w for w in cleanedText if w in train_data_new]
    vectorizer = CountVectorizer(analyzer = "word",   \
                             tokenizer = None,    \
                             preprocessor = None, \
                             stop_words = None,   \
                             max_features = 50000) 

    train_data_features = vectorizer.fit_transform(final)
    train_data_features = train_data_features.toarray()
    vocab = vectorizer.get_feature_names()
    dist = np.sum(train_data_features, axis=0)
    skills=zip(dist,vocab)
    skills.sort(reverse=True)
    return skills

def get_docx_text(path):
    """
    Take the path of a docx file as argument, return the text in unicode.
    """
    WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    PARA = WORD_NAMESPACE + 'p'
    TEXT = WORD_NAMESPACE + 't'
    document = zipfile.ZipFile(path)
    xml_content = document.read('word/document.xml')
    document.close()
    tree = XML(xml_content)

    paragraphs = []
    for paragraph in tree.getiterator(PARA):
        texts = [node.text
                 for node in paragraph.getiterator(TEXT)
                 if node.text]
        if texts:
            paragraphs.append(''.join(texts))

    return '\n\n'.join(paragraphs)
	
	
def handle_uploaded_file(file):
    content = ""
    # Load PDF into pyPDF
    pdf = pyPdf.PdfFileReader(file)
    # Iterate pages
    for i in range(0, pdf.getNumPages()):
        # Extract text from page and add to content
        content += pdf.getPage(i).extractText() + "\n"
    # Collapse whitespace
    content = " ".join(content.replace(u"\xa0", " ").strip().split())
	#returns a string of all the words in the pdf
	
    return content

def review_to_words( text ):
    review_text = BeautifulSoup(text).get_text()      
    letters_only = re.sub("[^a-zA-Z]", " ", review_text) 
    words = letters_only.lower().split()                             
    #stops = set(stopwords.words("english"))                  
    #meaningful_words = [w for w in words if not w in stops]   
    return( " ".join( words ))  

def search_by_skills(request):
    context = RequestContext(request)
    if request.method == 'POST':
        search_string = request.POST.get('Search')
        if len(search_string) < 1:
            return render_to_response('search_by_skills.html', {'error_message':"Enter value to search"}, context)
        else:
            dataFound = SkillDetail.objects.filter(Q(skills_name__istartswith=search_string) | Q(skills_name__icontains=search_string)).order_by('-skill_count')
            return render_to_response('search_by_skills.html', {'dataFound':dataFound,'error_message':"No entry found"}, context)
    else:
        return render_to_response('search_by_skills.html', context)
 
'''def downloadfile(request):
    
    if request.method == 'POST':
        context = RequestContext(request)
        data_enrty_id = request.POST.get('Download')
        documents = Skills.objects.get(entry_id = data_entry_id)

        return render_to_response("search_by_skills.html",context)
    else:
        return render_to_response("search_by_skills.html",{"success_message" : "File Not Found"},context)'''

import os
from django.core.servers.basehttp import FileWrapper
from django.conf import settings
def downloadfile(request):
    context = RequestContext(request)
    file_name = request.GET.get('file_name')
    #print file_name
    #path_to_file1 = Skill.objects.get(file_name = file_name)
    #print path_to_file1.file1
    path_to_file = settings.MEDIA_ROOT+'/'+str(file_name)
    pdf = open(path_to_file, 'rb')
    #print path_to_file
    wrapper = FileWrapper(file( path_to_file ))
    response = HttpResponse(wrapper,content_type='application/force-download')
    
    #response['Content-Length'] = os.path.getsize(file_name)
    #response['X-Sendfile'] = smart_str( os.path.basename( path_to_file ) )
    
    response = HttpResponse(pdf.read())
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str( os.path.basename( path_to_file ) )
    return response

       
    
