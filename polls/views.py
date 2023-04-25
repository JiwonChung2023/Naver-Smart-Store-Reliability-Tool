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