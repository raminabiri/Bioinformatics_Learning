#!/usr/bin/env bash
# Data for module 12/04 (protein families and domains). Run inside ~/global/m04.
#   query.faa      7 UniProt proteins: six beta-lactamases (Ambler classes A, B, C, D) + glucocorticoid receptor
#   mini_pfam.hmm  7 Pfam profile HMMs from the InterPro API, pressed for hmmscan
#   ecoli.faa      all 4300 proteins of E. coli K-12 MG1655 (RefSeq GCF_000005845.2), for hmmsearch
# Versions used in the lesson (2026-10-27): InterPro 110.0, Pfam 38.2.
set -euo pipefail

# 1. proteins (TEM-1, CTX-M-15, KPC-2 = class A; AmpC = C; OXA-48 = D; NDM-1 = B; GR)
curl -sS "https://rest.uniprot.org/uniprotkb/accessions?accessions=P62593,A0A5R8T042,Q9F663,P00811,Q6XEC0,C7C422,P04150&format=fasta" > query.faa
grep -c '>' query.faa                                   # 7

# 2. Pfam HMMs: Beta-lactamase2, Beta-lactamase, Transpeptidase, Lactamase_B, Hormone_recep, zf-C4, GCR
for p in PF13354 PF00144 PF00905 PF00753 PF00104 PF00105 PF02155; do
  curl -sS "https://www.ebi.ac.uk/interpro/api/entry/pfam/$p?annotation=hmm" | gunzip > $p.hmm
  sleep 1
done
cat PF*.hmm > mini_pfam.hmm
hmmpress -f mini_pfam.hmm                               # needs: conda activate databases

# 3. E. coli K-12 proteome
curl -sS https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/005/845/GCF_000005845.2_ASM584v2/GCF_000005845.2_ASM584v2_protein.faa.gz \
  | gunzip > ecoli.faa
grep -c '>' ecoli.faa                                   # 4300
