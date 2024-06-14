from django import forms
from .models import ClaimsDebts,MonthlyReport

class DailyReportForm(forms.ModelForm):
    sales_hall = forms.DecimalField(label='فروش سالن', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'فروش سالن', 'min': 0}), required=False, initial=0)
    sales_takeaway = forms.DecimalField(label='فروش بیرون بر', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'فروش بیرون بر', 'min': 0}), required=False, initial=0)
    sales_snappfood = forms.DecimalField(label='فروش اسنپ فود', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'فروش اسنپ فود', 'min': 0}), required=False, initial=0)
    sales = forms.DecimalField(label='سفارشات', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'سفارشات', 'min': 0}), required=False, initial=0)
    sales_company = forms.DecimalField(label='سفارشات شرکتی', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'سفارشات شرکتی', 'min': 0}), required=False, initial=0)
    sales_special_company = forms.DecimalField(label='شرکت خاص', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'شرکت خاص', 'min': 0}), required=False, initial=0)
    sales_charity = forms.DecimalField(label='خیریه / هیات', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'خیریه / هیات', 'min': 0}), required=False, initial=0)
    sales_misc = forms.DecimalField(label='متفرقه', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'متفرقه', 'min': 0}), required=False, initial=0)
    total_sales = forms.DecimalField(label='جمع فروش', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'جمع فروش', 'min': 0}), required=False, initial=0)
    rent = forms.DecimalField(label='اجاره', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'اجاره', 'min': 0}), required=False, initial=0)
    salaries = forms.DecimalField(label='حقوق', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'حقوق', 'min': 0}), required=False, initial=0)
    overtime = forms.DecimalField(label='اضافه کاری', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'اضافه کاری', 'min': 0}), required=False, initial=0)
    raw_materials = forms.DecimalField(label='مواد اولیه', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'مواد اولیه', 'min': 0}), required=False, initial=0)
    consumables = forms.DecimalField(label='مواد مصرفی', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'مواد مصرفی', 'min': 0}), required=False, initial=0)
    maintenance = forms.DecimalField(label='جاری', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'جاری', 'min': 0}), required=False, initial=0)
    staff_meals = forms.DecimalField(label='غذای پرسنل', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'غذای پرسنل', 'min': 0}), required=False, initial=0)
    misc_expenses = forms.DecimalField(label='متفرقه', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'متفرقه', 'min': 0}), required=False, initial=0)
    total_expenses = forms.DecimalField(label='جمع هزینه‌ها', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'جمع هزینه‌ها', 'min': 0}), required=False, initial=0)
    monthly_profit = forms.DecimalField(label='سود ماهانه', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'سود ماهانه', 'min': 0}), required=False, initial=0)
    profit_percentage = forms.DecimalField(label='درصد سود', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'درصد سود', 'min': 0}), required=False, initial=0)
    cost_to_sales_ratio = forms.DecimalField(label='نسبت مواد به فروش', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'نسبت مواد به فروش', 'min': 0}), required=False, initial=0)

    class Meta:
        model = MonthlyReport
        exclude = ['date']
        

class ClaimsForm(forms.ModelForm):
    class Meta:
        model = ClaimsDebts
        fields = ['claimsdebts_id', 'type']
        widgets = {
            'claimsdebts_id': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.HiddenInput(),
        }
        labels = {
            'claimsdebts_id': 'عنوان طلب',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].initial = ClaimsDebts.CLAIM  # Set initial value for type
        self.fields['type'].widget = forms.HiddenInput()  # Hide the field from user input


class DebtsForm(forms.ModelForm):
    class Meta:
        model = ClaimsDebts
        fields = ['claimsdebts_id', 'type']
        widgets = {
            'claimsdebts_id': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.HiddenInput(),
        }
        labels = {
            'claimsdebts_id': 'عنوان بدهی',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].initial = ClaimsDebts.DEBT  # Set initial value for type
        self.fields['type'].widget = forms.HiddenInput()  # Hide the field from user input
        

class IngredientForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='نام',
        initial=''  # مقدار اولیه را در اینجا تنظیم کنید
    )
    amount = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control mt-1', 'placeholder': 'مقدار'}),
        label='مقدار',
        initial=0.0  # مقدار اولیه را در اینجا تنظیم کنید
    )    