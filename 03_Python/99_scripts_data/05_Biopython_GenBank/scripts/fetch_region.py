# fetch_region.py: download one region of a GenBank record from NCBI with Bio.Entrez
# Usage: python3 fetch_region.py NC_000913.3 4175000 4190000 rpo_region.gb
import sys
from Bio import Entrez

Entrez.email = "your.name@example.org"     # NCBI asks for a contact email: put YOUR email here

accession = sys.argv[1]
start = int(sys.argv[2])
end = int(sys.argv[3])
out_file = sys.argv[4]

handle = Entrez.efetch(db="nuccore", id=accession, rettype="gbwithparts", retmode="text",
                       seq_start=start, seq_stop=end)
text = handle.read()
handle.close()

with open(out_file, "w") as out:
    out.write(text)
print(f"wrote {len(text)} characters to {out_file}")
