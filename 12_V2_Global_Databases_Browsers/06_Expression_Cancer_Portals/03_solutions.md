<div dir="rtl">

# پاسخ تشریحی: درگاه‌های بیان و سرطان

همه‌ی خروجی‌ها واقعی‌اند (GTEx API v2، HPA 25.1، Expression Atlas، GDC Release 46.0، cBioPortal v7.2.0؛ روی سرور دوره، 2026-10-27).

---

## پاسخ ۱: ‏FKBP5 در بافت‌ها

<div dir="ltr">

```bash
id=$(curl -sS "$G/reference/gene?geneId=FKBP5&gencodeVersion=v47" | jq -r '.data[0].gencodeId'); echo $id
curl -sS "$G/expression/medianGeneExpression?gencodeId=$id&datasetId=gtex_v11&itemsPerPage=100" \
  | jq -r '.data[] | "\(.median)\t\(.tissueSiteDetailId)"' | sort -gr | sed -n '1,3p;$p'
curl -sS "https://www.proteinatlas.org/ENSG00000096060.json" \
  | jq -r '["RNA tissue specificity", "RNA single cell type specific nCPM", "Subcellular main location"][] as $k | "\($k)\t\(.[$k] | tostring | .[0:120])"'
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
ENSG00000096060.15
179.68	Muscle_Skeletal
170.455	Esophagus_Muscularis
168.197	Nerve_Tibial
1.43119	Brain_Cerebellar_Hemisphere
RNA tissue specificity	Tissue enhanced
RNA single cell type specific nCPM	{"Innate lymphoid cells":"1778.0","Monocyte progenitors":"2488.9","Neutrophils":"5747.7","Podocytes":"1716.6","Proximal 
Subcellular main location	["Nucleoplasm"]
```

</div>

(الف) بیشترین در **ماهیچه‌ی اسکلتی** (۱۸۰ TPM)، ماهیچه‌ی مری و عصب؛ کمترین در **مخچه** (۱٫۴). دامنه **۱۲۶ برابر** است؛ برای NR3C1 تنها ۱۱ برابر (۴٫۹ تا ۵۲). گیرنده همه‌جا هست، ولی هدفش در بافت‌ها بسیار گوناگون است.
(ب) ‏«Tissue enhanced»: در برخی بافت‌ها بسیار بیشتر از میانگین. در تک‌سلول، بیشینه در **نوتروفیل‌ها** (۵۷۴۸ nCPM). جای سلولی: هسته (nucleoplasm).

---

## پاسخ ۲: آلبوترول و ترکیب دو دارو

<div dir="ltr">

```bash
awk -F'\t' '$2 ~ /^(NR3C1|FKBP5|TSC22D3|ZBTB16|PER1|DUSP1|KLF15|CRISPLD2)$/ {print $2 "\t" $4 "\t" $3 "\t" $6 "\t" $5}' e52778.tsv | sort
for c in 3 5 7; do
  awk -F'\t' -v c=$c 'NR > 1 && $c != "NA" && $c < 0.05 {n++} END {print "column", c, "significant:", n+0}' e52778.tsv
done
```

</div>

**خروجی واقعی** (ستون‌ها: ژن، log2FC آلبوترول، p آلبوترول، log2FC ترکیب، p ترکیب):

<div dir="ltr">

```
CRISPLD2	0.4	0.995443999658801	1.2	0.00177429420725912
DUSP1	0.4	0.995443999658801	1	0.0159474389922289
FKBP5	0.3	0.995443999658801	0.7	0.069580661931686
KLF15	0.4	0.995443999658801	0.6	0.0855332849236811
NR3C1	-0.2	0.995443999658801	-0.4	0.566090941079728
PER1	0.9	0.196802839876097	1.4	7.95037410602871e-05
TSC22D3	0.4	0.995443999658801	0.6	0.145241849276111
ZBTB16	0.3	0.995443999658801	0.4	0.21968086817836
column 3 significant: 0
column 5 significant: 83
column 7 significant: 2142
```

</div>

(الف) آلبوترول به تنهایی: **هیچ** ژنی با p زیر ۰٫۰۵. بیشترین log2FC از هشت ژن ما **PER1** ‏(۰٫۹) است. جور است: آلبوترول گیرنده‌ی بتا-۲ را فعال می‌کند و **cAMP** را بالا می‌برد؛ و PER1 ژنی است که با cAMP (از راه عامل CREB) روشن می‌شود. ولی این اثر کوچک و ناپایدار است.

(ب) **انتظار:** چون آلبوترول به تنهایی کمابیش بی‌اثر است، ترکیب دو دارو باید همانند دگزامتازون تنها اثر بگذارد. **Expression Atlas** اما تنها **۸۳** ژن معنادار برای ترکیب می‌دهد (در برابر ۲۱۴۲ برای دگزامتازون) و FKBP5 تنها ۰٫۷ و ZBTB16 تنها ۰٫۴.

ما همین مقایسه را با جدول شمارش NCBI و اسکریپت `geo_counts.py` ماژول 11/04 (در `11_V2_NCBI_Databases/99_scripts_data/04_GEO/scripts/`، با همان دو فایل درس 11/04) زدیم:

<div dir="ltr">

```bash
python3 geo_counts.py GSE52778_series_matrix.txt.gz counts.tsv.gz Albuterol_Dexamethasone Untreated 2908 2289 7704 1843 | sed -n '/selected genes/,/^$/p'
```

</div>

<div dir="ltr">

```
selected genes (Albuterol_Dexamethasone vs Untreated):
        mean_cpm_Untreated  mean_cpm_Albuterol_Dexamethasone  mean_log2FC  lines_up
GeneID                                                                             
2908                 179.3                             128.5        -0.50         1
2289                  15.1                             158.3         2.78         4
7704                   0.8                              79.9         4.44         4
1843                  36.9                             144.1         1.60         4 
```

</div>

در شمارش‌های NCBI، ترکیب دو دارو FKBP5 را ۲٫۷۸ و ZBTB16 را ۴٫۴۴ (log2) بالا می‌برد، **در هر چهار فرد**؛ نزدیک به دگزامتازون تنها. پس پاسخ Expression Atlas برای این یک مقایسه با داده‌ی خام **جور نیست**. ما فایل طرح آزمایش Atlas را هم دیدیم: نمونه‌ها درست به گروه‌ها داده شده‌اند (برای هر فرد: بی‌تیمار، دگزامتازون، آلبوترول، ترکیب). علت را نیافتیم. **درس:** بازتحلیل‌های آماده بسیار سودمندند، ولی وقتی یک نتیجه با زیست‌شناسی یا با نگاه ساده‌ی خودتان جور نیست، به داده‌ی خام برگردید. در بخش ۱۳ همین مقایسه را با DESeq2 می‌زنید و داوری می‌کنید.

---

## پاسخ ۳: نسخه‌ی شناسه

<div dir="ltr">

```bash
id=$(curl -sS "$G/reference/gene?geneId=NR3C1&gencodeVersion=v26" | jq -r '.data[0].gencodeId'); echo $id
curl -sS -w '\nHTTP %{http_code}\n' "$G/expression/medianGeneExpression?gencodeId=$id&datasetId=gtex_v11"
curl -sS "$G/expression/medianGeneExpression?gencodeId=$id&datasetId=gtex_v8&itemsPerPage=100" \
  | jq -r '.data | length, (.[] | select(.tissueSiteDetailId == "Lung") | "\(.median)\tLung (v8)")'
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
ENSG00000113580.14
{"data":[],"paging_info":{"numberOfPages":0,"page":0,"maxItemsPerPage":250,"totalNumberOfItems":0}}
HTTP 200

54
24.7418	Lung (v8)
```

</div>

پاسخ **تهی** است، با کد **200** (نه خطا!). ‏GTEx v11 شناسه‌ی `.14` (GENCODE v26) را نمی‌شناسد و چیزی نمی‌یابد. این از خطای آشکار بدتر است: اسکریپتی که تنها کد پاسخ را می‌سنجد (12/01، تابع `ask`) آن را درست می‌پندارد. درست کردن: شناسه را با همان نسخه‌ی GENCODE داده بگیرید (v47 برای gtex_v11)، یا داده‌ی هم‌نسخه (gtex_v8) را بخواهید. با v8 همه‌ی ۵۴ بافت آمد؛ ریه ۲۴٫۷ TPM (در v11 ‏۲۶٫۳). همیشه شمار سطرهای پاسخ را هم بسنجید.

---

## پاسخ ۴: امضای جهشی در دو سرطان

<div dir="ltr">

```bash
curl -sS -X POST -H "Content-Type: application/json" \
  "$C/molecular-profiles/coadread_tcga_pan_can_atlas_2018_mutations/mutations/fetch?projection=DETAILED" \
  -d '{"entrezGeneIds": [7157], "sampleListId": "coadread_tcga_pan_can_atlas_2018_all"}' > tp53_crc.json
for f in tp53_luad.json tp53_crc.json; do
  echo -n "$f: "
  jq -r '.[] | select(.variantType == "SNP") | "\(.referenceAllele)>\(.variantAllele)"' $f \
  | awk '{m = $1; if (m == "G>T" || m == "C>A") t = "G>T"; else if (m == "G>A" || m == "C>T") t = "C>T"; else t = "other"; c[t]++; n++}
         END {printf "SNVs=%d  G>T=%.0f%%  C>T=%.0f%%  other=%.0f%%\n", n, 100*c["G>T"]/n, 100*c["C>T"]/n, 100*c["other"]/n}'
done
jq -r '.[].proteinChange' tp53_crc.json | sort | uniq -c | sort -rn | head -4
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
tp53_luad.json: SNVs=281  G>T=43%  C>T=27%  other=30%
tp53_crc.json: SNVs=292  G>T=12%  C>T=71%  other=18%
     32 R175H
     20 R282W
     18 R248Q
     17 R273H
```

</div>

**تکه‌به‌تکه:** حلقه‌ی `for` (01/09) همان دستور را روی دو فایل می‌زند. ‏G>T و C>A یک جهش‌اند که روی دو رشته‌ی DNA دیده شده‌اند؛ پس با هم شمرده می‌شوند.

(الف) ریه: **G>T ‏۴۳٪**، C>T ‏۲۷٪. روده‌ی بزرگ: G>T تنها ۱۲٪ و **C>T ‏۷۱٪**.
(ب) در روده‌ی بزرگ چهار جهش پرتکرار **R175H، R282W، R248Q، R273H** هستند، همه از C>T (یا G>A). این جهش‌ها در **CpG** هستند: C متیل‌دار در CpG خودبه‌خود به T **دآمینه** می‌شود (امضای «پیری»، SBS1). در ریه، دود تنباکو G>T می‌سازد (R273L، R158L، G245V؛ درس). یک ژن، دو بافت، دو فرایند سازنده‌ی جهش.

---

## پاسخ ۵: ‏KRAS در ریه

<div dir="ltr">

```bash
curl -sS -X POST -H "Content-Type: application/json" "$C/molecular-profiles/luad_tcga_pan_can_atlas_2018_mutations/mutations/fetch" \
  -d '{"entrezGeneIds": [3845], "sampleListId": "luad_tcga_pan_can_atlas_2018_all"}' > kras.json
jq '[.[].sampleId] | unique | length' kras.json
jq -r '.[].proteinChange' kras.json | sort | uniq -c | sort -rn | head -4
jq -r '[.[].sampleId] | unique | .[]' kras.json | sort > kras_s.txt
jq -r '[.[].sampleId] | unique | .[]' tp53_luad.json | sort > tp53_s.txt
comm -12 kras_s.txt tp53_s.txt | wc -l
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
168
     70 G12C
     40 G12V
     20 G12D
     17 G12A
62
```

</div>

‏`comm -12` تنها سطرهایی را چاپ می‌کند که در **هر دو** فایل مرتب‌شده هستند.

(الف) ‏۱۶۸ از ۵۶۶ = **۲۹٫۷٪**. پرتکرارترین **G12C** (‏۷۰). ‏G12C از جانشینی G>T است (GGT → TGT)، باز همان امضای دود. ‏G12C امروز هدف داروهای ویژه است (sotorasib، adagrasib).
(ب) **۶۲** نمونه (۱۱٪ همه‌ی نمونه‌ها) هر دو را دارند.

---

## پاسخ ۶: داده‌ی باز در TCGA-BRCA

<div dir="ltr">

```bash
F='{"op":"in","content":{"field":"cases.project.project_id","value":["TCGA-BRCA"]}}'
curl -sS -G "$GD/files" --data-urlencode "filters=$F" --data-urlencode "facets=access" --data-urlencode "size=0" \
  | jq -r '.data.aggregations.access.buckets[] | "\(.doc_count)\t\(.key)"'
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
43492	controlled
27931	open
```

</div>

‏۴۳٬۴۹۲ کنترل‌شده و ۲۷٬۹۳۱ باز: **۶۱٪** کنترل‌شده (TCGA-LUAD ‏۶۲٪). نسبت در پروژه‌های TCGA نزدیک به هم است، چون هر بیمار همان گونه فایل‌ها را دارد (BAMها و جهش‌های خام کنترل‌شده؛ بیان، جهش‌های پالایش‌شده و داده‌ی بالینی باز). ‏BRCA بزرگ‌ترین پروژه‌ی TCGA است و پس بیشترین فایل را دارد.

---

## پاسخ ۷ (فکری): پایان‌نامه با داده‌ی TCGA

| خواسته | منبع | داده‌ی کنترل‌شده؟ |
| :--- | :--- | :--- |
| ۱. بیان FKBP5 در تومور و بافت سالم ریه | ‏cBioPortal یا GDC (بیان باز TCGA؛ نمونه‌های بافت سالم کنار تومور)؛ GTEx برای بافت سالم بیشتر | **نه** |
| ۲. جهش TP53 و بقا | ‏cBioPortal (جهش‌های سوماتیک پالایش‌شده و داده‌ی بالینی؛ برگه‌ی Survival) | **نه** |
| ۳. واریانت‌های **ارثی** در ژن‌های ترمیم DNA | فایل‌های واریانت germline یا BAM بافت سالم بیماران در GDC | **بله**؛ درخواست dbGaP ‏(phs000178) |

**نکته‌های اخلاقی:** (۱) واریانت‌های ارثی فرد را **شناسایی‌پذیر** می‌کنند و برای خانواده‌اش هم آگاهی سلامت دارند؛ برای همین کنترل‌شده‌اند. (۲) پس از تأیید dbGaP، داده تنها روی رایانه‌ی امن نهاد و تنها برای همان طرح تأییدشده به کار می‌رود؛ نه در گیت‌هاب، نه در ابر عمومی، نه برای همکار بیرون از طرح. (۳) در گزارش، داده را در سطح **گروه** بنویسید، نه فرد. (۴) درخواست ماه‌ها طول می‌کشد؛ زود آغاز کنید. جزئیات بیشتر در دوره‌ی جداگانه‌ی ژنومیک پزشکی.

</div>
