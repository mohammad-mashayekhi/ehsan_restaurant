from django import forms
from .models import ClaimDebt,MonthlyReport

class DailyReportForm(forms.ModelForm):
    sales_hall = forms.CharField(label='فروش سالن', widget=forms.TextInput(attrs={'class': 'form-control price-input', 'placeholder': 'فروش سالن', 'min': 0}), required=False, initial=0)
    sales_takeaway = forms.CharField(label='فروش بیرون بر', widget=forms.TextInput(attrs={'class': 'form-control price-input', 'placeholder': 'فروش بیرون بر', 'min': 0}), required=False, initial=0)
    sales_snappfood = forms.CharField(label='فروش اسنپ فود', widget=forms.TextInput(attrs={'class': 'form-control price-input', 'placeholder': 'فروش اسنپ فود', 'min': 0}), required=False, initial=0)
    sales_company = forms.CharField(label='سفارشات شرکتی', widget=forms.TextInput(attrs={'class': 'form-control price-input', 'placeholder': 'سفارشات شرکتی', 'min': 0}), required=False, initial=0)
    sales_special_company = forms.CharField(label='شرکت خاص', widget=forms.TextInput(attrs={'class': 'form-control price-input', 'placeholder': 'شرکت خاص', 'min': 0}), required=False, initial=0)
    sales_charity = forms.CharField(label='خیریه', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder price-input': 'خیریه / هیات', 'min': 0}), required=False, initial=0)
    sales_charity1 = forms.CharField(label='هیات', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder price-input': 'سفارشات', 'min': 0}), required=False, initial=0)
    sales_misc = forms.CharField(label='متفرقه', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder price-input': 'متفرقه', 'min': 0}), required=False, initial=0)
    total_sales = forms.CharField(label='جمع فروش', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder price-input': 'جمع فروش', 'min': 0}), required=False, initial=0)
    rent = forms.CharField(label='اجاره', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder price-input': 'اجاره', 'min': 0}), required=False, initial=0)
    salaries = forms.CharField(label='اضافه کاری/حقوق', widget=forms.TextInput(attrs={'class': 'form-control price-input', 'placeholder': 'حقوق', 'min': 0}), required=False, initial=0)
    hall = forms.CharField(label='سالن', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder price-input': 'اضافه کاری', 'min': 0}), required=False, initial=0)
    raw_materials = forms.CharField(label='مواد اولیه', widget=forms.TextInput(attrs={'class': 'form-control price-input', 'placeholder': 'مواد اولیه', 'min': 0}), required=False, initial=0)
    consumables = forms.CharField(label='مواد مصرفی', widget=forms.TextInput(attrs={'class': 'form-control price-input', 'placeholder': 'مواد مصرفی', 'min': 0}), required=False, initial=0)
    maintenance = forms.CharField(label='جاری', widget=forms.TextInput(attrs={'class': 'form-control price-input', 'placeholder': 'جاری', 'min': 0}), required=False, initial=0)
    delivery = forms.CharField(label='پیک', widget=forms.TextInput(attrs={'class': 'form-control price-input', 'placeholder': 'غذای پرسنل', 'min': 0}), required=False, initial=0)
    misc_expenses = forms.CharField(label='متفرقه', widget=forms.TextInput(attrs={'class': 'form-control price-input', 'placeholder': 'متفرقه', 'min': 0}), required=False, initial=0)
    total_expenses = forms.CharField(label='جمع هزینه‌ها', widget=forms.TextInput(attrs={'class': 'form-control price-input', 'placeholder': 'جمع هزینه‌ها', 'min': 0}), required=False, initial=0)
    monthly_profit = forms.CharField(label='سود ماهانه', widget=forms.TextInput(attrs={'class': 'form-control price-input', 'placeholder': 'سود ماهانه', 'min': 0}), required=False, initial=0)
    profit_percentage = forms.CharField(label='درصد سود', widget=forms.TextInput(attrs={'class': 'form-control price-input', 'placeholder': 'درصد سود', 'min': 0}), required=False, initial=0)
    cost_to_sales_ratio = forms.CharField(label='نسبت مواد به فروش', widget=forms.TextInput(attrs={'class': 'form-control price-input', 'placeholder': 'نسبت مواد به فروش', 'min': 0}), required=False, initial=0)

    class Meta:
        model = MonthlyReport
        exclude = ['date']
        
class ClaimsDebtsForm(forms.ModelForm):
    personal = forms.DecimalField(label='شخصی', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'شخصی', 'min': 0}), required=False, initial=0, max_digits=10, decimal_places=2)
    company = forms.DecimalField(label='شرکتی', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'شرکتی', 'min': 0}), required=False, initial=0, max_digits=10, decimal_places=2)
    specific_company = forms.DecimalField(label='شرکتی خاص', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'شرکتی خاص', 'min': 0}), required=False, initial=0, max_digits=10, decimal_places=2)
    
    market = forms.DecimalField(label='بازار', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'بازار', 'min': 0}), required=False, initial=0, max_digits=10, decimal_places=2)
    meat = forms.DecimalField(label='گوشت', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'گوشت', 'min': 0}), required=False, initial=0, max_digits=10, decimal_places=2)
    other = forms.DecimalField(label='متفرقه', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'متفرقه', 'min': 0}), required=False, initial=0, max_digits=10, decimal_places=2)
    staff = forms.DecimalField(label='کارکنان', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'کارکنان', 'min': 0}), required=False, initial=0, max_digits=10, decimal_places=2)
    
    total_claims = forms.DecimalField(label='جمع مطالبات', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'جمع مطالبات', 'min': 0}), required=False, initial=0, max_digits=10, decimal_places=2)
    total_debts = forms.DecimalField(label='جمع بدهی‌ها', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'جمع بدهی‌ها', 'min': 0, 'readonly': True}), required=False, initial=0, max_digits=10, decimal_places=2)
    level = forms.DecimalField(label='تراز', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'تراز', 'min': 0, 'readonly': True}), required=False, initial=0, max_digits=10, decimal_places=2)
    
    balance = forms.DecimalField(label='موجودی حساب', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'موجودی حساب', 'min': 0}), required=False, initial=0, max_digits=10, decimal_places=2)
    value_added_debt = forms.DecimalField(label='بدهی ارزش افزوده', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'بدهی ارزش افزوده', 'min': 0}), required=False, initial=0, max_digits=10, decimal_places=2)
    
    class Meta:
        model = ClaimDebt
        exclude = ['date']


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