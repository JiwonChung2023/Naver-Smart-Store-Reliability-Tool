<<<<<<< HEAD
from django.db import models
from datetime import datetime

# 장고 모델을 상속하여 새 모델 파일을 생성 -> DB의 테이블
class Quest(models.Model):
    qtxt=models.CharField(max_length=200)
    qdate=models.DateTimeField('date published')

class Choice(models.Model):
    quest=models.ForeignKey(Quest,on_delete=models.CASCADE)
    choice_txt=models.CharField(max_length=150)
    votes=models.IntegerField(default=0)
=======
from django.db import models
from datetime import datetime

# 장고 모델을 상속하여 새 모델 파일을 생성 -> DB의 테이블
class Quest(models.Model):
    qtxt=models.CharField(max_length=200)
    qdate=models.DateTimeField('date published')

class Choice(models.Model):
    quest=models.ForeignKey(Quest,on_delete=models.CASCADE)
    choice_txt=models.CharField(max_length=150)
    votes=models.IntegerField(default=0)
>>>>>>> 74da7df84f4910ad177c46656938bc1ce1afeb51
    vdate=models.DateTimeField('date published',default=datetime.now)