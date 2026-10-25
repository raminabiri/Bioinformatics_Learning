<div dir="rtl">

# پاسخ تشریحی: مولکول‌های کوچک

همه‌ی خروجی‌ها واقعی‌اند (PubChem و ChEMBL در 2026-10-24؛ RDKit 2026.03.1).

---

## پاسخ ۱: داروهای دیگر سل

<div dir="ltr">

```bash
cp rif.csv tb.csv
for n in isoniazid pyrazinamide ethambutol; do
  curl -s "$PUG/$n/property/SMILES,MolecularFormula/CSV" | tail -n +2 | sed "s/^/\"$n\",/" >> tb.csv
  sleep 0.3
done
python3 $P/02_Small_Molecules/scripts/mol_props.py tb.csv rifampicin | tail -3 | column -t -s$'\t'
```

</div>

**خروجی واقعی** (ستون‌ها: نام، MW، cLogP، HBD، HBA، RotB، TPSA، تخلف، Tanimoto):

<div dir="ltr">

```
isoniazid     137.1  -0.31  2  3  1  68.0  0  0.05
pyrazinamide  123.1  -0.42  1  3  1  68.9  0  0.05
ethambutol    204.3  -0.29  4  4  9  64.5  0  0.03
```

</div>

- (ب) هر سه کوچک (۱۲۳ تا ۲۰۴ دالتون)، **بی تخلف**، و بی شباهت به ریفامپیسین (۰٫۰۳ تا ۰٫۰۵). چهار داروی اصلی سل (ریفامپیسین، ایزونیازید، پیرازینامید، اتامبوتول) از نظر شیمیایی هیچ پیوندی با هم ندارند و هدف‌های جدا دارند؛ همین ترکیب آن‌ها را در درمان کارا می‌کند.
- (ج) ‏**اتامبوتول** با ۹ پیوند چرخان (با آنکه کوچک است، زنجیره‌ای خطی است). برای داکینگ: هر پیوند چرخان یک بُعد تازه به جست‌وجو می‌افزاید؛ مولکول خطی انعطاف‌پذیر سخت‌تر از مولکول حلقوی سفت داک می‌شود.

---

## پاسخ ۲: مرجع دیگر

<div dir="ltr">

```bash
python3 $P/02_Small_Molecules/scripts/mol_props.py rif.csv rifabutin | cut -f1,9 | column -t -s$'\t'
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
name           Tanimoto_to_rifabutin
rifampicin     0.66
rifabutin      1.00
rifapentine    0.63
rifaximin      0.65
rifamycin SV   0.65
ciprofloxacin  0.08
trimethoprim   0.07
ampicillin     0.11
```

</div>

- (الف) جدول بالا.
- (ب) **بله، ۰٫۶۶**، همان عدد درس. ‏Tanimoto **متقارن** است: (مشترک) ÷ (اجتماع) برای A و B همان است که برای B و A.
- (ج) ‏**ریفامپیسین** (۰٫۶۶). ریفاکسیمین و ریفامایسین SV با ۰٫۶۵ پشت سر آن‌اند؛ تفاوت‌ها کوچک‌اند و نباید زیاد از آن‌ها نتیجه گرفت.

---

## پاسخ ۳: خواندن یک SMILES

<div dir="ltr">

```bash
python3 -c "
from rdkit import Chem
from rdkit.Chem import Descriptors
m = Chem.MolFromSmiles('CC(=O)Oc1ccccc1C(=O)O')
print(m.GetNumAtoms(), round(Descriptors.MolWt(m), 2), Chem.rdMolDescriptors.CalcMolFormula(m))"
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
13 180.16 C9H8O4
```

</div>

- (الف) شمارش دستی: `C`، `C`، `O`، `O`، `c`×۶، `C`، `O`، `O` = ‏۹ کربن + ۴ اکسیژن = **۱۳** اتم سنگین.
- (ب) RDKit: ‏۱۳ اتم (بی هیدروژن؛ هیدروژن‌ها در SMILES ضمنی‌اند)، وزن ۱۸۰٫۱۶، فرمول C₉H₈O₄. همخوان.

---

## پاسخ ۴: فضاآرایی ریفامپیسین

<div dir="ltr">

```bash
python3 -c "
import csv
from rdkit import Chem
r = [x for x in csv.DictReader(open('rif.csv')) if x['name'] == 'rifampicin'][0]
m = Chem.MolFromSmiles(r['SMILES'])
cc = Chem.FindMolChiralCenters(m, includeUnassigned=True, useLegacyImplementation=False)
print(len(cc), cc)
flat = Chem.MolToSmiles(m, isomericSmiles=False)
print(len(r['SMILES']), len(flat))"
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
9 [(1, 'S'), (22, 'S'), (27, 'S'), (28, 'R'), (29, 'S'), (30, 'R'), (31, 'R'), (32, 'R'), (33, 'S')]
164 110
```

</div>

- (الف) **۹ مرکز کایرال** (هر کدام با شماره‌ی اتم و برچسب R یا S).
- (ب) ‏۱۶۴ ← ۱۱۰ نویسه. همه‌ی `@` (پیکربندی ۹ مرکز کایرال) و `/` و `\` (هندسه‌ی پیوندهای دوگانه‌ی حلقه‌ی بزرگ و پیوند `C=N` دنباله) از دست رفت. SMILES بی فضاآرایی در واقع ۲⁹ = ‏۵۱۲ ایزومر فضایی (و بیشتر، با پیوندهای دوگانه) را با هم نشان می‌دهد؛ تنها یکی از آن‌ها ریفامپیسین است.

---

## پاسخ ۵: سازوکار سیپروفلوکساسین در ChEMBL

<div dir="ltr">

```bash
curl -s "https://www.ebi.ac.uk/chembl/api/data/molecule.json?pref_name__iexact=ciprofloxacin" | python3 -c "
import sys, json
m = json.load(sys.stdin)['molecules'][0]
print(m['molecule_chembl_id'], m['first_approval'], m['atc_classifications'])"
curl -s "https://www.ebi.ac.uk/chembl/api/data/mechanism.json?molecule_chembl_id=CHEMBL8" | python3 -c "
import sys, json
for x in json.load(sys.stdin)['mechanisms']:
    print(x['mechanism_of_action'], x['target_chembl_id'], x['action_type'])"
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
CHEMBL8 1987 ['J01MA02', 'S03AA07', 'S01AE03', 'S02AA15']
Bacterial DNA gyrase inhibitor CHEMBL2311224 INHIBITOR
Topoisomerase IV inhibitor CHEMBL2363076 INHIBITOR
```

</div>

- (الف) ‏**CHEMBL8**، نخستین تأیید **۱۹۸۷**، چهار کد ATC (J01 خوراکی/تزریقی، و S01، S02، S03 قطره‌های چشمی و گوشی).
- (ب) **DNA ژیراز** (زیرواحد A آن را ژن **gyrA** می‌سازد) و **توپوایزومراز IV** (زیرواحد A آن را ژن **parC** می‌سازد). این همان دو ژنی است که جهش‌هایشان (`gyrA_S83L` در isoA و `parC_S80I` در isoB) را در ماژول 08/01 پیدا کردید. ‏ChEMBL هدف دارو را می‌گوید؛ AMRFinderPlus جهش در همان هدف را.

---

## پاسخ ۶: ساختارهای سه‌بعدی

<div dir="ltr">

```bash
python3 -c "
from rdkit import Chem
for m in Chem.SDMolSupplier('rif3d.sdf', removeHs=False):
    print(m.GetProp('_Name'), m.GetNumAtoms(), m.GetNumHeavyAtoms())"
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
rifampicin 117 59
rifabutin 123 61
rifapentine 127 63
rifaximin 108 57
rifamycin SV 97 50
ciprofloxacin 42 24
trimethoprim 39 21
ampicillin 43 24
```

</div>

- (الف) جدول بالا (هشت مولکول؛ ‏`removeHs=False` هیدروژن‌ها را نگه می‌دارد).
- (ب) ریفامپیسین **۵۹** اتم سنگین دارد، همان ۵۹ اتم RFP در بلور 5UAC. ‏۱۱۷ − ۵۹ = ۵۸ هیدروژن، همان H₅₈ فرمول؛ هیدروژن‌هایی که بلورنگاری نمی‌بیند و پیش از داکینگ باید افزوده شوند (ماژول ۰۳).

---

## پاسخ ۷: فکری — فیلتر کتابخانه

- (الف) **ریفامپیسین** (۳ تخلف)، و همه‌ی ریفامایسین‌ها؛ یعنی همان داروهایی که RNAP را در همین جایگاه مهار می‌کنند.
- (ب) **موافق:** برای یافتن داروی **خوراکی** سنتزی، فیلتر کتابخانه را کوچک و ارزان می‌کند و ترکیب‌هایی را که احتمال جذب کمی دارند پیش از داکینگ کنار می‌گذارد. **مخالف:** جایگاه ریفامپیسین بزرگ است و مهارکننده‌های شناخته‌شده‌اش همه فراورده‌های طبیعی بزرگ‌اند؛ فیلتر سخت شاید درست همان ترکیب‌هایی را حذف کند که اندازه‌شان برای این جایگاه مناسب است. یک راه میانه: فیلتر نرم‌تر (برای نمونه بیش از یک تخلف مجاز) یا جدا کردن فراورده‌های طبیعی.

</div>
