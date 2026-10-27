# PROGRESS — Bioinformatics course (Persian, for biologists new to bioinformatics)

Short handoff file. The full narrative of every session (decisions, problems, verified numbers) is in **SESSION_LOG.md** — keep it updated, the user asked for complete reports.

## 1. Current goal
Rewrite the course part by part in the step-by-step format of STYLE_GUIDE.md: dissect every command, real outputs only, strict prerequisites (nothing used before it is taught), ≥5 exercises with a hint under each title plus detailed solutions, references under every technique, RTL via `_tools/rtl_wrap.py`. The user says "ادامه" to continue; commit and push every 3 modules.

**Now (2026-10-27):** writing **version 2** in order (user: "continue writing with the same rules"). User (2026-10-27): **write all of part 11 without asking, then commit and push.** Done: 11/01 Entrez_EDirect, 11/02 Gene/RefSeq/Protein/Taxonomy, 11/03 BioProject/BioSample/SRA (committed+pushed together). Next: 11/04 GEO → 11/08, commit after 11/06 and at the end.

**Earlier (2026-10-26):** every lesson in 00–09 now has per-technique 📺/📄 boxes and a book section in منابع (112 boxes added to 00–07). Parts 00–09 are **complete** (every module has lesson, exercises and solutions) and pushed. Part 10 is deliberately not written (user: "do not go into advanced topics"; it becomes course v2).

**Standing rules from the user:**
- Run only what needs **< 1 GB RAM**; everything heavier is code-only, labelled ✍️ "از مستندات". (2026-10-25: anything under 1 GB may run freely while genomepipe is busy; the 1.3 GB Vina runs wait for a free window and were approved once at ~3 min each on 2 cores.)
- Glossary: STYLE_GUIDE §8. "ضراوت" → **"بیماری‌زایی"** (replaced course-wide).
- Glossary extended 2026-10-26: عدم، می‌باشد، اکثر، لذا، توسط، نمودن/گردیدن (formal/Arabic words the user dislikes). `persian_words.py` flags them; course is clean.
- Under **every technique**: a 📺 video URL and a 📄 reference; at the end of each lesson a منابع list with papers, **books**, and Coursera + edX + YouTube.
- Do not touch `/data/1/genomepipe` or `genomepipe_tools`.

## 2. Done so far
- ✅ **00** Orientation, **01** Linux (10 modules), **02** BioLinux (5), **03** Python (6) — pushed (b5afb1b and earlier).
- ✅ **04_R_Packages** (87c221b). User decision: R language + statistics are a SEPARATE course; no R/RStudio install lessons.
- ✅ **05_Reproducible_Work**: Git basics, branches via a local bare repo, first Snakemake workflow, full pipeline with config/params/logs and a ground-truth check.
- ✅ **06_Metagenomics**: rewritten without new runs; all outputs reused from the 2026-10-12..15 runs and verified by reading those files.
- ✍️ **07_Bacterial_Genomics**: all 5 modules written, **nothing run** (user asked for no code at the time). Sample outputs come from official docs; exercise tables labelled فرضی. ST10 and ST131 profiles verified via the PubMLST REST API.
- ✅ **08_AMR_Virulence_Phylogeny** (eade55f, 1f8094a). Data = known-answer simulations on the part-01 K-12 genome plus real public sequences.
  - 01 AMR: AMRFinderPlus 4.2.7 / DB 2026-08-07.1 recovered exactly the 5 planted features (`tet(A)` as PARTIALX 50.38%); ~80 s, 183 MB. RGI and ABRicate are doc-only.
  - 02 virulence: stxtyper read the planted operon as `STX2A COMPLETE`; VFDB setA via makeblastdb/blastn shows K-12 itself carries 65 VF genes (the teaching point); heatmap with ggplot2.
  - 03 mobile elements: real plasmid pEK499 (EU935739.1) → 12 core AMR genes, replicons IncFIA + IncFII, `catB3` truncated by IS26, class 1 integron; `find_crispr.py` finds the K-12 I-E array (12 spacers) next to the cas operon.
  - 04 phylogeny: MAFFT + NJ/bootstrap on 15 real beta-lactamase genes (5 CTX-M groups at 100%); simulated 20-isolate outbreak with a known true tree → transmission H1→H2 recovered, Robinson-Foulds 4 only from polytomies. IQ-TREE and Gubbins are doc-only.
- ✅ **09_Structural_Bioinformatics** (1b148be) — **introductory level by user decision**. Restructured 5 modules → 4 (dropped `05_Visualization`, folded PyMOL into module 01). Shared data: RNA polymerase + rifampicin (5UAC wild type, 5UAL S531L, 5UAH D516V; Molodtsov 2017), AlphaFold `AF-P0A8V2-F1`, and 1L2Y for MD.
  - 01: gemmi + PyMOL; the 14 pocket residues include D516/H526/S531, which ties the structure back to module 08/01. AlphaFold model vs experiment: mean pLDDT 90.1, CA RMSD 1.39 Å.
  - 02: PubChem + ChEMBL + RDKit; every rifamycin breaks 2–4 Lipinski rules yet several are oral drugs. RDKit numbers match ChEMBL exactly.
  - 03: full Vina pipeline. Wild-type redocking passes (1.55 Å), S531L fails (8.42 Å, correct pose rank 5). With `--exhaustiveness 32` the wild type finds a 1.00 Å pose but ranks it second → **the limit is scoring, not search** (lesson §7.1). Solutions written 2026-10-26 from 7 real runs (approved by the user): seeds agree (first poses within 0.13 Å); shifted box gives −5.93 / 29.4 Å with no warning; 16 Å box still works; docking from the RDKit conformer fails (8.36 Å, best rank 3 at 2.78 Å) because the macrocycle shape is fixed and differs 2.35 Å from the crystal; rifabutin −7.61 is not comparable.
  - 04: OpenMM + mdtraj on Trp-cage. Key finding: the same seed run twice gives different results (RMSD 2.12 vs 2.30) — MD on CPU is not bit-wise reproducible, unlike Vina. Only patterns across replicas are reportable (TRP6 always least mobile, 0.49–0.61 Å). A 200 ps run raises ASN1 RMSF from 1.99 to 3.11 Å, i.e. RMSF is not converged.

## 3. Files changed
- Recent commits: **eade55f** (part 08 + glossary change + `envs/amr.yml`, `envs/phylo.yml`), **1f8094a** (PROGRESS next steps), **1b148be** (part 09: restructure, 4 modules, `envs/structural.yml`, `SESSION_LOG.md`, README updates).
- Layout: `README.md` unnumbered; lessons `01_lesson*.md`, then exercises, then solutions; scripts and small data in `<part>/99_scripts_data/<module>/scripts|data`; figures in `<module>/images/`.
- Untracked user files left alone on purpose: `Bioinformatics_Course_ColorCoded.xlsx`, `advanced.odt`.
- Working data lives in the session scratchpad (`p08/{amr,phylo}`, `p09/{dock,md}`) and **is wiped between sessions**; rebuild it by rerunning the scripts in `99_scripts_data` (verified to reproduce the same numbers).

## 4. Key decisions and rejected approaches
- **Version 2 (2026-10-26):** user wants omics (GEO, STRING, Enrichr, NetworkAnalyst, GeneMANIA, Cytoscape, DGIdb, miRNA DBs, single-cell) and most NCBI databases in v2, folders 11+ named `NN_V2_…`. Human dataset GSE52778 (airway) becomes a second thread because these tools are human-centric and bacteria have no miRNA; STRING bridges to *E. coli*.
- Part 09 stays **introductory**; a professional structural-bioinformatics course and an NGS/third-generation course are planned separately, with an expert reviewer the user will introduce. Part 10 is deferred to course version 2. Reason: the user wants depth in dedicated courses rather than a shallow pass here.
- Every part uses **known-answer data** (simulated genomes, a crystal pose for redocking, a simulated outbreak with its true tree) so the learner can check the tool instead of trusting it. Rejected: using real unlabelled datasets, which hide tool error.
- Tools that are heavy or not installed are written from **official documentation only** and labelled ✍️, with predictions marked as predictions. Rejected: inventing plausible outputs.
- Part 05 Snakemake uses only tools already taught (Bash, seqkit, Python, part-04 R scripts). Rejected the old fastp/FastQC/bowtie2 workflow because those tools are taught later, in part 06.
- R scripts are called as `shell: "Rscript …"`, not Snakemake `script:`, so the part-04 scripts stay usable on their own.
- `diff` and `column` are not taught in part 01, so exercises use `sort | uniq -u`; `column -t -s$'\t'` is introduced explicitly in 08/01.
- Never send the user's email to external APIs.

## 5. Known bugs and caveats (exact messages)
- `conda.anaconda.org` unreachable from the server: `Could not resolve host: conda.anaconda.org`. All env files are only dry-run solved against the offline cache.
- `envs/workflow.yml` under strict priority: `package snakemake-minimal-9.25.2-pyhdfd78af_0 is excluded by strict repo priority` → needs `CONDA_CHANNEL_PRIORITY=flexible`. With python=3.13: `pulp … requires python_abi =3.14`.
- `envs/r_packages.yml` offline: `nothing provides r-aplot needed by bioconductor-ggtree-4.0.4` (cache gap only; r-aplot exists on conda-forge).
- AMRFinderPlus DB on this server lacks the nucleotide BLAST index: `The BLAST database for AMR_DNA-Escherichia.fa was not found.` Worked around in a scratchpad **copy** (`makeblastdb` on `AMR_DNA-*.fa`, run with `-d`); the miniforge install is untouched.
- AlphaFold DB and its Google Cloud mirror return **403** from this server (`We're sorry, but this service is not available in your location`). The model was taken from `models.rcsb.org` as BinaryCIF; gemmi cannot read BinaryCIF (`Unknown format`) and PyMOL needs msgpack-c, so a small decoder was used in the scratchpad. Resulting mean pLDDT 90.05 matches RCSB's own value.
- VFDB (`mgc.ac.cn`) and ZINC time out from the server; VFDB and PlasmidFinder data files were taken from the ABRicate GitHub repo (data only). Running ABRicate from a clone was denied by the sandbox classifier ("Code from External"), so ABRicate and RGI stay doc-only.
- YouTube is unreachable from the server (`curl` returns 000); all video URLs come from WebSearch and still need checking. Coursera returns 451.
- `obrms` returns `RMSD := inf` when atom order differs → use `rmsd_pdbqt.py` (same order) or `rmsd_graph.py` (graph matching).
- `gemmi.Structure.get_info` does not exist in 0.7 → use `st.info[...]`. In OpenMM scripts, `from openmm.unit import *` shadows Python's `sum`.
- `ape::root()` moves bootstrap labels unless `edgelabel = TRUE`, and labels the new root "Root"; NJ can return negative branch lengths (CTX-M-3: −0.00033), explained in 08/04.
- In PDB format a four-digit residue number touches the chain name (`A1342`), so whitespace-based `awk` reads the wrong column — use fixed columns (this became exercise 09/01-5).
- Snakemake `shell:` with `zcat … | head` exits 141 (SIGPIPE under pipefail).
- In this shell `grep` is ugrep, `awk` is gawk, `find` is bfs — use `/usr/bin/grep` and `/usr/bin/mawk` when capturing lesson outputs.

- EDirect 24.0 on this server prints `curl: (56) OpenSSL SSL_read: OpenSSL/3.6.4: error:0A000126:SSL routines::unexpected eof while reading, errno 0` on stderr for most requests, then retries and succeeds. Its error lines include the **NCBI API key and the machine email** → always `2>> err.log` (scratch), never paste stderr into lessons.
- 2026-10-27: one `esearch` hung for >2 h (NCBI side); wrap every EDirect call in `timeout 90`.
- EDirect 24.0: `elink -name gene_protein_refseq` is **ignored** when elink reads from a pipe (13 = 13 links for rpoB, 87 for five genes) → use `elink -target protein | efilter -query "refseq[filter]"`. Raw `elink.fcgi&linkname=` works. (Taught as a pitfall in 11/01.)
- SRA Toolkit: no env had it except `genomepipe_tools` (off limits). `conda create --offline sra-tools=3.4.1` fails (perl deps missing from cache: `OfflineError: EnforceUnusedAdapter called with url …perl-importer…`). Lesson 11/03 ran the binaries straight from the package cache: `PATH=~/miniforge3/pkgs/sra-tools-3.4.1-2_linux_64/bin:$PATH` (prefetch, vdb-validate, fasterq-dump, fastq-dump all work).
- `pgrep -f`/`pkill -f` with a pattern that also appears in the calling command line kills the calling shell (exit 144). Use `ps aux | grep '[x]yz'`.
- EDirect pipelines that fetch all links of a human gene (`elink -target nuccore | efetch`) exceed the timeout (hundreds of records): count first, use `linkname` via curl. Helper with retries: scratchpad `r.sh`.
- Rate-limit JSON error contains the server's public IP in `"api-key"` → redact in lessons.

## 6. Next steps (priority order, one session each)
1. **Version 2: writing part 11 in order without asking.** 11/01–11/03 done and pushed 2026-10-27. Next 11/04–11/08. Then the rest of part 11. Scaffold notes: Parts 11–22 (`NN_V2_…`, 46 module READMEs) and `V2_ROADMAP.md`. User removed single-cell, human variant and long-read parts (→ separate NGS course; clinical interpretation → separate medical-genomics course). Part 10's modules 01/05/06 live in parts 20–22; `10_Advanced/README.md` is now a pointer.
2. Real runs of part 07 (nothing run in v1) — needs coordination with genomepipe and user approval.
3. Optionally upgrade 08/04 lesson 2 to real IQ-TREE runs (IQ-TREE 3 is installed but not in PATH).
4. Plan the separate courses with the user (names in `V2_ROADMAP.md`); structural and NGS first, with the expert reviewer.
5. Verify the env files online (`r_packages`, `workflow`, `metagenomics`, `bacterial_genomics`, `amr`, `phylo`, `structural`) once conda is reachable. Note: there is no `structural` env on this server; the tools are in the miniforge base env.
6. At course end: full link check with the user's VPN (`_tools/check_links.sh`), every YouTube URL, and the book chapter numbers added 2026-10-26.
