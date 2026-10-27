<div dir="rtl">

# ماژول ۰۵: هستی‌شناسی ژن و پایگاه‌های مسیر (GO, KEGG, Reactome, WikiPathways, MSigDB) — نسخه‌ی ۲

| | |
| :--- | :--- |
| **بخش** | `12_V2_Global_Databases_Browsers` |
| **پیش‌نیاز** | ماژول‌های [12/01](../01_Ensembl_BioMart/) (هشت ژن و شناسه‌هایشان) و [12/04](../04_Protein_Families_Domains/) (دامنه‌ها)؛ `curl`، `jq`، `awk` |
| **زمان تقریبی** | ۳ ساعت (یک درس، نزدیک به ۹۰ دقیقه، و تمرین‌ها) |
| **ابزار** | ‏QuickGO API، KEGG REST، Reactome (release 97؛ Content و Analysis Service)، WikiPathways JSON، MSigDB (2026.2.Hs)؛ AmiGO و جست‌وجوی MSigDB (وب، ✍️) |
| **داده** | هشت ژن پاسخ به دگزامتازون (NR3C1، FKBP5، TSC22D3، ZBTB16، PER1، DUSP1، KLF15، CRISPLD2)؛ rpoB، gyrA و acrB ‏*E. coli* |
| **منابع رایانه** | تنها درخواست وب (بزرگ‌ترین فایل ۱۲ مگابایت) |
| **وضعیت** | ✅ اجرا شده (2026-10-27)؛ جست‌وجوی MSigDB ✍️ (نام‌نویسی) |

## اهداف یادگیری
پس از این ماژول می‌توانید:
1. سه شاخه‌ی GO، ساختار گرافی و کدهای شاهد را بخوانید و آنوتیشن‌های یک پروتئین را از QuickGO بگیرید.
2. ژن‌ها را در KEGG (KO و مسیر)، Reactome و WikiPathways دنبال کنید.
3. مجموعه‌ژن‌های MSigDB را بگیرید و با فهرست خود بسنجید.
4. یک تحلیل غنی‌سازی کوچک بزنید و دام‌های آن (ایزوفرم‌ها، پوشش پایگاه) را بشناسید؛ پیش‌زمینه‌ی بخش ۱۴.

## ترتیب مطالعه
1. ‏[01_lesson.md](01_lesson.md): درس؛ GO و QuickGO، KEGG، Reactome و ORA، WikiPathways، MSigDB.
2. ‏[02_exercises.md](02_exercises.md): ۷ تمرین؛ زیر عنوان هر تمرین راهنمایی آمده است.
3. ‏[03_solutions.md](03_solutions.md): پاسخ تشریحی.

## ورودی و خروجی
- **ورودی:** [`dex8_symbols.txt`، `dex8_ids.tsv`، `hallmark_names.txt`](../99_scripts_data/05_Pathway_Ontology_Resources/data/).
- **خروجی:** `gr_go.json`، `dex_path.tsv`، `ora.json`، `wp_hs.tsv`، پوشه‌ی `hall/`؛ ورودی بخش ۱۴ (غنی‌سازی).

</div>
