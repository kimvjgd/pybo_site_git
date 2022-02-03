from django.shortcuts import render, get_object_or_404, redirect, HttpResponse

from .models import Question, Answer
from django.utils import timezone
from .forms import QuestionForm, AnswerForm


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
        # 방법 1
    question = get_object_or_404(Question, pk=question_id) 
    if request.method == "POST":
      form = AnswerForm(request.POST) 
      if form.is_valid():
        answer = form.save(commit=False)
        answer.create_date = timezone.now()
        answer.question = question      # FK 처리
        answer.save()
        return redirect('pybo:detail', question_id=question.id)
    else:
      form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)


        # 방법 2] ForeignKey 관계인 경우
      # question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
      # return redirect('pybo:detail',question_id=question_id)
      # return redirect('pybo:detail',question_id=question_id)


def question_create(request): 
  """
  pybo 질문등록
  """
  if request.method == 'POST':
    form = QuestionForm(request.POST)
    if form.is_valid():    # 유효성 검사
      question = form.save(commit=False)    # form 정보를 model에 저장하라
      question.create_date = timezone.now()
      question.save()
      return redirect('pybo:index')
  else:
    form = QuestionForm()
  context = {'form':form}
  return render(request, 'pybo/question_form.html', context)

