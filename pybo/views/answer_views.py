from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone


from ..forms import AnswerForm
from ..models import Question, Answer



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

      # 방법 1]
      # answer = Anser(question = question,
      #                content = content,
      #                create_date = timezone.now())
      # answer.save()


      # 방법 2] ForeignKey 관계인 경우
      # question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
      # return redirect('pybo:detail',question_id=question_id)
      # return redirect('pybo:detail',question_id=question_id)


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
    