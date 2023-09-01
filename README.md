# filter-propka
Python script to get residues from a PROPKA output that have a pKa more or less than a threshold. 

For example, if you wanted to find which residues are estimated to be protonated at pH 7.

This can be used for choosing protonation states when setting up molecular dynamics simulations of a protein.

**Usage:** 

filter-propka.py [-h] [--resname_value RESNAME_VALUE] [--chain_value CHAIN_VALUE] file_path pka_threshold


**positional arguments:**

**file_path**             Path to the PROPKA output file (.pka)
 
**pka_threshold**         Threshold for pKa filtering, i.e. pH. This is a numeric value e.g. 7

**options:**

**-h, --help**            show this help message and exit

**--resname_value RESNAME_VALUE**
                        Resname value to filter (ASP, GLU, HIS, LYS). If none supplied then all titratable residues are given.
                        
**--chain_value CHAIN_VALUE**
                      Chain value to filter. If none then all chains are given.
