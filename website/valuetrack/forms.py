from django import forms
from .models import Customer, ProblemStatement, Provider, Category, Service
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django.contrib.auth.models import User

# Form for Category model
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']


# Update User Details
class UpdateUserForm(UserChangeForm):
	# Hide Password Stuff
	password = None
	# Get the other fields
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}), required=False)
	first_name = forms.CharField(label="", max_length=200, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}), required=False)
	last_name = forms.CharField(label="", max_length=200, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}), required=False)

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email')

	def __init__(self, *args, **kwargs):
		super(UpdateUserForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'
    
# Update User Password
class ChangePasswordForm(SetPasswordForm):
	class Meta:
		model = User
		fields = ['new_password1', 'new_password2']

	def __init__(self, *args, **kwargs):
		super(ChangePasswordForm, self).__init__(*args, **kwargs)

		self.fields['new_password1'].widget.attrs['class'] = 'form-control'
		self.fields['new_password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['new_password1'].label = ''
		self.fields['new_password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['new_password2'].widget.attrs['class'] = 'form-control'
		self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['new_password2'].label = ''
		self.fields['new_password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

# Register New User
class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email'}), required=False)
	first_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}), required=False)
	last_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}), required=False)

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'
  
# Form to Update Customer Details
class UpdateCustomer(forms.ModelForm):
    
    name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Customer Name', 'class': 'form-control'}), max_length=200, required=False)
    main_contact = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Main Contact','class': 'form-control'}), max_length=200, required=False)
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}), required=False)
    phone = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Phone', 'class': 'form-control'}), max_length=20, required=False)
    industry = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Industry', 'class': 'form-control'}), max_length=100, required=False)
    location = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Location', 'class': 'form-control'}), max_length=100, required=False)
    account_manager = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Account Manager', 'class': 'form-control'}), max_length=200, required=False)
    status = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Status', 'class': 'form-control'}), max_length=100, required=False)
    notes = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': 'Notes', 'class': 'form-control'}), required=False)

    logo = forms.ImageField(label='', required=False)

    class Meta:
        # Form for updating customer details
        model = Customer
        # Include all relevant fields for editing
        fields = ['name', 'main_contact', 'phone', 'email', 'account_manager', 'status', 'industry', 'location', 'notes', 'logo',]
        
# Form to Update Problem Statement Details        
class UpdateProblem(forms.ModelForm):

    customer = forms.ModelChoiceField(label='', queryset=Customer.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}), required=True)
    
    def __init__(self, *args, **kwargs):
        customer = kwargs.pop('customer', None)
        super().__init__(*args, **kwargs)

        if customer:
            self.fields['customer'].initial = customer
            self.fields['customer'].widget = forms.HiddenInput()


    title = forms.CharField(label='Title', widget=forms.TextInput(attrs={'placeholder': 'Problem Title', 'class': 'form-control'}), max_length=200, required=True)
    description = forms.CharField(label='Description', widget=forms.Textarea(attrs={'placeholder': 'Description', 'class': 'form-control', 'rows': 4}), required=True)
    impact = forms.CharField(label='Impact', widget=forms.Textarea(attrs={'placeholder': 'Impact', 'class': 'form-control', 'rows': 3}), required=False)
    urgency = forms.ChoiceField(label='Urgency', choices=ProblemStatement._meta.get_field('urgency').choices, widget=forms.Select(attrs={'class': 'form-select'}), required=False)
    status = forms.ChoiceField(label='Status', choices=ProblemStatement._meta.get_field('status').choices, widget=forms.Select(attrs={'class': 'form-select'}), required=False)
    notes = forms.CharField(label='Notes', widget=forms.Textarea(attrs={'placeholder': 'Notes', 'class': 'form-control', 'rows': 3}), required=False)

    class Meta:
        model = ProblemStatement
        fields = ['customer', 'title', 'description', 'impact', 'urgency', 'status', 'notes', ]
        
        
class UpdateProvider(forms.ModelForm):
	name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Provider Name', 'class': 'form-control'}), max_length=200, required=True)
	type = forms.ChoiceField(label='', choices=Provider._meta.get_field('type').choices, widget=forms.Select(attrs={'class': 'form-select'}), required=True)	
	department = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Department (if applicable)', 'class': 'form-control'}), max_length=200, required=False)
	contact_name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Contact Name', 'class': 'form-control'}), max_length=200, required=True)
	email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}), required=False)
	phone = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Phone', 'class': 'form-control'}), max_length=20, required=False)
	address = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Address', 'class': 'form-control'}), max_length=300, required=False)		
	address2 = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Address 2', 'class': 'form-control'}), max_length=300, required=False)
	city = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'City', 'class': 'form-control'}), max_length=100, required=False)
	county = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'County', 'class': 'form-control'}), max_length=100, required=False)
	postcode = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Postcode', 'class': 'form-control'}), max_length=20, required=False)
	country = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Country', 'class': 'form-control'}), max_length=100, required=False)
	notes = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': 'Notes', 'class': 'form-control', 'rows': 3}), required=False)
	status = forms.ChoiceField(label='', choices=Provider._meta.get_field('status').choices, widget=forms.Select(attrs={'class': 'form-select'}), required=True)
	tags = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Tags (comma-separated)', 'class': 'form-control'}), max_length=255, required=False)
	website = forms.URLField(label='', widget=forms.URLInput(attrs={'placeholder': 'Website', 'class': 'form-control'}), required=False)	
	industry = forms.ChoiceField(label='', choices=Provider._meta.get_field('industry').choices, widget=forms.Select(attrs={'class': 'form-select'}), required=True)

	# Set default values
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if not self.initial.get('type') and not self.data.get('type'):
			self.fields['type'].initial = 'External'

		if not self.initial.get('industry') and not self.data.get('industry'):
			self.fields['industry'].initial = 'Other'


	class Meta:
		model = Provider
		fields = ['name', 'type', 'department', 'contact_name', 'email', 'phone', 'address', 'address2', 'city', 'county', 'postcode', 'country', 'notes', 'status', 'tags', 'website', 'industry',]


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'category', 'tags', 'active']