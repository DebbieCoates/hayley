from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer, ProblemStatement, Provider
from django.contrib import messages
from .forms import UpdateCustomer, SignUpForm, UpdateProblem, UpdateUserForm, ChangePasswordForm, UpdateProblem, UpdateProvider
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q

# View all providers
def provider_list(request):
    sort = request.GET.get('sort', 'name')
    direction = request.GET.get('direction', 'asc')
    status_filter = request.GET.get('status')

    order_by = sort if direction == 'asc' else f'-{sort}'

    providers = Provider.objects.all()

    if status_filter:
        providers = providers.filter(status__iexact=status_filter)

    providers = providers.order_by(order_by)

    provider_status_summary = Provider.objects.values('status').annotate(count=Count('id'))

    return render(request, 'provider_list.html', {
        'providers': providers,
        'sort': sort,
        'direction': direction,
        'status_filter': status_filter,
        'provider_status_summary': provider_status_summary,
    })
    
# View an individual provider
def provider(request, provider_id):
    provider = get_object_or_404(Provider, id=provider_id)
    return render(request, 'provider.html', {'provider': provider})


# Delete a provider
def provider_delete(request, provider_id):
    provider = get_object_or_404(Provider, id=provider_id)
    provider.delete()
    messages.success(request, f'Provider "{provider.name}" deleted successfully.')
    return redirect('providers')

def provider_edit(request, provider_id):
    provider = get_object_or_404(Provider, id=provider_id)

    if request.method == 'POST':
        form = UpdateProvider(request.POST, instance=provider)
        if form.is_valid():
            form.save()
            messages.success(request, f'Provider "{provider.name}" updated successfully.')
            return redirect('provider', provider_id=provider.id)
    else:
        form = UpdateProvider(instance=provider)

    return render(request, 'provider_edit.html', {
        'form': form,
        'provider': provider
    })

# Add a new provider
def provider_add(request):
    if request.method == 'POST':
        form = UpdateProvider(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New provider added successfully.')
            return redirect('providers')
    else:
        form = UpdateProvider()
    return render(request, 'provider_add.html', {'form': form})

# Create your views here.
def home(request):
    return render(request, 'home.html')

# About page
def about(request):
    return render(request, 'about.html')

# View all problem statements
from django.db.models import Count

def problem_list(request):
    sort = request.GET.get('sort', 'title')
    direction = request.GET.get('direction', 'asc')
    status_filter = request.GET.get('status')
    urgency_filter = request.GET.get('urgency')

    order_by = sort if direction == 'asc' else f'-{sort}'

    problems = ProblemStatement.objects.select_related('customer')

    if status_filter:
        problems = problems.filter(status=status_filter)
    if urgency_filter:
        problems = problems.filter(urgency=urgency_filter)

    problems = problems.order_by(order_by)

    # Summary counts
    status_summary = ProblemStatement.objects.values('status').annotate(count=Count('id'))
    urgency_summary = ProblemStatement.objects.values('urgency').annotate(count=Count('id'))

    return render(request, 'problem_list.html', {
        'problems': problems,
        'sort': sort,
        'direction': direction,
        'status_filter': status_filter,
        'urgency_filter': urgency_filter,
        'status_summary': status_summary,
        'urgency_summary': urgency_summary,
    })
    
    
# View an individual problem statement
def problem(request, problem_id):
    problem = ProblemStatement.objects.get(id=problem_id)
    customer = problem.customer  # access the related customer
    return render(request, 'problem.html', {
        'problem': problem,
        'customer': customer
    })

# Delete a problem statement
def problem_delete(request, problem_id):
    problem = ProblemStatement.objects.get(id=problem_id)
    customer_id = problem.customer.id  # capture before deletion
    problem.delete()
    messages.success(request, f'Problem "{problem.title}" deleted successfully.')

    # Check if 'next' is passed in the query string
    next_url = request.GET.get('next')
    if next_url:
        return redirect(next_url)

    # Default fallback
    return redirect('problems')

# Edit a problem statement
def problem_edit(request, problem_id):
    problem = get_object_or_404(ProblemStatement, id=problem_id)
    customer = problem.customer

    if request.method == 'POST':
        form = UpdateProblem(request.POST, instance=problem)
        if form.is_valid():
            form.save()
            messages.success(request, f'Problem "{problem.title}" updated successfully.')
            return redirect('problem', problem_id=problem.id)
    else:
        form = UpdateProblem(instance=problem)

    return render(request, 'problem_edit.html', {
        'form': form,
        'problem': problem,
        'customer': customer
    })

# Add a new problem statement for a specific customer
def problem_add_from_customer(request, customer_id):
    customer = Customer.objects.get(id=customer_id)

    if request.method == "POST":
        form = UpdateProblem(request.POST)
        if form.is_valid():
            problem = form.save(commit=False)
            problem.customer = customer
            problem.save()
            messages.success(request, "New Problem Statement Added Successfully!")
            return redirect('customer', customer_id=customer.id)
    else:
        form = UpdateProblem(initial={'customer': customer})  # 👈 this pre-selects the customer

    return render(request, 'problem_add.html', {'form': form, 'customer': customer})
   
# Add a new problem statement (general)   
def problem_add(request):
    if request.method == "POST":
        form = UpdateProblem(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Problem added successfully.")
            return redirect('problems')
    else:
        form = UpdateProblem()

    return render(request, 'problem_add.html', {'form': form})


 # Update User Details    

# Update User Info
def update_user(request):
	if request.user.is_authenticated:
		# Get current user
		current_user = User.objects.get(id=request.user.id)
		# Create our form
		user_form = UpdateUserForm(request.POST or None, instance=current_user)
	
		if user_form.is_valid():
			# Update and Save user info
			user_form.save()
			# Log user back in
			login(request, current_user)
			messages.success(request, "Your User Info Has Been Updated!")
			return redirect('home')
		return render(request, 'update_user.html', {'user_form':user_form})
	else:
		messages.success(request, "Must Be Logged In To View That Page...")
		return redirect('login')

# Update User Password
def update_password(request):
	if request.user.is_authenticated:
		#get the current user
		current_user = request.user
		
		# Did they post? Or are they viewing the page
		if request.method == "POST":
			# Define our form
			form = ChangePasswordForm(current_user, request.POST)
			# is form valid
			if form.is_valid():
				#save the form info
				form.save()
				# re-login the user
				login(request,current_user)
				# Success message
				messages.success(request, "Your Password Has Been Updated!")
				return redirect('update_user')
			else:
				# loop thru error messages
				for error in list(form.errors.values()):
					messages.error(request, error)
					return redirect('update_password')
		else:
			# Define our form
			form = ChangePasswordForm(current_user)
			return render(request, 'update_password.html', {"form":form})

	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home') 

#login
def login_user(request):
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You have been logged in!")
                return redirect('home')
            else:
                messages.error(request, "There was an error logging in. Please try again...")
                return redirect('login')    
        else:
            return render(request, 'login.html', {})

#logout
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out...")
    return redirect('home')

# Register
def register_user(request):
	# Grab the register form
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			# Log them in
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			# Authenticate
			user = authenticate(username=username, password=password)
			# Log them in
			login(request, user)
			messages.success(request, "Login Succesful! Welcome!")
			return redirect('home')
		else:
			messages.success(request, "Whoops!  Looks Like There Was A Problem... Try Again!")
			return redirect('register')

	else:
		return render(request, 'register.html', {'form':form})

# view all customers
def customer_list(request):
    sort = request.GET.get('sort', 'name')
    direction = request.GET.get('direction', 'asc')
    status_filter = request.GET.get('status')
    problem_status_filter = request.GET.get('problem_status')

    order_by = sort if direction == 'asc' else f'-{sort}'

    customers = Customer.objects.annotate(
        open_problems=Count('problem_statements', filter=Q(problem_statements__status='Open')),
        closed_problems=Count('problem_statements', filter=Q(problem_statements__status='Closed'))
    )

    if status_filter:
        customers = customers.filter(status=status_filter)

    if problem_status_filter:
        customers = customers.filter(problem_statements__status=problem_status_filter).distinct()

    customers = customers.order_by(order_by)

    total_customers = customers.count()
    total_open = sum(c.open_problems for c in customers)
    total_closed = sum(c.closed_problems for c in customers)

    customer_status_summary = Customer.objects.values('status').annotate(count=Count('id'))
    problem_status_summary = ProblemStatement.objects.values('status').annotate(count=Count('id'))

    return render(request, 'customer_list.html', {
        'customers': customers,
        'sort': sort,
        'direction': direction,
        'status_filter': status_filter,
        'problem_status_filter': problem_status_filter,
        'total_customers': total_customers,
        'total_open': total_open,
        'total_closed': total_closed,
        'customer_status_summary': customer_status_summary,
        'problem_status_summary': problem_status_summary,
    })

# view an individual customer
def customer(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    problems = customer.problem_statements.all()
    problem_count = problems.count()

    return render(request, 'customer.html', {
        'customer': customer,
        'problems': problems,
        'problem_count': problem_count
    })

# delete a customer
def customer_delete(request, customer_id):
    # get the contact to be deleted
    customer = Customer.objects.get(id=customer_id)
    # delete the contact
    customer.delete()
    # display a success message
    messages.success(request, f'{customer.name} deleted successfully.')
    # redirect to the customer list page
    return redirect('customers')

# edit a customer
def customer_edit(request, customer_id):
    # Get the customer to be edited
    customer = Customer.objects.get(id=customer_id)
    # Pre-fill the form with the existing customer data
    form = UpdateCustomer(instance=customer)
    if request.method == 'POST':
        form = UpdateCustomer(request.POST, request.FILES or None, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, f'Customer {customer.name} updated successfully.')
            return redirect('customers')
    return render(request, 'customer_edit.html', {'customer': customer, 'form': form})
    
# add a new customer
def customer_add(request):
    if request.method == 'POST':
        form = UpdateCustomer(request.POST, request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'New customer added successfully.')
            return redirect('customers')
    else:
        form = UpdateCustomer()
    return render(request, 'customer_add.html', {'form': form})