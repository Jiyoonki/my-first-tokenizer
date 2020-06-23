from django.shortcuts import render

# Create your views here.

def token_list(request):
    return render(request, 'tokenizer/token_list.html', {})