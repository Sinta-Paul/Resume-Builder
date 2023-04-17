from django.shortcuts import render,redirect
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
# Create your views here.
def home(request):

    style_sheet = getSampleStyleSheet()
    font = style_sheet['Normal'].fontName
    font_size = 16
    buffer = io.BytesIO()
    if request.method =='POST':
        org=request.POST.getlist("org")
        pos=request.POST.getlist("pos")
        fromex=request.POST.getlist("from-ex")
        toex=request.POST.getlist("to-ex")
        descex=request.POST.getlist("desc-ex")
        exp={}
        for i in range(len(org)):
            l1=[]
            l1.append(org[i])
            l1.append(pos[i])
            l1.append(descex[i])
            l1.append(toex[i])
            exp.update({i:l1})

        title=request.POST.getlist("title")
        link=request.POST.getlist("link")
        descpr=request.POST.getlist("desc-pr")
        project={}
        for i in range(len(title)):
            l1=[]
            l1.append(title[i])
            l1.append(link[i])
            l1.append(descpr[i])
            project.update({i:l1})

        descac=request.POST.getlist("desc-ac")
        hobby={}
        for i in range(len(title)):
            l1=[]
            l1.append(descac[i])
            hobby.update({i:l1})

        data={"PERSONAL":{"name":request.POST.get("name"),"email":request.POST.get("email"),"mobile":request.POST.get("mobile"),"linkedin":request.POST.get("linkedin"),"github":request.POST.get("github"),"skills":request.POST.getlist("skills")},
              "EDUCATION":{"college":request.POST.get("college"),"degree":request.POST.get("degree"),"discipline":request.POST.get("discipline"),"cgpa":request.POST.get("cgpa"),"from":request.POST.get("frm-ed"),"to":request.POST.get("to-ed")},
              "EXPERIENCE":exp,
              "PROJECTS":project,
              "HOBBIES":hobby}
        y=800

        pdf_canvas = canvas.Canvas(buffer)
        pdf_canvas.setFont(font, font_size)
        pdf_canvas.drawString(250, y, data['PERSONAL']['name'])
        font_size=11
        pdf_canvas.setFont(font, font_size)
        pdf_canvas.drawString(20,y-10,"______________________________________________________________________________________")
        pdf_canvas.drawString(160, y-30,data['PERSONAL']['email'])
        pdf_canvas.drawString(320, y-30,data['PERSONAL']['mobile'])
        pdf_canvas.drawString(200,y-50,data['PERSONAL']['linkedin'])
        pdf_canvas.drawString(200,y-70,data['PERSONAL']['github'])
        
        y=y-90
        pdf_canvas.drawString(20,y, "Education:")
        pdf_canvas.drawString(20,y-10,"______________________________________________________________________________________")
        pdf_canvas.drawString(20, y-30, data['EDUCATION']['college'])
        pdf_canvas.drawString(20, y-50,data['EDUCATION']['degree'])
        pdf_canvas.drawString(20, y-70,data['EDUCATION']['discipline'])
        pdf_canvas.drawString(200, y-30, "CGPA:{}".format(data['EDUCATION']['cgpa']))
        pdf_canvas.drawString(200, y-50, data['EDUCATION']['from'])
        pdf_canvas.drawString(270, y-50, data['EDUCATION']['to'])

        y=y-90
        pdf_canvas.drawString(20,y, "Experience:")
        pdf_canvas.drawString(20,y-10,"______________________________________________________________________________________")
        for idx, exp in data['EXPERIENCE'].items():
            y=y-25
            for i in exp:
                pdf_canvas.drawString(20,y,i)
                y=y-15


        y=y-50
        pdf_canvas.drawString(20,y, "Projects:")
        pdf_canvas.drawString(20,y-10,"______________________________________________________________________________________")
        for idx, exp in data['PROJECTS'].items():
            y=y-25
            for i in exp:
                pdf_canvas.drawString(20,y,i)
                y=y-15

        y=y-50
        pdf_canvas.drawString(20,y, "Hobbies/Achievements:")
        pdf_canvas.drawString(20,y-10,"__________________________________________________________________")
        for idx, exp in data['HOBBIES'].items():
            y=y-20
            for i in exp:
                pdf_canvas.drawString(20,y,i)
                y=y-10

        pdf_canvas.showPage()
        pdf_canvas.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='resume.pdf')

    return render(request,'base\main.html')