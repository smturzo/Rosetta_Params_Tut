This Directory is a bit more messy. But lets start with the files/folder you can ignore.
These are:
    1. test_error.txt  
    2. test_log.txt 

Things you will need to do here:
1. Convert the GAMESS output file to MOL file.
    a. I have done it with Open Babel
        i.   But any Open Babel version won't work
        ii.  Doug modified a version of it and it is this one:
             * https://github.com/dougrenfrew/openbabel
        iii. The commands to do this is in this script: obabel_command.sh
        iv.  The above will output this file: test_mol.mol
             * In this file look at line 66 - 76 
             * That part you will have to add on
               your own.
             * For convenience I have made another mol file called test_2_mol.mol
             * If you do: diff test_mol.mol test_2_mol.mol
             ** It will show the differences right away.
        v.   Okay so once you have added the things in line 66 - 76. You should be
             able to convert mols to params with the script: molfile_to_params_polymer.py

2. Convert the MOL file to params file
    For me this looks like this: ./molfile_to_params_polymer.py -i test_mol.mol -n HAL -p HAL
        i.  Above command could look different for you.
        ii. The above command should output: 
             * HAL.params 
             * HAL_0001.pdb
        iii. Once you the params file. You can test it with this pyrosetta script: run_ncaa_test.sh 
             * This calls ncaa_params_test.py 
             * The above pyrosetta script calls the pymol observer and if your pymol is set up 
               such that it is listening to pyrosetta, then you can visualize all the torsions
               of your small molecules.
             ** If you need help with setting up pymol observer let me know.

Note: The HAL folder is where I previously tried creating the params file from scratch for that Test_Molecule.inp
Note: The make_rot_lib_inputs folder is where I tried to make the Rotamer Library for the Test_Molecule.inp.
      * Can be ignored for now.
Note: Folders rosetta_py and molfile_to_params_polymer is needed to run molfile_to_params_polymer.py from this directory
Note: For your case run molfile_to_params_polymer.py however if you have been running before.
Note: Once you get up to here. Let me know what the next bugs through a github issue.
