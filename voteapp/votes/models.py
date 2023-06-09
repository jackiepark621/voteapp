from django.db import models

class Topic(models.Model):
    #null=False, 비어있지 않도록
    title = models.CharField(max_length=50, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    # auto_now_add: 레코드 추가될 때 알아서 입력된 시간이 저장되도록 한다.

    #topics, options로 일률적으로 나오는 것을 해결
    def __str__(self):
        return self.title


class Option(models.Model):
    name = models.CharField(max_length=20, null=False)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=False)
    #ForeignKey로 Topic연계, on_delete로 만약 토픽이 삭제되면 같이 삭제 되는 것

    def __str__(self):
        return self.name

class Vote(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=False)
    option = models.ForeignKey(Option, on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)

