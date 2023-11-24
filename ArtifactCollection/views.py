__author__ = "reed@reedjones.me"
from django.shortcuts import render
from django import forms

#
#
# def upload_file(request):
#     if request.method == 'POST':
#         form = YourForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#     else:
#         form = YourForm()
#
#     return render(request, 'upload_file.html', {'form': form})