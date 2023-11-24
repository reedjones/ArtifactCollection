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



from django.core.mail import EmailMessage

def send_notification_email_with_attachment(user, message, attachment_path):
    subject = 'Notification'
    from_email = 'your_email@example.com'
    recipient_list = [user.email]

    email = EmailMessage(subject, message, from_email, recipient_list)
    email.attach_file(attachment_path)
    email.send()



from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa

class PDFReportView(View):
    def get(self, request, *args, **kwargs):
        template_path = 'pdf/report_template.html'
        context = {'artifacts': Artifact.objects.all()}

        # Create a Django response object with appropriate PDF headers
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="report.pdf"'

        # Create a PDF object using the response object as its "file"
        pdf = pisa.CreatePDF(get_template(template_path).render(context), dest=response)

        # Return the response
        if not pdf.err:
            return response

        return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))