from django.shortcuts import render, get_object_or_404, redirect, HttpResponse

from config.settings import LOGIN_REDIRECT_URL

from .models import Question, Answer
from django.utils import timezone
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    """
    pybo 목록 출력
    """
    # 입력 파라미터
    page = request.GET.get('page', '1')   # 페이지
    question_list = Question.objects.order_by('-create_date')       # - 내림차순

    paginator = Paginator(question_list, 10)      # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj}

    
    return render(request, 'pybo/question_list.html', context)
    # return HttpResponse("안녕하세요 pybo에 오신 것을 환영합니다.")

def detail(request, question_id):
    """
    pybo 내용 출력
    """
    
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)

@login_required(login_url='common:login')
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
        answer.author = request.user
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

@login_required(login_url='common:login')
def question_create(request): 
  """
  pybo 질문등록
  """
  if request.method == 'POST':
    form = QuestionForm(request.POST)
    if form.is_valid():    # 유효성 검사
      question = form.save(commit=False)    # form 정보를 model에 저장하라
      question.author = request.user
      question.create_date = timezone.now()
      question.save()
      return redirect('pybo:index')
  else:
    form = QuestionForm()
  context = {'form':form}
  return render(request, 'pybo/question_form.html', context)


# def login(request): 
#   """
#   pybo 질문등록
#   """
#   if request.method == 'POST':
#     form = LoginForm(request.POST)
#     if form.is_valid():    # 유효성 검사

#       return redirect(LOGIN_REDIRECT_URL)
#   else:
#     form = LoginForm()
#   context = {'form':form}
#   return render(request, 'pybo/question_form.html', context)