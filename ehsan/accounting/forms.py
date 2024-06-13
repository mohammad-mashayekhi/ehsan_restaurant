from django import forms
from accounting.models import DailyReport

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class DailyReportForm(forms.ModelForm):
    hall_sales = forms.DecimalField(label='فروش سالن', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'فروش سالن', 'min': 0}), required=False, initial=0)
    takeaway_sales = forms.DecimalField(label='فروش بیرون بر', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'فروش بیرون بر', 'min': 0}), required=False, initial=0)
    snapp_food_sales = forms.DecimalField(label='فروش اسنپ فود', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'فروش اسنپ فود', 'min': 0}), required=False, initial=0)
    sales = forms.DecimalField(label='سفارشات', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'سفارشات', 'min': 0}), required=False, initial=0)
    company_orders = forms.DecimalField(label='سفارشات شرکتی', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'سفارشات شرکتی', 'min': 0}), required=False, initial=0)
    special_company = forms.DecimalField(label='شرکت خاص', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'شرکت خاص', 'min': 0}), required=False, initial=0)
    charity_orders = forms.DecimalField(label='خیریه / هیات', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'خیریه / هیات', 'min': 0}), required=False, initial=0)
    miscellaneous_sales = forms.DecimalField(label='متفرقه', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'متفرقه', 'min': 0}), required=False, initial=0)
    total_sales = forms.DecimalField(label='جمع فروش', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'جمع فروش', 'min': 0}), required=False, initial=0)
    rent = forms.DecimalField(label='اجاره', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'اجاره', 'min': 0}), required=False, initial=0)
    salary = forms.DecimalField(label='حقوق', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'حقوق', 'min': 0}), required=False, initial=0)
    overtime = forms.DecimalField(label='اضافه کاری', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'اضافه کاری', 'min': 0}), required=False, initial=0)
    raw_materials = forms.DecimalField(label='مواد اولیه', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'مواد اولیه', 'min': 0}), required=False, initial=0)
    consumables = forms.DecimalField(label='مواد مصرفی', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'مواد مصرفی', 'min': 0}), required=False, initial=0)
    current_expenses = forms.DecimalField(label='جاری', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'جاری', 'min': 0}), required=False, initial=0)
    staff_meal = forms.DecimalField(label='غذای پرسنل', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'غذای پرسنل', 'min': 0}), required=False, initial=0)
    miscellaneous_expenses = forms.DecimalField(label='متفرقه', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'متفرقه', 'min': 0}), required=False, initial=0)
    total_expenses = forms.DecimalField(label='جمع هزینه‌ها', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'جمع هزینه‌ها', 'min': 0}), required=False, initial=0)
    monthly_profit = forms.DecimalField(label='سود ماهانه', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'سود ماهانه', 'min': 0}), required=False, initial=0)
    profit_percentage = forms.DecimalField(label='درصد سود', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'درصد سود', 'min': 0}), required=False, initial=0)
    material_to_sales_ratio = forms.DecimalField(label='نسبت مواد به فروش', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'نسبت مواد به فروش', 'min': 0}), required=False, initial=0)

    class Meta:
        model = DailyReport
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }