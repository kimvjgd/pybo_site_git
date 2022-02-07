from django.shortcuts import render, get_object_or_404, redirect, HttpResponse

from config.settings import LOGIN_REDIRECT_URL

from .models import Question, Answer
from django.utils import timezone
from .forms import QuestionForm, AnswerForm, CommentForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required(login_url='common:login')
def comment_create_question(request, question_id):
      question = get_object_or_404(Question, pk=question_id)
      if request.method == "POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                  comment = form.save(commit=False)
                  comment.author = request.user
                  comment.create_date = timezone.now()
                  comment.question = question
                  comment.save()
                  return redirect('pybo:detail', question_id=question_id)
      else:
            form = CommentForm()
      context = {'form':form}
      return render(request, 'pybo/comment_form.html',)

@login_required(login_url='common:login')
def answer_delete(request, answer_id):
      """
      pybo 답변삭제
      """
      answer= get_object_or_404(Answer, pk=answer_id)
      if(request.user != answer.author):
            messages.error(request, '삭제권한이 없습니다.')
      else:
            answer.delete()
      return redirect('pybo:detail', question_id = answer.question.id)
    

@login_required(login_url='common:login')
def answer_modify(request, answer_id):
      """
      pybo 답변수정
      """
      answer = get_object_or_404(Answer, pk=answer_id)
      if request.user != answer.author:
            messages.error(request, '수정권한이 없습니다.')
            return redirect('pybo:detail', question_id=answer.question.id)
      if request.method == "POST":
            form = AnswerForm(request.POST, instance=answer)
            if form.is_valid():
                  answer = form.save(commit=False)
                  answer.author = request.user
                  answer.modify_date = timezone.now()
                  answer.save()
                  return redirect('pybo:detail', question_id=answer.question.id)
      else:
            form = AnswerForm(instance=answer)
      context = {'answer': answer, 'form': form}
      return render(request, 'pybo/answer_form.html', context)

@login_required(login_url='common:login')
def question_delete(request, question_id):
      """
      pybo 질문삭제
      """
      question = get_object_or_404(Question, pk=question_id)
      if request.user != question.author:
          messages.error(request, '삭제권한이 없습니다.')
          return redirect('pybo:detail', question_id = question.id)
      question.delete()
      return redirect('pybo:index')

@login_required(login_url='common:login')
def question_modify(request,question_id):
    """
    pybo 질문수정
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
      messages.error(request, '수정권한이 없습니다.')
      return redirect('pybo:detail', questino_id=question_id)
    
    if request.method == "POST":
      form = QuestionForm(request.POST, instance=question)
      if form.is_valid():
        question = form.save(commit=False)
        question.author = request.user
        question.modify_date = timezone.now()
        question.save()
        return redirect('pybo:detail',question_id=question.id)
    else:
      form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)



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


@login_required(login_url='common:login')
def comment_modify_question(request, comment_id):
  pass

@login_required(login_url='common:login')
def comment_delete_question(request, comment_id):
  pass


