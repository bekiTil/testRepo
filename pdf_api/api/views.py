from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from reportlab.pdfgen import canvas
from io import BytesIO

class GeneratePDFView(APIView):
    def post(self, request):
        data = request.data
        name = data.get('name')
        email = data.get('email')
        details = data.get('details')

        if not all([name, email, details]):
            return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        # Generate PDF
        pdf_buffer = BytesIO()
        p = canvas.Canvas(pdf_buffer)
        p.drawString(100, 800, f"Name: {name}")
        p.drawString(100, 780, f"Details: {details}")
        p.showPage()
        p.save()

        pdf_buffer.seek(0)
        pdf_filename = f"{name}_details.pdf"

        # Send Email with PDF Attachment
        email_subject = "Your Generated PDF"
        email_body = "Please find attached your PDF document."
        email_message = EmailMessage(
            subject=email_subject,
            body=email_body,
            from_email=None,
            to=[email],
        )
        email_message.attach(pdf_filename, pdf_buffer.read(), "application/pdf")
        email_message.send()

        return Response({"message": "PDF generated and email sent successfully."}, status=status.HTTP_200_OK)
