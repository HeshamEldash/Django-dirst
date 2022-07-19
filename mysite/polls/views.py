from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice, CustomUser
from django.template import loader
from django.shortcuts import render,get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.models import User
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def logged_in(request):
    user= request.user
    context={
        "user": user
    }
    # print(request.method)
    if request.method == "POST":
        logout(request)
        print(request.method)
        return redirect("polls")

    return render(request, "polls/index.html", context=context)

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return render(request, "polls/logged_in.html")
        else:
            return render(request, "polls/login_user.html")
    else:
        return render(request, "polls/login_user.html")

def register(request):
    form = CreateUserForm
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name =  request.POST.get("first_name")
        email = request.POST.get("email")
        password = request.POST.get("password1")
        special_number = request.POST.get("special_number")
        user = User.objects.create_user(first_name, email, password)
        customuser = CustomUser(user_id=user.id ,special_number= special_number)
        customuser.save()
        return HttpResponseRedirect(reverse("polls:register"))
    else:
        print("get")
    context = {
        "form": form
    }
    return render(request, "polls/register.html", context=context)







# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     output = ", ".join([q.question_text for q in latest_question_list])
#     template = loader.get_template("polls/index.html")
#     context = {
#         "latest_question_list": latest_question_list,
#     }
#     return render(request, "polls/index.html", context=context)

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte= timezone.now()).order_by("-pub_date")[:5]




# def detail(request, question_id):
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#     # return render(request, 'polls/detail.html', {'question': question})
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/detail.html", {"question":question})




class DetailView (generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     context = {
#         "question" : question
#     }
#     return render(request, "polls/results.html", context=context)

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice= question.choice_set.get(pk=request.POST["choice"])
        print(request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


