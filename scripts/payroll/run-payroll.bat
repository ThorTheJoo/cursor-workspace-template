@echo off
REM Convert Nett Pay List XLS to FNB Payment CSV (standalone payroll)
python scripts\payroll\netpay_to_payment_csv.py %*
echo Output in reports\payroll\
