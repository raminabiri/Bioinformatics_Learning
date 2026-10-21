# PROGRESS — Bioinformatics course (Persian, for biologists new to bioinformatics)

## 1. Current goal
Rewrite the course part by part in the new step-by-step format (STYLE_GUIDE.md; memory: deep-explanation-style): dissect every command, real outputs only, strict prerequisites (nothing used before taught), exercises with a hint under each title + detailed solutions, refs (docs + Coursera + edX + YouTube), RTL. User says "ادامه" to continue. Commit+push every 3 modules.
**Now:** part 05 done & pushed (2026-10-21). Next: part 06/01 Read QC rewrite.

## 2. Done so far
- ✅ 00 Orientation, 01 Linux (10 modules), 02 BioLinux (5), 03 Python (6) — new format, pushed (b5afb1b and earlier).
- ✅ **04_R_Packages** (2026-10-20, pushed 87c221b). User decision: R language + statistics = SEPARATE course; no R/RStudio install lessons. Modules: 01_Install_Packages · 02_Run_Rscript · 03_Bioc_Examples (DESeq2 on simulated E. coli counts, seed 42, TP 88/FP 5/FN 12; vegan; ggtree woodmouse) · 04_R_in_Pipelines (run_all.sh, set -e, logs).
- ✅ **05_Reproducible_Work** (2026-10-21, pushed): 01_Git_Basics · 02_Git_Branches_GitHub (local bare repo as fake GitHub) · 03_Snakemake_First (count reads per accession = ground_truth.tsv) · 04_Snakemake_Pipeline (config.yaml, params/log, Python+R scripts, merge, check_truth; 7 exercises all run for real in scratchpad `p4/` and `doctor/`).
  - Real Snakemake 9 behavior found: inputs < 1 MB are checksummed (`--max-checksum-file-size`, default 1MB), so `touch names.tsv` triggers nothing; FASTQ (~3 MB) still follows mtime. Lesson 04 table + exercise 1 explain it.
  - `diversity.R` (part 04) silently treats any level ≠ genus as organism; exercise 04/4 teaches a `sys.exit` config check in the Snakefile instead of changing the part-04 script.
- Old part-05 content (Snakemake QC workflow with fastp/FastQC/bowtie2, old Git lesson) backed up in scratchpad `old_part05/` and in git history; reuse QC workflow when rewriting 06/01.

## 3. Files changed
- Part 05 committed with composition.R 4th arg, 04/02 lesson+solutions, envs/workflow.yml, READMEs. Untracked user files left alone: `Bioinformatics_Course_ColorCoded.xlsx`, `advanced.odt`.

## 4. Key decisions and rejected approaches
- Part 05 Snakemake uses ONLY taught tools (Bash, seqkit, Python, R scripts of part 04). Rejected old fastp/FastQC/bowtie2 workflow: those tools are taught in part 06 (prereq rule).
- R scripts called via `shell: "Rscript …"`, not `script:` — so part-04 scripts stay usable outside Snakemake.
- `[.]` instead of `\.` in Snakefile regex (Python SyntaxWarning `"\." is an invalid escape sequence`); no `head` after `zcat` in rules (pipefail → exit 141).
- Part 04 env `envs/r_packages.yml` pins >= versions (unpinned solve picked bioconductor-ggtree 1.2.12).
- File naming: README.md unnumbered; 01_lesson, 02_exercises, 03_solutions; scripts/data in `<part>/99_scripts_data/<module>/`.
- Never send user's email to external APIs; heavy jobs/downloads are not run (write + cite docs, label hypothetical).

## 5. Known bugs / caveats (exact messages)
- conda.anaconda.org unreachable from server: `Could not resolve host: conda.anaconda.org`. Env files only dry-run solved with the offline cache.
- `envs/workflow.yml` with strict priority: `package snakemake-minimal-9.25.2-pyhdfd78af_0 is excluded by strict repo priority`; solves with `CONDA_CHANNEL_PRIORITY=flexible` (documented in yml + 05/03 lesson). With python=3.13: `pulp … requires python_abi =3.14` (offline cache).
- `envs/r_packages.yml` offline: `nothing provides r-aplot needed by bioconductor-ggtree-4.0.4` (cache gap; r-aplot exists on conda-forge).
- System R uses bspm/r2u: `install.packages("vegan")` installed r-cran-vegan + r-cran-permute system-wide via apt (2026-10-20).
- Snakemake shell + `zcat … | head` → exit 141 (SIGPIPE under pipefail).
- `_tools/check_links.sh` sometimes `FAIL 000` for YouTube (timeouts); rerun.
- Coursera returns 451 from server; URLs taken from WebSearch index. Full link check deferred to course end (user's VPN).
- In my shell grep=ugrep, awk=gawk, find=bfs: use /usr/bin/grep and /usr/bin/mawk for lesson outputs.

## 6. Next steps (priority order)
1. Part 06/01 Read QC rewrite (reuse old Snakemake QC workflow from git history; old part-05 backup was in a previous session's scratchpad `old_part05/` — may be gone, use `git show 87c221b:05_Reproducible_Work/02_Workflows_Snakemake/...`), then 06/02–06/04.
2. 07/01–07/02 rewrite; 07/03–07/05 write-only (MLST, pan-genome, Snippy).
3. Verify `envs/r_packages.yml` and `envs/workflow.yml` solve online when conda is reachable.
4. At course end: full link check with user's VPN (`_tools/check_links.sh`).
