from django.shortcuts import render, redirect
from .models import Customer
from django.contrib import messages
from .forms import UpdateCustomer, SignUpForm, UpdateUserForm, ChangePasswordForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# Update User
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

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

# view all customers
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customer_list.html', {'customers': customers})  

# view a single customer
def customer(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    return render(request, 'customer.html', {'customer': customer})

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