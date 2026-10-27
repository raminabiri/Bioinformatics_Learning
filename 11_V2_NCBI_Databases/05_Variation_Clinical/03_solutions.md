<div dir="rtl">

# پاسخ تشریحی: dbSNP، ClinVar، dbVar، MedGen و GTR

همه‌ی خروجی‌ها واقعی‌اند (curl 8.20.0، EDirect 24.0، Variation Services v0؛ روی سرور دوره، 2026-10-27). شمار رکوردهای ClinVar هر ماه دگرگون می‌شود.

---

## پاسخ ۱: یک واریانت، همه‌ی جاها

<div dir="ltr">

```bash
curl -sS "$V/spdi/NC_000007.14:117559590:TCTT:T/all_equivalent_contextual" \
  | jq -r '.data.spdis[] | "\(.seq_id):\(.position):\(.deleted_sequence):\(.inserted_sequence)"'
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
NC_000007.14:117559590:TCTT:T
NC_000007.13:117199644:TCTT:T
NG_016465.4:98807:TCTT:T
NM_000492.4:1589:TCTT:T
NM_000492.3:1651:TCTT:T
```

</div>

(الف) **پنج** توالی: کروموزوم ۷ در GRCh38 (`NC_000007.14`) و GRCh37 (`NC_000007.13`)، RefSeqGene (`NG_016465.4`) و دو نسخه‌ی رونوشت.
(ب) در SPDI جایگاه از **آغاز mRNA** شمرده می‌شود: ۱۶۵۱ در `.3` و ۱۵۸۹ در `.4`؛ ‏۶۲ باز فرق. پس `.4` **۶۲ باز کمتر 5′ UTR** دارد. ‏`c.` از **کُدون آغاز** شمرده می‌شود و CDS در دو نسخه یکی است، پس `c.1521_1523del` در هر دو یکی می‌ماند. این همان فایده‌ی `c.` است: با دگرگونی UTR پایدار می‌ماند.

---

## پاسخ ۲: ‏Ile507del

<div dir="ltr">

```bash
curl -sS "$B/esummary.fcgi?db=snp&id=121908745" | grep -oE '<DOCSUM>[^<]*' | grep -oE 'NP_000483.3:p\.[A-Za-z0-9]*' | sort -u
elink -db snp -id 121908745 -target clinvar | esummary \
  | xtract -pattern DocumentSummary -element accession title -block germline_classification -element description review_status
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
NP_000483.3:p.Ile507del
VCV000007106	NM_000492.4(CFTR):c.1516ATC[1] (p.Ile507del)	Pathogenic	practice guideline
```

</div>

(الف) ‏**Pathogenic** با **practice guideline** (۴ ستاره)، مانند F508del. هر دو در پنل غربالگری رهنمود بالینی‌اند.
(ب) ‏`c.1516ATC[1]` نوشتار HGVS برای **تکرار**ها است: از جایگاه ۱۵۱۶ توالی `ATC` تکرار می‌شود، و در آلل جهش‌یافته تنها **یک** نسخه (`[1]`) از آن مانده است (در آلل مرجع دو نسخه: Ile506 و Ile507). ‏`c.1519_1521del` همان را با زبان حذف می‌گوید؛ و API هر دو را به یک SPDI (`1585:ATCATC:ATC`) می‌رساند (`c.1516ATC%5B1%5D` را به `/contextuals` دادیم: همان `NM_000492.4:1585:ATCATC:ATC`؛ `%5B` و `%5D` همان کروشه‌ها در نشانی‌اند، 11/01). نوشتار تکرار ساختار توالی را بهتر نشان می‌دهد؛ برای رایانه SPDI بی‌ابهام‌تر است.

---

## پاسخ ۳: ‏G551D، جهشی با یک دارو

<div dir="ltr">

```bash
esearch -db clinvar -query rs75527207 | esummary \
  | xtract -pattern DocumentSummary -element accession title -block germline_classification -element description review_status
curl -sS "$B/esummary.fcgi?db=snp&id=75527207" | grep -oE '<(CLINICAL_SIGNIFICANCE|SPDI)>[^<]*'
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
VCV001333303	NM_000492.4(CFTR):c.1652G>T (p.Gly551Val)	Likely pathogenic	criteria provided, single submitter
VCV000007120	NM_000492.4(CFTR):c.1652G>A (p.Gly551Asp)	Pathogenic	practice guideline
<CLINICAL_SIGNIFICANCE>pathogenic,drug-response,likely-pathogenic,not-provided
<SPDI>NC_000007.14:117587805:G:A,NC_000007.14:117587805:G:T
```

</div>

(الف) **دو** آلل در یک جایگاه (`G>A` و `G>T`) و **دو** رکورد ClinVar: ‏**G551D** (`c.1652G>A`) بیماری‌زا با ۴ ستاره، و **G551V** (`c.1652G>T`) «احتمالاً بیماری‌زا» تنها با گزارش یک آزمایشگاه (۱ ستاره). یک rs، دو سرنوشت بالینی؛ همان اشتباه رایج ۱.
(ب) ‏ClinVar برای هر واریانت چند **گونه** رده‌بندی جدا دارد؛ `germline_classification` تنها «این واریانت بیماری‌زاست؟» را می‌گوید. پاسخ به دارو در گزارش‌های جدا (SCVهایی با رده‌ی «drug response») ثبت می‌شود. ‏dbSNP همه‌ی رده‌های همه‌ی گزارش‌ها را در یک فیلد گرد آورده، پس `drug-response` را نشان می‌دهد. برای دیدن آن گزارش‌ها به صفحه‌ی VCV در ClinVar بروید (بخش «Submitted interpretations»).

---

## پاسخ ۴: ‏NR3C1 در ClinVar

<div dir="ltr">

```bash
for q in 'NR3C1[gene]' 'NR3C1[gene] AND clinsig_pathogenic[prop]' 'NR3C1[gene] AND clinsig_vus[prop]'; do
  echo "$(curl -sS -G "$B/esearch.fcgi" --data-urlencode db=clinvar --data-urlencode "term=$q" \
          | grep -oE '<Count>[^<]*' | head -1 | cut -d'>' -f2)  $q"; sleep 0.4
done
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
367  NR3C1[gene]
25  NR3C1[gene] AND clinsig_pathogenic[prop]
246  NR3C1[gene] AND clinsig_vus[prop]
```

</div>

(الف) ‏۳۶۷ رکورد، ۲۵ بیماری‌زا، ۲۴۶ VUS.
(ب) ‏VUS در NR3C1 **۶۷٪** (۲۴۶ از ۳۶۷) و در CFTR ‏۴۰٪. برای CFTR دهه‌ها پژوهش، کنسرسیوم‌های کارشناسی (CFTR2) و یک رهنمود بالینی هست؛ برای NR3C1 (بیماری کم‌یاب مقاومت به گلوکوکورتیکوئید) نه. هر چه ژن کم‌پژوهش‌تر، سهم «نمی‌دانیم» بیشتر.

---

## پاسخ ۵: واریانت ساختاری در دل ژن

<div dir="ltr">

```bash
esummary -db gene -id 1080 | xtract -pattern DocumentSummary -element Name -block GenomicInfoType -element ChrAccVer ChrStart ChrStop
awk 'BEGIN{print "gene:", 117668664-117480024+1; print "nsv7909578:", 117519332-117501896+1; print "offset:", 117501896-(117480024+1)}'
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
CFTR	NC_000007.14	117480024	117668664
gene: 188641
nsv7909578: 17437
offset: 21871
```

</div>

(الف) ‏Gene مختصات 0-based می‌دهد (11/01)، پس روی GRCh38: ‏**117480025..117668665**، به طول **۱۸۸٬۶۴۱** باز؛ رشته‌ی مثبت (آغاز < پایان).
(ب) ‏**۱۷٬۴۳۷** باز، نزدیک به **۲۱٫۹ هزار** باز پس از آغاز ژن. این‌جا تنها طول و فاصله را شمردیم؛ فرق یک بازی میان 0-based و 1-based در این عددها اثری ندارد. یک حذف ۱۷ هزار بازی در بخش آغازی ژن، احتمالاً یک یا چند اگزون آغازی را برمی‌دارد؛ برای دانستن دقیق، جای اگزون‌ها (رکورد GenBank ‏`NG_016465.4`، 11/02) را ببینید.

---

## پاسخ ۶: از بیماری به همه‌چیز

<div dir="ltr">

```bash
echo "medgen->clinvar $(curl -sS "$B/elink.fcgi?dbfrom=medgen&db=clinvar&id=41393" | grep -c '<Id>')"; sleep 0.4
echo "medgen->gtr $(curl -sS "$B/elink.fcgi?dbfrom=medgen&db=gtr&id=41393" | grep -c '<Id>')"
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
medgen->clinvar 5598
medgen->gtr 515
```

</div>

(الف) ‏۵۵۹۷ رکورد ClinVar و ۵۱۴ آزمون GTR (پس از کم کردن شناسه‌ی آغاز).
(ب) ‏`CFTR[gene]` همه‌ی واریانت‌های ژن را می‌آورد، با **هر** بیماری یا بی بیماری (مانند «not provided» یا «CFTR-related disorders»، ناباروری، پانکراتیت). پیوند MedGen تنها رکوردهایی است که **فیبروز کیستیک** را نام برده‌اند. از سوی دیگر، GTR از راه MedGen ‏۵۱۴ آزمون دارد ولی با `CFTR[gene] AND "Cystic fibrosis"[disname]` ‏۲۳۹: پیوند MedGen هر آزمونی را می‌آورد که این مفهوم را نام برده است، از جمله آزمون‌هایی که CFTR را در فیلد ژن نام نبرده‌اند. دو راه به یک بیماری، دو پاسخ؛ همیشه بگویید از کدام راه شمرده‌اید.

---

## پاسخ ۷ (اندیشیدنی): گزارش یک آزمایشگاه

**آنچه می‌توان گفت:**
- ‏F508del بیماری‌زاست، با بالاترین سطح بازبینی (۴ ستاره، رهنمود بالینی).
- فیبروز کیستیک **مغلوب** است: بیماری با **دو** آلل بیماری‌زا (یکی از هر والد) پدید می‌آید.
- واریانت دوم **VUS** با **۱ ستاره** است: یعنی یک آزمایشگاه آن را با معیار گفته‌شده «نامعلوم» دانسته؛ نه بیماری‌زا، نه بی‌خطر.

**آنچه نمی‌توان گفت:**
- این‌که بیمار CF دارد یا تنها **ناقل** است. با یک واریانت بیماری‌زا و یک VUS، تشخیص با پایگاه داده بسته نمی‌شود.
- این‌که دو واریانت روی **دو کروموزوم** گوناگون‌اند (cis/trans)؛ این را تنها آزمایش والدین می‌گوید.

پاسخ درست به همراه بیمار: «این پرسش را باید پزشک و مشاور ژنتیک با یافته‌های بالینی (مانند آزمون عرق) و آزمایش والدین پاسخ دهند.» تفسیر رسمی چنین گزارشی (معیارهای ACMG) موضوع دوره‌ی جدای ژنومیکس پزشکی است.

---

## برای خواندن بیشتر

- ‏Landrum MJ, et al. (2018). *ClinVar.* Nucleic Acids Res 46:D1062–D1067. https://doi.org/10.1093/nar/gkx1153
- ‏Holmes JB, et al. (2020). *SPDI.* Bioinformatics 36:1902–1907. https://doi.org/10.1093/bioinformatics/btz856
- ‏HGVS Nomenclature (تکرارها و قاعده‌ی ۳′): https://hgvs-nomenclature.org/
- ‏YouTube: *GenomeConnect and ClinVar Webinar* (ClinGen Resource): https://www.youtube.com/watch?v=Pty0vW9CkEE

</div>
