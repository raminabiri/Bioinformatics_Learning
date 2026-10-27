<div dir="rtl">

# پاسخ تشریحی: هستی‌شناسی ژن و پایگاه‌های مسیر

همه‌ی خروجی‌ها واقعی‌اند (QuickGO، KEGG REST، Reactome 97، WikiPathways؛ روی سرور دوره، 2026-10-27). شمار آنوتیشن‌ها و مسیرها با هر نسخه‌ی تازه عوض می‌شود.

---

## پاسخ ۱: ‏GO برای FKBP5

<div dir="ltr">

```bash
curl -sS -H "$H" "$Q/annotation/search?geneProductId=Q13451&limit=200" > fk_go.json
jq '.numberOfHits' fk_go.json
jq -r '.results[].goAspect' fk_go.json | sort | uniq -c
ids=$(jq -r '[.results[] | select(.goAspect == "molecular_function") | .goId] | unique | join(",")' fk_go.json)
curl -sS -H "$H" "$Q/ontology/go/terms/$ids" | jq -r '.results[] | "\(.id)\t\(.name)"' > fk_mf.tsv
jq -r '.results[] | select(.goAspect == "molecular_function") | "\(.goId)\t\(.goEvidence)"' fk_go.json | sort | uniq -c \
  | awk 'NR == FNR {split($0, a, "\t"); n[a[1]] = a[2]; next} {print $1 "\t" $2 "\t" $3 "\t" n[$2]}' fk_mf.tsv - | sort -rn | head -8
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
81
      4 biological_process
     12 cellular_component
     65 molecular_function
57	GO:0005515	IPI	protein binding
1	GO:0031072	IPI	heat shock protein binding
1	GO:0031072	IEA	heat shock protein binding
1	GO:0030674	IDA	protein-macromolecule adaptor activity
1	GO:0005528	TAS	FK506 binding
1	GO:0005528	IEA	FK506 binding
1	GO:0003755	IEA	peptidyl-prolyl cis-trans isomerase activity
1	GO:0003755	IDA	peptidyl-prolyl cis-trans isomerase activity
```

</div>

**تکه‌به‌تکه:** ‏`uniq -c` شمار هر جفت «اصطلاح + کد» را در ستون نخست می‌گذارد؛ پس در `awk` فایل دوم، ‏`$2` شناسه و `$3` کد است. ‏`split($0, a, "\t")` سطرهای `fk_mf.tsv` را در Tab می‌شکند.

(الف) ‏۸۱ آنوتیشن: ۶۵ MF، ۱۲ CC، تنها ۴ BP.
(ب) ‏**«protein binding»** با IPI، **۵۷ بار** از ۶۵: هر آزمایش برهم‌کنش (مانند پویش‌های گسترده‌ی دوهیبریدی) یک آنوتیشن جدا ساخته است. این اصطلاح **کمابیش هیچ** آگاهی‌ای نمی‌دهد: بیشتر پروتئین‌ها به چیزی می‌چسبند. اصطلاح‌های آگاهی‌بخش:
- ‏**heat shock protein binding** (IPI): چسبیدن به Hsp90. ✅
- ‏**peptidyl-prolyl cis-trans isomerase activity** (IDA): کار آنزیمی خانواده‌ی FKBP (چرخاندن پیوند پرولین).
- ‏**FK506 binding**: دارویی (تاکرولیموس) که نام خانواده از آن است.

**درس:** در شمارش آنوتیشن‌ها (و در غنی‌سازی GO، بخش ۱۴) اصطلاح‌های بسیار کلی مانند «protein binding» را کنار بگذارید یا جدا ببینید.

---

## پاسخ ۲: چند درصد آزمایشی؟

<div dir="ltr">

```bash
jq '[.results[] | select(.goEvidence == "IDA" or .goEvidence == "IPI" or .goEvidence == "EXP"
                       or .goEvidence == "IMP" or .goEvidence == "IGI" or .goEvidence == "IEP")] | length' gr_go.json
jq '[.results[] | select(.goEvidence == "IEA")] | length' gr_go.json
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
87
34
```

</div>

‏۸۷ از ۱۴۷ = **۵۹٪** آزمایشی؛ IEA ‏۳۴ = **۲۳٪**؛ بقیه (۲۶، یعنی ۱۸٪) استنباطی یا گفته‌ی کارشناس (TAS ‏۱۶، IBA ‏۶، ISA ‏۲، ISS ‏۱، IC ‏۱). ‏GR از پرپژوهش‌ترین پروتئین‌های انسان است. برای پروتئین یک باکتری کم‌شناخته، این نسبت وارونه است: بیشتر IEA.

---

## پاسخ ۳: فرزندان و یک شناسه‌ی گم‌شده

<div dir="ltr">

```bash
curl -sS -H "$H" "$Q/ontology/go/terms/GO:0003707/children" | jq -r '.results[0].children[] | "\(.id)\t\(.relation)"'
curl -sS -H "$H" "$Q/ontology/go/terms/GO:0004882/complete" | jq -r '.results[0] | "\(.id)\t\(.name)\tobsolete=\(.isObsolete)"'
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
GO:0030284	is_a
GO:0004883	is_a
GO:0004879	nuclear receptor activity	obsolete=false
```

</div>

(الف) **دو** فرزند: `GO:0030284` (nuclear estrogen receptor activity، نام از درس، بخش ۳.۳ نیامده؛ با `ontology/go/terms/GO:0030284` بسنجید) و `GO:0004883` (nuclear glucocorticoid receptor activity). گیرنده‌های آندروژن، پروژسترون و مینرالوکورتیکوئید اصطلاح ویژه‌ی خود را در این‌جا ندارند.

(ب) پرسش `GO:0004882`، پاسخی با شناسه‌ی **`GO:0004879`** (nuclear receptor activity) برمی‌گرداند. یعنی «androgen receptor activity» در اصطلاح کلی‌تر **ادغام** شده و شناسه‌ی قدیمی تنها یک نام دیگر (secondary ID) برای آن است. پیامد: جدول‌های قدیمی GO (برای نمونه از یک مقاله‌ی ۲۰۱۵) شناسه‌هایی دارند که امروز به اصطلاح دیگری می‌رسند یا منسوخ‌اند. پیش از تحلیل، شناسه‌ها را با نسخه‌ی کنونی GO به‌روز کنید و نسخه‌ی GO را گزارش کنید.

---

## پاسخ ۴: ‏gyrA و acrB در KEGG

<div dir="ltr">

```bash
for b in b2231 b0462; do curl -sS "$K/link/ko/eco:$b"; curl -sS "$K/link/pathway/eco:$b"; sleep 0.5; done
curl -sS "$K/list/pathway/eco" | grep -E 'eco01501|eco01503'
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
eco:b2231	ko:K02469

eco:b0462	ko:K18138
eco:b0462	path:eco01501
eco:b0462	path:eco01503
eco01501	beta-Lactam resistance - Escherichia coli K-12 MG1655
eco01503	Cationic antimicrobial peptide (CAMP) resistance - Escherichia coli K-12 MG1655
```

</div>

(الف) ‏gyrA: ‏**K02469** و **هیچ مسیری** (سطر تهی پاسخ `link/pathway` است). ‏acrB: ‏**K18138**، در «beta-Lactam resistance» و «CAMP resistance».

(ب) ‏KEGG «مسیر مقاومت» را برای **سازوکارهای** مقاومت می‌کشد: پمپ‌های بیرون‌ریز (AcrAB-TolC) دارو را بیرون می‌ریزند و پس در نقشه هستند. مقاومت به کینولون‌ها با **جهش در هدف** (gyrA S83L، 08/01) است و ژن gyrA خودش کار عادی‌اش (DNA gyrase، از KO و BRITE) را دارد، نه نقش مقاومت. مسیرهای KEGG پیرامون **کارکرد** ساخته شده‌اند؛ جهش‌های مقاومت را از پایگاه‌های ویژه (AMRFinderPlus، CARD؛ بخش ۰۸) بگیرید.

---

## پاسخ ۵: غنی‌سازی بی NR3C1

<div dir="ltr">

```bash
grep -v NR3C1 dex8_symbols.txt > dex7.txt
curl -sS -X POST -H "Content-Type: text/plain" --data-binary @dex7.txt \
  "$A/identifiers/projection?pageSize=6&page=1&sortBy=ENTITIES_PVALUE&order=ASC&resource=TOTAL" > ora7.json
jq -r '"found pathways: \(.pathwaysFound)"' ora7.json
jq -r '.pathways[] | [.stId, .name[0:55], "\(.entities.found)/\(.entities.total)", (.entities.pValue | tostring), (.entities.fdr | tostring)] | @tsv' ora7.json
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
found pathways: 38
R-HSA-9909396	Circadian clock	5/148	2.7650927214573073E-8	0.0000010507352341537768
R-HSA-9931510	Phosphorylated BMAL1:CLOCK (ARNTL:CLOCK) activates expr	3/32	0.0000012449747679443846	0.000023654520590943307
R-HSA-9931521	The CRY:PER:kinase complex represses transactivation by	2/21	0.00009113261981064102	0.0010935914377276923
R-HSA-9022699	MECP2 regulates neuronal receptors and channels	2/32	0.0002107518681094822	0.0018967668129853399
R-HSA-1368108	BMAL1:CLOCK,NPAS2 activates circadian expression	2/41	0.00034482289472281824	0.0024137602630597277
R-HSA-8986944	Transcriptional Regulation by MECP2	2/100	0.002007096489841431	0.012042578939048587
```

</div>

(الف) ‏۳۸ مسیر (به جای ۵۷). ‏«Nuclear Receptor transcription» و سه مسیر کلی «رونویسی» **ناپدید** شدند؛ **Circadian clock** در صدر است.

(ب) ‏p-value ‏Circadian clock از 1.1×10⁻⁶ به **2.8×10⁻⁸** رسید، در حالی که شمار یافته‌ها (۵ از ۱۴۸) **عوض نشد**. آزمون ابرهندسی (بخش ۱۴) می‌پرسد «اگر به اندازه‌ی ورودی شما موجودیت تصادفی برمی‌داشتیم، چقدر احتمال داشت ۵ تا در این مسیر بیفتند؟». با برداشتن NR3C1 و ایزوفرم‌هایش، **ورودی کوچک‌تر** شد؛ ۵ یافته از ورودی کوچک‌تر شگفت‌انگیزتر است، پس p کوچک‌تر. یعنی p-value هر مسیر به **همه**‌ی فهرست بستگی دارد، نه تنها به ژن‌های آن مسیر.

---

## پاسخ ۶: مسیر داروی آسم

<div dir="ltr">

```bash
awk -F'\t' '$1 == "WP2880" || $1 == "WP5503" {n = split($3, a, ","); print $1 "\t" $2 "\t" n}' wp_hs.tsv
awk -F'\t' '$1 == "WP5503" {print $3}' wp_hs.tsv | tr ',' '\n' | grep -xFf <(tail -n +2 dex8_ids.tsv | cut -f2)
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
WP2880	Glucocorticoid receptor pathway	70
WP5503	Albuterol and budesonide therapy for asthma	26
2908
```

</div>

(الف) ‏WP2880 ‏**۷۰** ژن و WP5503 ‏**۲۶** ژن. در WP5503 از هشت ژن ما تنها **NR3C1** (2908) هست.

(ب) برای «پاسخ به دگزامتازون»، **WP2880** بهتر است: بزرگ‌تر و ویژه‌ی GR، و دست‌کم TSC22D3 (GILZ) را دارد (درس). ‏WP5503 بیشتر **داروشناسی** را می‌کشد: گیرنده‌ها و پیام‌رسانی دو دارو (گیرنده‌ی بتا-۲ آدرنرژیک برای آلبوترول و GR برای بودزونید)، نه ژن‌هایی که پس از دارو روشن می‌شوند. کمبود هر دو: FKBP5، PER1، DUSP1، KLF15 و ZBTB16، هدف‌های شناخته‌شده‌ی GR در داده‌ی ما، در WP2880 نیستند. هیچ مسیر دستی‌ای همه‌ی هدف‌های رونویسی را ندارد؛ برای آن، مجموعه‌ژن‌های **آزمایشی** (C2 در MSigDB، یا داده‌ی خودتان) بهترند.

---

## پاسخ ۷ (فکری): ‏FKBP5 و آندروژن

(الف) در جدول Hallmark درس تنها **یک** ژن از هشت (FKBP5) در ANDROGEN_RESPONSE است. یک ژن از ۱۰۱ ژن مجموعه هیچ «غنی‌سازی»ای نیست؛ یک آزمون ابرهندسی با ۱ هم‌پوشانی نزدیک به هیچ معنایی ندارد. ‏FKBP5 در دو مجموعه‌ی استروژن هم هست.

(ب) ‏FKBP5 هدف **همه**‌ی گیرنده‌های استروئیدی است. GR، گیرنده‌ی آندروژن (AR) و گیرنده‌ی پروژسترون به عنصرهای پاسخ بسیار همانندی در DNA می‌چسبند و FKBP5 عنصرهای پاسخ گیرنده‌های استروئیدی در اینترون‌هایش دارد؛ پس هر کدام از این هورمون‌ها آن را روشن می‌کند. FKBP5 خود هم‌یار Hsp90 در چرخه‌ی همین گیرنده‌هاست (Reactome، درس) و چرخه‌ی **بازخورد منفی** می‌سازد. پس بودنش در مجموعه‌ی آندروژن یعنی «پاسخ به استروئیدها»، نه «فعال شدن مسیر آندروژن».

(ج) آزمون بهتر: (۱) غنی‌سازی روی **همه**‌ی ژن‌های تغییرکرده‌ی آزمایش (نه هشت ژن برگزیده)، با پس‌زمینه‌ی درست، یا GSEA روی کل فهرست مرتب‌شده (بخش ۱۴)؛ (۲) سنجیدن ژن‌های **ویژه‌ی** AR (که با GR مشترک نیستند) در داده؛ (۳) آزمایش: آیا داروی بازدارنده‌ی AR پاسخ دگزامتازون را کم می‌کند؟

</div>
