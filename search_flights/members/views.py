from django.http import HttpResponse
from django.template import loader

def members(request):
  templates = ['userInput.html', 'results.html', 'forms.py']
  template = loader.get_template(templates)
  return HttpResponse(template.render())
