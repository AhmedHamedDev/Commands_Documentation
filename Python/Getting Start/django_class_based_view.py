## https://www.dennisivy.com/post/django-class-based-views/

#  Function based view

from django.shortcuts import render
from .models import Product

def productList(request):
	products = Product.objects.all()
	context = {'products/':products}
	return render(request, 'base/product_list.html', context)

from . import views 

urlpatterns = [
    path('products', views.productsList, name='products'),
]

#############

from django.shortcuts import render
from .models import Product

def productsList(request):
	products = Product.objects.all()
	
	if request.method == 'POST':
  		Product.object.create()
	
	context = {'products':products}
	return render(request, 'base/product_list.html', context)

#  Function based view

# className.as_view() : at the url pattern 
## when we want a class to act as a method that return view
## Any arguments passed to as_view() will override attributes set on the class. In this example,
## we set template_name on the TemplateView. A similar overriding pattern can be used for the url attribute on RedirectView.


from django.views.generic.list import ListView
from .models import Product 

class ProductList(ListView):
	model = Product
  

from . import views 

urlpatterns = [
    path('products', views.ProductList.as_view(), name='products'),
]

#################

from django.views.generic.list import ListView
from .models import Product 

class ProductList(ListView):
	model = Product

	def post(self, request):
		Product.object.create()

##################

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Task

class TaskList(ListView):
	   model = Task

class TaskDetail(DetailView):
	   model = Task

class TaskCreate(CreateView):
	   model = Task
       fields = ['title', 'description', 'complete']
       success_url = reverse_lazy('tasks')

class TaskUpdate(UpdateView):
       model = Task
       fields = ['title', 'description', 'complete']
       success_url = reverse_lazy('tasks')

class TaskDelete(DeleteView):
      model = Task
      context_object_name = 'task'
      success_url = reverse_lazy('tasks')



from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete


urlpatterns = [
    path('', TaskList.as_view(), name='tasks'),
    path('task/<str:pk>/', TaskDetail.as_view(), name='task'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<str:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<str:pk>/', TaskDelete.as_view(), name='task-delete'),
]

# override properties
class TaskList(ListView):
	model = Task
	template_name = 'base/tasks.html'
	context_object_name = 'tasks'
	paginate_by = 5
	ordering = ['-date_created']

#######################

# Django Built in views

# Django provides use with many built in views we can use and customize. These views are separated into the following categories:

    # Generic Base Views
    # Generic Display Views
    # Generic  Editing Views
    # Generic date views
    # Auth Views

# Listed out below are all the django built in views inside of their category:

# Auth Views

    # LoginView
    # LogoutView
    # PasswordChangeDoneView
    # PasswordChangeView
    # PasswordResetCompleteView
    # PasswordResetConfirmView
    # PasswordResetDoneView
    # PasswordResetView

# Generic Base

    # RedirectView
    # TemplateView
    # View

# Generic List

    # ListView

# Generic Detail

    # DetailView

# Generic Edit

    # CreateView
    # DeleteView
    # FormView
    # UpdateView

# Generic Dates

    # ArchiveIndexView
    # DateDetailView
    # DayArchiveView
    # MonthArchiveView
    # TodayArchiveView
    # WeekArchiveView
    # YearArchiveView