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
      stName,grade,sco,isok,upper4point8=main.nssrt(qt)

      page={"title":'홍길동의 포트폴리오',
            "h1":"DAATT",
            "h2":"데이터 받음",
            "result":"해당 스토어("+stName+") 분석 결과 "+grade+"등급",
            "grade":grade,
            "name":stName
            
            }
      if (isok=='정상영업'):
            if (upper4point8=='yes'):
                  if (sco<10):
                        page['aresult1'] = '정상적으로 등록된 사업자입니다.'
                        page['aresult2'] = '상품별 별점에 의심의 여지가 있습니다.'
                        page['aresult3'] = '작위적인 리뷰를 찾지 못했습니다.'

                  elif (10<sco<30):
                       page['aresult1'] = '정상적으로 등록된 사업자입니다.'
                       page['aresult2'] = '상품별 별점에 의심의 여지가 있습니다.'
                       page['aresult3'] = '작위적인 리뷰를 조금 발견했습니다.'
                  else:
                       page['aresult1'] = '정상적으로 등록된 사업자입니다.'
                       page['aresult2'] = '상품별 별점에 의심의 여지가 있습니다.'
                       page['aresult3'] = '작위적인 리뷰를 다수 발견했습니다.'
            else:
                  if (sco<10):
                       page['aresult1'] = '정상적으로 등록된 사업자입니다.'
                       page['aresult2'] = '상품별 별점에 의심의 여지가 있습니다.'
                       page['aresult3'] = '작위적인 리뷰를 찾지 못했습니다.'
                  elif (10<sco<30):
                       page['aresult1'] = '정상적으로 등록된 사업자입니다.'
                       page['aresult2'] = '상품별 별점에 의심의 여지가 있습니다.'
                       page['aresult3'] = '작위적인 리뷰를 조금 발견했습니다.'
                  else:
                       page['aresult1'] = '정상적으로 등록된 사업자입니다.'
                       page['aresult2'] = '상품별 별점에 의심의 여지가 있습니다.'
                       page['aresult3'] = '작위적인 리뷰를 다수 발견했습니다.'
      else: 
            page['aresult1']='정상적으로 등록된 사업자가 아닙니다. 주의하세요.'
      return render(request,'back.html',{"page":page})
