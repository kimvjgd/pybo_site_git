from django.shortcuts import render, get_object_or_404, redirect, HttpResponse

from .models import Question, Answer
from django.utils import timezone


# Create your views here.
def index(request):
    """
    pybo 목록 출력
    """
    question_list = Question.objects.order_by('-create_date')       # - 내림차순
    total_count = Question.objects.count()
    context = {
        'question_list': question_list,
        'total_count':total_count
    }          # key 이름 = context 변수
    
    return render(request, 'pybo/question_list.html', context)
    # return HttpResponse("안녕하세요 pybo에 오신 것을 환영합니다.")

def detail(request, question_id):
    """
    pybo 내용 출력
    """
    
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)

def answer_create(request, question_id):
    """
    pybo 답변등록
    """
    question = get_object_or_404(Question, pk=question_id)
    # content = request.POST['content'] # content키가 없으면 - 예외가 발생
    content = request.POST.get('content')    # content가 없어도 none리턴

    # Answer 생성
      # 방법 1
    # answer = Answer(question = question, 
    #                 content = content,
    #                 create_date = timezone.now())
    # answer.save()
      # 방법 2] ForeignKey 관계인 경우
    question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
    return redirect('pybo:detail',question_id=question_id)
    # return redirect('pybo:detail',question_id=question_id)

