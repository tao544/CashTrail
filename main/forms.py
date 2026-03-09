from django import forms
from .models import Transaction

CATEGORY_CHOICES = [
    ("Food", "🍔 Food"),
    ("Transport", "🚗 Transport"),
    ("School", "📚 School"),
    ("Games", "🎮 Games"),
    ("Shopping", "🛍️ Shopping"),
    ("Other", "📦 Other"),
]

class ChildExpenseForm(forms.ModelForm):

    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.Select(attrs={
            "class": "form-select",
            "id": "categorySelect"
        })
    )

    other_category = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "What did you spend on?",
            "id": "otherCategory"
        })
    )

    class Meta:
        model = Transaction
        fields = ["category", "amount"]

        widgets = {
            "amount": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter amount"
            })
        }