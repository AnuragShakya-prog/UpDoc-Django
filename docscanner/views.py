from django.shortcuts import render,redirect
from .forms import DocumentForm
import pdb
from PIL import Image
from .models import Document
from django.core.files.uploadedfile import InMemoryUploadedFile
import io
import numpy as np
from docscanner.docScanner import scan as scanner
from django.shortcuts import get_object_or_404
import random
import json
import uuid
from django.http import Http404
import cv2
import numpy as np
from docscanner.docScanner.pyimagesearch.transform import four_point_transform
import imutils
#  Create your views here.



def homepage(request):
    if(request.user.is_authenticated):
        return redirect("/docs/dashboard")
    else:
        return render(request,"docscanner/index.html")


def dashboard(request):
    if request.user.is_authenticated:

        if request.method=='POST':
            image=request.FILES["document_image"]
            document_name=request.POST.get("document_name","document")
            gr_width=request.POST.get("gr_width",'false')

            if image:
                points=request.POST.get("points",[])
                gr_width=json.loads(gr_width)
                points=json.loads(points)

                image_array=np.asarray(Image.open(image))
                image_array=correctImage(image_array,gr_width)

                if len(points)==4:
                    scanned_image,doc_outline_image=drawRectFromCorner(image_array,points)
                    found=True

                else:

                    scanned_image,doc_outline_image,found=scanner.scanDocument(image_array)
                    
                if not found:
                    return render(request,"docscanner/doc404.html",status=404)

                scanned_image_bytes=io.BytesIO()
                
                tempScannedImage=Image.fromarray(scanned_image)
                tempScannedImage.save(fp=scanned_image_bytes,format='PNG')
                
                # Handling outline image
                outline_image_pil=Image.fromarray(doc_outline_image)
                outline_image_bytes=io.BytesIO()
                outline_image_pil.save(outline_image_bytes,format="PNG")
                

                inmemory_scanned_image=InMemoryUploadedFile(scanned_image_bytes,"document_image",f"image-{document_name}-id{str(uuid.uuid1())}.png","image/png",len(scanned_image_bytes.getbuffer()),None)
                inmemory_outline_image=InMemoryUploadedFile(outline_image_bytes,"outline_image",f"out_{str(uuid.uuid1())}.png","image/png",len(outline_image_bytes.getbuffer()),None)
                
                

                document=Document.objects.create(document_owner=request.user,document_image=inmemory_scanned_image,document_name=document_name,outline_image=inmemory_outline_image)
                
                return redirect(f"/docs/docinfo/{document.pk}/")

        user_documents=Document.objects.filter(document_owner=request.user)
        context={"form":DocumentForm,"docs":user_documents}

        return render(request,"docscanner/dashboard.html",context)
    else:
        return redirect("/")



def docView(request,docId):
    
    if request.user.is_authenticated:
        document=get_object_or_404(Document,pk=docId,document_owner=request.user)

        return render(request,"docscanner/docView.html",{"document":document})
        


def docInfo(request,docId):

    document=get_object_or_404(Document,pk=docId,document_owner=request.user)
    if request.method=='POST':
        document.delete()
        return redirect("/")

    return render(request,"docscanner/confirm_document.html",{"document":document})


def drawRectFromCorner(image,points):
    
    points=np.array(points)*image.shape[:2][::-1]

    cropped=four_point_transform(image,points)
    cropped=imutils.resize(cropped,height=600)


    return cropped,image

   
def correctImage(image,gr_width):
    # Sometimes the image gets rotated automatically while transfering from frontend to backend
    # gr_width: if it's True this means the width was greater than height
    # So checking here also if width is greater than Height if not rotate it
    # image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    (height,width)=image.shape[:2]

    if gr_width:

        if width>height or width==height:
            return image

        else:
            rotated=Image.fromarray(image).transpose(Image.ROTATE_270)
            image=np.asarray(rotated)
    
        return image
    else:
        
        if height>width or width==height:
            return image

        else:
            rotated=Image.fromarray(image).transpose(Image.ROTATE_270)
            image=np.asarray(rotated)
    
        return image
