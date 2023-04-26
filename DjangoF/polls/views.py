<<<<<<< HEAD
from django.shortcuts import render
# http로 반환값을 주기 위한 함수
from django.http import HttpResponse # http로 반환 값을 주기 위한 함수
from .models import Quest
from django.utils import timezone
from . import main
# Create your views here.
def index(request):
    #return HttpResponse(data)
    qlist=Quest.objects.all()
    print(qlist)
    page={'title':'홍길동의 포트폴리오',
          'h1': '데이터 사이언티스트 홈',
          'slogan':'귀사의 점프를 위한 인재가 여기 있습니다.'
          }
    return render(request,'front.html',{'quests':qlist,'page':page})

def create(request):
    #return HttpResponse('')
    if(request.method=='POST'):
          qt=request.POST['qtxt']
          print('QTXT:',qt)
          quest=Quest(qtxt=qt,qdate=timezone.now())
          quest.save()

    qlist=Quest.objects.all()
    print(qlist)
    grade,stName=main.nssrt(qt)
    page={"title":'홍길동의 포트폴리오',
          "h1":"DAATT",
          "h2":"데이터 받음",
          "data":qt+"를 분석한 결과,.",
          "grade":"해당 스토어("+stName+")는 "+grade+" 등급을 받았습니다."
          }
    return render(request,'back.html',{"quests":qlist,"page":page})

def move(request):
    #return HttpResponse('')
    if(request.method=='POST'):
          qt=request.POST['qtxt']
          print('QTXT:',qt)
          quest=Quest(qtxt=qt,qdate=timezone.now())
          quest.save()
          
    qlist=Quest.objects.all()
    print(qlist)
    page={"title":'홍길동의 포트폴리오',
          "h1":"DAATT",
          "h2":"데이터 받음",
          "data":qt+" 를 받았습니다.",
          }
    return render(request,'back.html',{"quests":qlist,"page":page})
=======
from django.shortcuts import render
# http로 반환값을 주기 위한 함수
from django.http import HttpResponse # http로 반환 값을 주기 위한 함수
from .models import Quest

# Create your views here.
def index(request):
    #return HttpResponse(data)
    qlist=Quest.objects.all()
    print(qlist)
    page={'title':'홍길동의 포트폴리오',
          'h1': '데이터 사이언티스트 홈',
          'slogan':'귀사의 점프를 위한 인재가 여기 있습니다.'
          }
    return render(request,'base.html',{'quests':qlist,'page':page})
>>>>>>> 74da7df84f4910ad177c46656938bc1ce1afeb51
