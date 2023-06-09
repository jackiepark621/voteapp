from django import forms
from .models import Vote, Topic

class PollCreateForm(forms.Form):
    topic = forms.CharField(label='투표주제', min_length='2', max_length='50')
    options = forms.CharField(label='튜표 선택옵션', min_length='2', max_length='300')


class PollUpdateForm(forms.ModelForm):
    #선택지 수정
    #토픽과 관계 없이 그냥 만들어버림
    options = forms.CharField(label='투표 선택 옵션', min_length=2, max_length=300)

    class Meta:
        model = Topic
        fields = ['title']
        labels = {
            'title': '제목을 바꺼바라'
        }


#모델 폼 선언
#주의!! forms.Form 아니라 form.ModelForm이다!!
class VoteForm(forms.ModelForm):
    topic = forms.ModelChoiceField(queryset=Topic.objects.all(), widget=forms.HiddenInput)

    #meta, M 대문자 필수
    class Meta:
        #모델에 있는 vote를 참조하기 위해, model로부터 import하는 것
        model = Vote
        fields = ['topic', 'option']
        labels = {
            'option': '선택이름 바꺼바라'
        }

#장고의 모델폼을 상속 받으면, 내부에 메타라는 크래스를 선언하고, 연결할 모델에 참조를 선언하는 것으로
#바로 폼을 구현할 수 있습니다.
#vote가 참조안되니까, 되기 위해 import
#이렇게 하면 장고에서 모델의 각 송성에 알맞은 폼 필드를 바로 그려주는 거죠.
#그러니까 따로 필드를 정의할 필요가 없다는 말이죠.
#대부분의 모델 속성을 가지고 있기 때문에, 해당 필드만 그려지고 입력 받도록 선언할 수 있습니다.
#topic, option이라는 필드만 입력받도록 했습니다.
