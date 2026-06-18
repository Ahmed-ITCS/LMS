from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from library_app.models import Book, BookTransaction, Member


class AddBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['isbn', 'title', 'author', 'copies']


class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search by title, author, or ISBN'}),
    )


class IssueBookForm(forms.Form):
    isbn = forms.ModelChoiceField(
        queryset=Book.objects.none(),
        to_field_name='isbn',
        label='Book',
    )
    member = forms.ModelChoiceField(
        queryset=Member.objects.none(),
        label='Member',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['isbn'].queryset = Book.objects.filter(copies__gt=0)
        self.fields['member'].queryset = Member.objects.all()


class ReturnBookForm(forms.Form):
    transaction = forms.ModelChoiceField(
        queryset=BookTransaction.objects.none(),
        label='Active loan',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['transaction'].queryset = BookTransaction.objects.filter(
            is_active=True
        ).select_related('book', 'member')


class MemberRegistrationForm(UserCreationForm):
    member_id = forms.CharField(max_length=20)
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'member_id']

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            Member.objects.create(user=user, member_id=self.cleaned_data['member_id'])
        return user


class LoginForm(AuthenticationForm):
    pass
