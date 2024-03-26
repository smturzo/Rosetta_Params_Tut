1. Made the Test_Molecule.inp file with software Avogadro.
   b. Used Avogadro's input generator function to get the coordinates
   a. Within the Test_Molecule.inp the grabbed coordinates are
   between $DATA and $END and added the following QM settings 
   these are above the $DATA. 
   c. Ran QM calculation with GAMESS. Check run_gms.sh to see
   how this was run
   d. Let Avogadro figure out the charge and multiplicity 
    (ICHARG=X MULT=X respectively, this will be a number
    based on your molecule) of your molecule.

2. The run_gms.sh is the slurm script to run a GAMESS calculation
   In this case geometry optimization plus single point energy.
   But the main thing is here:
   /mnt/home/vmulligan/GAMESS/gamess_openmp_2022_02/rungms Test_Molecule.inp 00 4 >& ../outputs/test_molecule.gamout
   Here's a translation of this:
   /path/to/gamess/rungms inputfile.inp [version number, usually 00] [number of processor, typically recommended to leave as 4] >& /path/to/output.gamout

3. Okay once the calculation completes, go to the 01_Outputs for the next README.txt
