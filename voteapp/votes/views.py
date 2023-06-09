from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import PollCreateForm, VoteForm, PollUpdateForm
from .models import Topic, Option, Vote

def view_all_polls(request):
    #all() 해당 모델의 모든 데이터를 불러온다.
    topics = Topic.objects.all()
    context = {
        #기존 list 형태로 만든 데이터는 더 이상 불 필요
        'topics': topics
        #'topics':
         #   [
            #{'id': 1, 'topic': '부먹 VS 찍먹'},
            #{'id': 2, 'topic': '커피 VS 녹차'},
            #{'id': 3, 'topic': '딸기 VS 사과'},
          #   ]
    }
    return render(request, 'pages/view_all_polls.html', context)
def create_poll(request):
    if request.method == 'POST':
        form = PollCreateForm(request.POST)
        if form.is_valid():
            #데이터베이스에 저장하는 로직 추가 필요
            title = form.cleaned_data['topic']
            options = form.cleaned_data['options'].split(',')
            topic = Topic(title=title)
            topic.save()

            for item in options:
                Option.objects.create(name=item, topic=topic)

            return HttpResponseRedirect('/polls/')
    else:
        form = PollCreateForm()

    context = {
        'create_form': form
    }
    return render(request, 'pages/create_poll.html', context)
def view_poll_by_id(request, id):
    #get() : 데이터를 하나 특정해서 가져온다.
    #id, primery Key 내장, 이미 들어있고, 선언 불필요.
    topic = Topic.objects.get(id=id)
    #filter Method
    options = Option.objects.filter(topic=topic).all()
    #count() 레코드 개수를 반환한다.
    total_votes = Vote.objects.filter(topic=topic).count()

    results = {}
    for item in options:
        vote_count = Vote.objects.filter(option=item).count()
        if total_votes > 0:
            percent = vote_count / total_votes * 100

            result_text = "투표 수 : %d, 비율: %.2f" % (vote_count, percent)
        else:
            result_text = "투표_없음"
        results[item.name] = result_text

    context = {
        'topic': topic,
        'results': results
    }

    return render(request, 'pages/view_poll_by_id.html', context)
def vote_poll(request, id):
    topic = Topic.objects.get(id=id)

    if request.method == 'POST':
        form = VoteForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/polls/%d' % id)
    else:
        form = VoteForm()

    form.fields['topic'].initial = topic
    form.fields['option'].queryset = Option.objects.filter(topic=topic).all()

    context = {
        'form': form,
        'topic': topic
    }
    return render(request, 'pages/vote_poll.html', context)
def update_poll(request, id):
    topic = Topic.objects.get(id=id)

    if request.method =='POST':
        #POST에서 받은 데이터를 집어넣어줌, 새로 생성이 아니라, 기존 데이터를 활용, 그래서코드가 다른 것
        #form = PollCreateForm(request.POST, instance=topic)
        #이것 때문에 다운로드 기능이 된건가봐..아니야..
        form = PollUpdateForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()

            #기존 옵션 삭제
            Option.objects.filter(topic=topic).delete()

            #새로운 옵션 추가
            options_new = form.cleaned_data['options'].split(',')
            for item in options_new:
                Option.objects.create(name=item, topic=topic)

            return HttpResponseRedirect('/polls/%d/' % id)
    else:
        form = PollUpdateForm(instance=topic)
    # 초기값으로 기존 옵션들이 다 들어가도록 직접 수정
    options = Option.objects.filter(topic=topic).all()
    joined = ".".join(item.name for item in options)
    form.fields['options'].initial = joined

    context = {
        #= 아니라 :
        #'update_form' = form,
        'update_form': form,
        'topic': topic
    }
    #return HttpResponse(request, 'pages/update_poll.html, context')
    #찾았다! contextr가 '' 안에 들어왔네!!!!
    #게다가 htttResponse도 들어가 있네;;;
    return render(request, 'pages/update_poll.html', context)


def delete_poll(request, id):
    return HttpResponse('delete poll' + str(id))

