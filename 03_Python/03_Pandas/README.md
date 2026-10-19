# ماژول 02: پردازش جدول‌ها با pandas و NumPy (Data Wrangling with pandas & NumPy)

| | |
| :--- | :--- |
| **بخش** | `03_Python` |
| **پیش‌نیاز** | 01_Python_Biopython |
| **زمان تقریبی** | ۶ ساعت |
| **ابزارها** | pandas، NumPy، matplotlib، seaborn |
| **داده (پیشنهادی)** | گزارش‌های fastp/MultiQC و `ground_truth.tsv` بخش ۰۶ |
| **وضعیت** | ⚪ طراحی‌شده — سرفصل و اهداف مشخص است؛ درس طبق [STYLE_GUIDE](../../STYLE_GUIDE.md) نوشته و تست خواهد شد |

## اهداف یادگیری
پس از این ماژول می‌توانید:
1. جدول‌های خروجی ابزارها را بخوانید، پاک‌سازی و ادغام کنید (tidy data).
2. group-by و pivot برای خلاصه‌سازی نمونه‌ها انجام دهید.
3. نمودار انتشارپذیر با matplotlib/seaborn بسازید.

## سرفصل درس
1. DataFrame، انواع داده، ایندکس
2. خواندن TSV/JSON (گزارش fastp) و ادغام با metadata
3. tidy data، melt/pivot، groupby
4. NumPy برای محاسبات برداری
5. نمودار: توزیع، heatmap، stacked bar فراوانی

## تمرین‌های برنامه‌ریزی‌شده
- ساخت جدول QC همه‌ی نمونه‌ها از JSONهای fastp (هم‌ارز تمرین ۶ ماژول 06/01 با jq)
- نمودار stacked bar ترکیب ground truth دو نمونه
- (چالشی) تابع مقایسه‌ی یک پروفایل تاکسونومیک با ground truth (precision/recall/L1 distance)
