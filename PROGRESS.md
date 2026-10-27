# PROGRESS — Bioinformatics course (Persian, for biologists new to bioinformatics)

Short handoff file. The full narrative of every session (decisions, problems, verified numbers) is in **SESSION_LOG.md** (Persian) — keep it updated; the user wants complete reports.

## 1. Current goal
Write course **version 2** (parts 11–22, folders `NN_V2_…`, plan in `V2_ROADMAP.md`) in the STYLE_GUIDE.md format: dissect every command, **real outputs only** (dated), known-answer data, strict prerequisites, ≥5 exercises with a «راهنمایی» hint plus detailed solutions, 📺 video + 📄 reference under every technique, منابع with papers + books + Coursera/edX/YouTube, RTL via `_tools/rtl_wrap.py`, wording via `_tools/persian_words.py`, links via `_tools/check_internal_links.py`. Commit + push every 3 modules (and at the end of a part).

**State (2026-10-27, later):** v1 (parts 00–09) complete. v2 part 11 complete. **v2 part 12 modules 01–03 (Ensembl/BioMart, UCSC, IGV) written, run and pushed.** User said "go to 12" and earlier "write to the end without asking" → continue with 12/04–06. **Restructure question deferred:** user asked whether parts 11/12 should come before Linux/Python; decision: finish all of v2 first, then decide (option on the table: a learning-path table + web-first/code-second modules, not renumbering).

**Standing rules from the user:**
- Run only what needs **< 1 GB RAM**; heavier work is code-only, labelled ✍️ "از مستندات". Do not touch `/data/1/genomepipe` or the `genomepipe_tools` env.
- Plain Persian: avoid عدم، می‌باشد، استفاده، دستورالعمل، اکثر، لذا، توسط، نمودن/گردیدن، مثال، عملی… (STYLE_GUIDE §8).
- **Never** put the NCBI API key (`$NCBI_API_KEY` in ~/.bashrc), the machine email or the server IP in lessons or commits; EDirect stderr prints them → send stderr to a scratch log. Never send the user's email to external services.
- Never commit the untracked user files `Bioinformatics_Course_ColorCoded.xlsx`, `advanced.odt`.
- Commits end with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.

## 2. Done so far
- ✅ **v1 parts 00–06, 08, 09** written and run (09 is introductory by user decision). ✍️ **07** written but nothing run.
- ✅ All v1 lessons have per-technique 📺/📄 boxes and book sections (cc70d8d). Part 10 is now a pointer to v2/separate courses.
- ✅ **v2 scaffold**: parts 11–22, 46 module READMEs (310755b, a1c4f63, 0c75968). Separate-course folders in `/data/Education/new/` (not a git repo).
- ✅ **v2 part 12, modules 01–03** (2026-10-27), env `envs/databases.yml` (ucsc-liftover 502, samtools/bcftools 1.24, hmmer 3.4, igv-reports 1.16.0):
  - 01 Ensembl REST (release 116) + BioMart (jun2026 archive) + `ens_ids.py` (requests, retries): NR3C1 ENST00000394464 = NM_000176.3 (1 ENST ↔ 10 NM; 8 are the same mRNA with different start AUGs); release 114 vs 116 coordinate changes; Ensembl Bacteria rpoB/gyrA.
  - 02 UCSC API (0-based) + hgRenderTracks images + liftOver (F508del 117199645→117559591; 3000 random windows: 315 Deleted all N, 9 Split, 12 to _random; wrong-direction chain gives no error).
  - 03 IGV ✍️ + `samtools tview -d T`, mpileup AD/ADF/ADR (4 true variants vs 1451 single-read errors, 0.198% = wgsim 0.002), MAPQ: 224 reads moved to tufA/rRNA copies; igv-reports HTML.
- ✅ **v2 part 11** (67f2196, 46270b3, 868cdc8), all run on 2026-10-27:
  - 01 Entrez/E-utilities (curl) + EDirect/xtract/Biopython; rpoB Gene 948488, NP_418414.1 (1342 aa).
  - 02 RefSeq prefixes, NR3C1 MANE NM_000176.3→NP_000167.1 (777 aa), 11 GR isoforms, IPG (WP_000263098.1, 402,479 records), CDD, Taxonomy, `datasets`.
  - 03 BioProject PRJEB7774 (312 runs, 595 GB), BioSample, SRA Toolkit on ERR688359 (1,158,189 reads = ENA).
  - 04 GEO GSE52778: series matrix has no expression; NCBI counts; FKBP5/TSC22D3/ZBTB16 up, NR3C1 down; GEO2R ✍️.
  - 05 dbSNP/ClinVar/dbVar/MedGen/GTR on rs113993960 (F508del, VCV000007105, 4 stars); HGVS↔SPDI with the Variation API; 3′ rule.
  - 06 PubMed ATM, MeSH D012293, spelling (83+33→115), citation exporter, PMC full text, PubTator3.
  - 07 BLAST+: S450↔S531 mapping, tblastn, E-value vs dbsize, primers F1406/R1770 (365 bp), six-frame ORFs, CD-Search API; remote BLAST did not answer within 25 min (reported as is).
  - 08 Pathogen Detection FTP (591,810 isolates; blaCTX-M-15 13%), SNP clusters, NCBI Virus/Datasets (CCHFV 5471 records, Iran 177).

## 3. Files changed (part 12 session, 2026-10-27)
- `12_V2_Global_Databases_Browsers/0[1-3]_*/` — README + `01_lesson.md` + `02_exercises.md` + `03_solutions.md`; part README (status), `99_scripts_data/01_Ensembl_BioMart/{scripts/ens_ids.py,data/*.xml}`, `02_UCSC_Genome_Browser/{data/*.bed,images/*.png}`, `03_IGV_Visualization/scripts/rpoB_snapshots.igv.txt`.
- `envs/databases.yml` (new) + `envs/README.md`; `V2_ROADMAP.md`, `README.md`, `SESSION_LOG.md`, `PROGRESS.md`; memory `course-roadmap-2026-10.md` (restructure deferred).
- Scratch: `scratchpad/p12/m01…m03`, helper `p12/ej.sh` (curl + retry until valid JSON).

## 3b. Files changed (part 11 session)
- `11_V2_NCBI_Databases/0[1-8]_*/` — README + `01_lesson*.md` + exercises + solutions (11/01 has `01_lesson_eutils.md`, `02_lesson_edirect.md`, `03_exercises.md`, `04_solutions.md`; the others have `01_lesson.md`, `02_exercises.md`, `03_solutions.md`).
- `11_V2_NCBI_Databases/99_scripts_data/`: `01_Entrez_EDirect/scripts/gene_table.py`, `04_GEO/scripts/geo_counts.py`, `07_BLAST_Suite_Tools/scripts/{map_positions.py,six_frames.py}`, `08_Pathogen_Virus_Resources/scripts/amr_summary.py`.
- `11_V2_NCBI_Databases/README.md` (all ✅), `V2_ROADMAP.md` (status), `README.md` (v2 paragraph + tree), `SESSION_LOG.md`, `PROGRESS.md`; memory `course-roadmap-2026-10.md` + `MEMORY.md`.
- Scratch data (wiped between sessions): `/tmp/claude-1000/…/scratchpad/p11/m01…m08`, helper `r.sh` (EDirect with timeout + retries), `p11/videos_verified.txt`.

## 4. Key decisions and rejected approaches
- Modules 11/02–11/08 use **one lesson file** (not two) to keep parts readable; 11/01 needed two (curl vs EDirect).
- Big NCBI files are **streamed** (`csv` line by line, ~270 MB RAM) instead of pandas (would exceed 1 GB).
- Where a web tool has no API (GEO2R, Primer-BLAST, ORFfinder, Isolates Browser, MicroBIGG-E) the lesson gives ✍️ web steps **and** does the same analysis on the server (BLAST+, Biopython, FTP data). Rejected: describing outputs we did not see.
- Failures and odd behaviour are taught as pitfalls (elink -name ignored, PubTator OR, remote BLAST queue, `xtract -mixed`), not hidden.
- Unverifiable claims were softened or removed (GEO2R design, NBK3841, ClusteredNR default, ST131 inference).
- Shell functions and awk `?:` are not taught in v1 → replaced with `for` loops / explained inline.
- SRA Toolkit run from the conda package cache (`~/miniforge3/pkgs/sra-tools-3.4.1-2_linux_64/bin`) because `genomepipe_tools` is off limits and an offline env build failed.
- Videos verified with `https://noembed.com/embed?url=…` (YouTube itself is blocked from the server).

## 5. Known bugs and caveats (exact messages)
- Part 12 (2026-10-27): Ensembl REST often `HTTP 500`/`503` with an HTML page → `jq: parse error: Invalid numeric literal`, `requests.exceptions.JSONDecodeError`; use retries (`scratchpad/p12/ej.sh`, `ens_ids.py`). BioMart 116 (jun2026.archive) answers GET only (POST → `405 Not Allowed`), was "Service unavailable" ~15 min. `rest.ensemblgenomes.org` unreachable (main REST serves bacteria). Fly-side homology needs `compara=multi` (`Could not find a GenomeDB named 'homo_sapiens'`).
- UCSC `hgTables` via curl → Cloudflare Turnstile page; `hgRenderTracks` ignores `hgt.customText`. Running a downloaded liftOver binary was blocked by the permission classifier → use Bioconda ucsc-liftover.
- igv.org unreachable from server; headless Chrome screenshots of igv-reports stay blank (igv.js never finishes).
- EDirect 24.0 stderr on most calls: `curl: (56) OpenSSL SSL_read: OpenSSL/3.6.4: error:0A000126:SSL routines::unexpected eof while reading, errno 0` (retries succeed; lines contain the API key and email). Some calls hang for hours → always `timeout 60–90` and retry.
- EDirect: `elink -name gene_protein_refseq` ignored in a pipe → use `efilter -query "refseq[filter]"`.
- Raw PubMed XML: `UNEXPECTED MIXED CONTENT <i> IN <Reference>` unless `xtract -mixed`.
- PMC OA service `https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi` → 404; ID converter moved to `https://pmc.ncbi.nlm.nih.gov/tools/idconv/api/v1/articles/`.
- Remote BLAST (RID `E13YYMUD014`) stayed `Status=WAITING` 25+ min; `blastp -remote` timed out (rc=124). NCBI rules: ≤1 request/10 s, poll an RID ≤1/min.
- GEO2R/GEO help pages: reCAPTCHA from the server. Coursera often returns 451.
- Offline conda: `OfflineError: EnforceUnusedAdapter called with url …perl-importer…` (sra-tools); `Could not resolve host: conda.anaconda.org`.
- `pkill -f`/`pgrep -f` whose pattern matches the calling shell kills it (exit 144) → `ps aux | grep '[x]yz'`.
- Monitor tasks expire after 5 min and stop any loop inside them → long polls go in `run_in_background` Bash.
- Pathogen Detection TSV: `scientific_name` is the strain name (use `species_taxid`); dates contain `missing`, `NULL`, `1900-01-01`.
- v1 caveats (still open): AMRFinderPlus DB lacks nucleotide BLAST index (`The BLAST database for AMR_DNA-Escherichia.fa was not found.`); AlphaFold DB 403 from server; VFDB/ZINC time out; `envs/workflow.yml` needs `CONDA_CHANNEL_PRIORITY=flexible`; `grep` here is ugrep (use `/usr/bin/grep` for exact outputs).

## 6. Next steps (priority order, one session each)
1. **v2 part 12, modules 04–06** (InterPro/HMMER on P04150 & beta-lactamases, GO/KEGG/Reactome — all APIs answered on 2026-10-27; GTEx (gencodeId ENSG00000113580.14)/HPA/GDC release 46/cBioPortal APIs answered); commit+push at end of part 12.
3. Optional: if remote BLAST answers on a later day, add the real Swiss-Prot hits to 11/07 §10 (keep the queue story).
4. v2 part 13 (RNA-seq; DESeq2 on GSE52778 counts from 11/04 — `deg_r` env has GEOquery 2.80.0, DESeq2 **not** installed).
5. Real runs of v1 part 07 (needs genomepipe coordination and user approval).
6. Plan the separate courses with the user (folders in `/data/Education/new/`).
7. Course-end checks with the user's VPN: `_tools/check_links.sh`, every YouTube URL, book chapter numbers.
