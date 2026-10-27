<div dir="rtl">

# پاسخ تشریحی: PubMed، MeSH، PMC و PubTator3

همه‌ی خروجی‌ها واقعی‌اند (curl 8.20.0، EDirect 24.0، jq؛ روی سرور دوره، 2026-10-27). شمار مقاله‌ها هر روز بالا می‌رود.

---

## پاسخ ۱: سرعنوان دوم

<div dir="ltr">

```bash
esearch -db mesh -query '"Drug Resistance, Bacterial"[MeSH Terms]' | esummary \
  | xtract -pattern DocumentSummary -element Id -block DS_IdxLinks -element TreeNum | head -2
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
68024881	G06.099.225	G06.225.347	G07.690.773.984.269.347
```

</div>

(الف) ‏UID ‏`68024881` → سرعنوان **D024881** (همان قاعده‌ی `68` + شماره).
(ب) **سه** شماره‌ی درخت، همه با `G`: شاخه‌ی **پدیده‌ها و فرایندها** (Phenomena and Processes). ‏Rifampin در `D` است: شاخه‌ی **مواد شیمیایی و داروها**. درخت MeSH شانزده شاخه‌ی اصلی دارد (A آناتومی، B جانداران، C بیماری‌ها، D داروها، G فرایندها، …)؛ یک جست‌وجوی خوب بیشتر وقت‌ها از چند شاخه سرعنوان می‌گیرد: یک دارو (D)، یک فرایند (G)، یک جاندار (B).

---

## پاسخ ۲: موضوع اصلی

<div dir="ltr">

```bash
for q in '"Rifampin"[MeSH Terms] AND "Drug Resistance, Bacterial"[MeSH Terms]' \
         '"Rifampin"[MeSH Major Topic] AND "Drug Resistance, Bacterial"[MeSH Major Topic]'; do
  echo "$(curl -sS -G "$B/esearch.fcgi" --data-urlencode db=pubmed --data-urlencode "term=$q" | grep -oE '<Count>[^<]*' | head -1 | cut -d'>' -f2) | $q"
  sleep 0.4
done
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
2938 | "Rifampin"[MeSH Terms] AND "Drug Resistance, Bacterial"[MeSH Terms]
719 | "Rifampin"[MeSH Major Topic] AND "Drug Resistance, Bacterial"[MeSH Major Topic]
```

</div>

(الف) ‏۲۹۳۸ در برابر **۷۱۹** (یک‌چهارم).
(ب) برای مرور کوتاه، `[MeSH Major Topic]`: مقاله‌هایی که **درباره‌ی** مقاومت به ریفامپیسین‌اند. چیزی که از دست می‌دهید: مقاله‌هایی که مقاومت به ریفامپیسین را **در کنار** موضوع دیگری کاویده‌اند (مانند یک مقاله‌ی اپیدمیولوژی سل که چند دارو را سنجیده)، و همه‌ی مقاله‌های تازه‌ی هنوز نمایه‌نشده.

---

## پاسخ ۳: ‏۱۱۵ مقاله در گذر زمان

<div dir="ltr">

```bash
awk -F'\t' '{d=int($2/10)*10; c[d]++} END{for(k in c) print k"s", c[k]}' pm.tsv | sort
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
1970s 8
1980s 35
1990s 17
2000s 13
2010s 26
2020s 16
```

</div>

(الف) ‏۱۹۷۰ها ۸، ‏**۱۹۸۰ها ۳۵**، ۱۹۹۰ها ۱۷، ۲۰۰۰ها ۱۳، ۲۰۱۰ها ۲۶، ۲۰۲۰ها ۱۶ (جمع ۱۱۵).
(ب) دهه‌ی ۱۹۸۰. در آن دوره ژنتیک کلاسیک باکتری (جداسازی جهش‌یافته‌های مقاوم به ریفامپیسین، نقشه‌برداری و نخستین تعیین توالی ژن‌ها) اوج داشت و rpoB *E. coli* الگوی اصلی بود (همان *Mol Gen Genet* و *J Bacteriol* گام ۳). اوج دوم در ۲۰۱۰ها با تعیین توالی ژنوم و پژوهش‌های **تکامل آزمایشگاهی** مقاومت می‌آید. (`int($2/10)*10` سال را به آغاز دهه گرد می‌کند: 1987 → 1980.)

---

## پاسخ ۴: فهرست منابع این درس

<div dir="ltr">

```bash
curl -sS "https://api.ncbi.nlm.nih.gov/lit/ctxp/v1/pubmed/?format=ris&id=28009073,11290327" > refs.ris
grep -c '^TY' refs.ris
grep -E '^(TY|T1|PY|DO|ER)' refs.ris | cut -c1-90
curl -sS "https://api.ncbi.nlm.nih.gov/lit/ctxp/v1/pubmed/?format=citation&id=28009073" | jq -r '.ama.orig'
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
2
TY  - JOUR
T1  - Structural basis for rifamycin resistance of bacterial RNA polymerase by the three m
DO  - 10.1111/mmi.13606
ER  - 
TY  - JOUR
T1  - Structural mechanism for rifampicin inhibition of bacterial rna polymerase
DO  - 10.1016/s0092-8674(01)00286-0
ER  - 
Molodtsov V, Scharf NT, Stefan MA, Garcia GA, Murakami KS. Structural basis for rifamycin resistance of bacterial RNA polymerase by the three most clinically important RpoB mutations found in Mycobacterium tuberculosis. Mol Microbiol. 2017;103(6):1034-1045. doi:10.1111/mmi.13606
```

</div>

(الف) **دو** رکورد؛ `TY` آغاز هر رکورد و `ER` پایانش است، `T1` عنوان و `DO` DOI. برچسب `PY` در این خروجی **نیست**: سال در برچسب دیگری (مانند `Y1` یا `DA`) آمده است؛ پیش از بردن به نرم‌افزار منابع، یک بار فایل را ببینید.
(ب) با مرجع 09/01 (Molodtsov V, Scharf NT, Stefan MA, Garcia GA, Murakami KS (2017) … Molecular Microbiology 103:1034–1045) یکی است؛ تنها سبک فرق دارد (AMA شماره‌ی هر جلد مجله، `(6)`، را هم می‌آورد). در عنوان Campbell در RIS، «rna» کوچک نوشته شده: PubMed گاهی بزرگی حرف‌ها را ساده می‌کند؛ پیش از چاپ، عنوان‌ها را با مقاله بسنجید.

---

## پاسخ ۵: PubTator روی مقاله‌ی دیگر

<div dir="ltr">

```bash
curl -sS "$P3/publications/export/biocjson?pmids=11290327" \
  | jq -r '.PubTator3[0].passages[] | .annotations[] | "\(.infons.type)\t\(.text)\t\(.infons.identifier // "-")"' \
  | sort | uniq -c | sort -k2,2 -k1,1nr
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
      3 Chemical	Rif	MESH:D012293
      1 Chemical	rifampicin	MESH:D012293
      1 Chemical	Rifampicin	MESH:D012293
      1 Disease	tuberculosis	MESH:D014376
      1 Species	Thermus aquaticus	271
```

</div>

(الف) تنها دارو (سه نوشتار، یک شناسه)، یک بیماری و یک جاندار. **هیچ ژن و هیچ جهشی** یافت نشد: چکیده از «RNA polymerase» و «β subunit» می‌گوید، نه از نام ژن `rpoB`؛ و جهشی را با الگوی حرف-عدد-حرف نام نمی‌برد. ‏PubTator تنها همان را می‌یابد که در متن هست.
(ب) ‏***Thermus aquaticus*** (TaxID 271): ساختار بلوری Campbell از RNA پلیمراز این باکتری گرمادوست بود، نه *E. coli* (پروتئین‌های گرمادوست آسان‌تر بلور می‌شوند). نتیجه درباره‌ی جایگاه ریفامپیسین به *E. coli* و *M. tuberculosis* گسترش داده شد، چون این جایگاه در همه‌ی باکتری‌ها حفظ‌شده است.

---

## پاسخ ۶: دو شماره‌گذاری در یک متن

<div dir="ltr">

```bash
grep -c 'S450L' pmc.xml
grep -oE '.{60}S450L.{40}' pmc.xml | head -2
for t in "rpoB%20S531L" "rpoB%20S450L" "rpoB%20S531L%20OR%20rpoB%20S450L"; do
  echo "$(curl -sS "$P3/search/?text=$t&page=1" | jq -r '.count') $t"; sleep 1
done
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
2
n in the RRDR cluster I (D516V/D435V, H526Y/H445Y and S531L/S450L in <italic toggle="yes">E. coli</italic
AP were also classified into the same groups; the D435V and S450L mutants are less sensitive to RMP (IC<s
379 rpoB%20S531L
319 rpoB%20S450L
319 rpoB%20S531L%20OR%20rpoB%20S450L
```

</div>

(الف) نویسندگان هر جهش را **جفت** نوشته‌اند: `S531L/S450L` «در *E. coli* و *M. tuberculosis*». ‏`grep -c` سطرها را می‌شمارد (۲)، نه نام‌بُردها (۳ در درس، که `grep -o` بود): یک سطر دو بار S450L دارد.
(ب) دو جست‌وجو، ۳۷۹ و ۳۱۹ مقاله. ولی `… OR …` همان **۳۱۹** را داد، نه بیشتر: جست‌وجوی PubTator3 مانند PubMed با `OR` بولی رفتار نمی‌کند (یا آن را جور دیگری می‌فهمد). راه مطمئن: دو جست‌وجوی جدا، و یکی کردن فهرست PMIDها (`sort -u`). درس: **پیش از اعتماد به عملگرهای یک ابزار تازه، با یک پرسش با پاسخ معلوم بیازماییدشان.**

---

## پاسخ ۷ (اندیشیدنی): بخش «روش جست‌وجو» یک مرور

نمونه:

> «جست‌وجو در PubMed در 2026-10-27 با پرسش `rpoB[tiab] AND (rifampicin[tiab] OR rifampin[tiab]) AND "Escherichia coli"[MeSH Terms]` انجام شد (۱۱۵ رکورد). دو املای rifampicin و rifampin در عنوان و چکیده جست‌وجو شد، چون سرعنوان MeSH «Rifampin» تنها رکوردهای نمایه‌شده را می‌پوشاند. هیچ محدودیت زبان یا سال گذاشته نشد. رکوردها با E-utilities (efetch، XML) گرفته و با EDirect 24.0 جدول شدند؛ فهرست PMIDها در پیوست ۱ است.»

باید در آن باشد: **تاریخ** اجرا، **پرسش کامل** با برچسب‌ها، **شمار** نتیجه، **پایگاه** (و اگر چند پایگاه، هر کدام)، محدودیت‌ها (زبان، سال، گونه‌ی انتشار)، ابزار و نسخه، و **فهرست شناسه‌ها**. بی تاریخ و فهرست PMID، کسی همان ۱۱۵ را دوباره نمی‌یابد، چون PubMed هر روز رکورد تازه می‌گیرد و ATM هم دگرگون می‌شود.

---

## برای خواندن بیشتر

- ‏Wei CH, et al. (2024). *PubTator 3.0.* Nucleic Acids Res 52:W540–W546. https://doi.org/10.1093/nar/gkae235
- ‏Cochrane Handbook، فصل ۴ (جست‌وجو و گزینش مطالعه‌ها): https://training.cochrane.org/handbook
- ‏YouTube: *This MeSH tutorial will dramatically improve your literature search on PubMed*: https://www.youtube.com/watch?v=7fWFupz0LVA

</div>
