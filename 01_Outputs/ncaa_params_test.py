#!/usr/bin/env python

'''
Simple script to test that a capped, dipeptide can have its backbone ans side chain torsions rotated  and be scored using mm_std
'''

#import pyrosetta
import pyrosetta.distributed
import argparse

def check_torsions( pose, pmm ):
    '''
    Sweep through each backbone and side chain torsion sending output to PyMOL for visual insepction
    '''

    print( "" )

    # backbone torsions
    n_bb_tor = len( pose.residue( 1 ).mainchain_torsions() )

    for bb_tor in range( 1, n_bb_tor+1 ) : # for each backbone torsion

        print( f"Working on BB torsion {bb_tor}" )
        pmm.set_PyMOL_model_name( f"BB_{bb_tor}" )
        tor_id = pyrosetta.rosetta.core.id.TorsionID( 1, pyrosetta.rosetta.core.id.BB, bb_tor )
        start_tor = pose.torsion( tor_id )

        for offset in range( 0, 370, 10 ):
            pose.set_torsion( tor_id, start_tor + float(offset) )
            pmm.apply( pose )

    # side chain torsions
    n_sc_tor = pose.residue( 1 ).nchi()

    for sc_tor in range( 1, n_sc_tor+1 ) : # for each side chain chi torsion

        print( f"Working on SC torsion {sc_tor}" )
        pmm.set_PyMOL_model_name( f"SC_{sc_tor}" )
        tor_id = pyrosetta.rosetta.core.id.TorsionID( 1, pyrosetta.rosetta.core.id.CHI, sc_tor )
        start_tor = pose.torsion( tor_id )

        for offset in range( 0, 370, 10 ):
            pose.set_torsion( tor_id, start_tor + float(offset) )
            pmm.apply( pose )


def check_score( pose, pmm ):
    '''
    Score the pose with MM_STD energy function and send the output to PyMOL
    '''
    sf = pyrosetta.create_score_function( "mm_std" )
    ener = sf( pose )
    pmm.set_PyMOL_model_name( "ScoreMMSTD" )
    pmm.apply( pose )
    pmm.send_energy( pose )
    print( f"Score of pose is {ener}" )

def main():

    # command line args
    parser = argparse.ArgumentParser()
    parser.add_argument( "--three_letter_code", required=True, help="Three letter code of the central AA you want to test", metavar="TLC" )
    parser.add_argument( "--extra_res_fa", help="additional residue type params files passed to rosetta via the extra_res_fa flag", metavar="FILE" )
    args = parser.parse_args()

    # init with extra residue
    flags = f'''
    -extra_res_fa {args.extra_res_fa} -out:level 10000
    '''
    pyrosetta.distributed.init( flags )

    # make a single residue capped pose, ACE-XYZ-NME
    pose = pyrosetta.pose_from_sequence(f"X[{args.three_letter_code}:MethylatedCtermProteinFull:AcetylatedNtermProteinFull]")
    #pose = pyrosetta.pose_from_sequence(f"X[{args.three_letter_code}:AcetylatedNtermDimethylatedCtermPeptoidFull]")
    #pose = pyrosetta.pose_from_sequence(f"X[{args.three_letter_code}:AcetylatedNtermProteinFull]")
    #pose = pyrosetta.pose_from_sequence(f"X[{args.three_letter_code}:MethylatedCtermProteinFull]")

    # setup PyMOL mover
    pmm = pyrosetta.rosetta.protocols.moves.PyMOLMover()
    pmm.keep_history( True )

    # checks
    check_score( pose, pmm )
    check_torsions( pose, pmm )


if __name__ == '__main__':
    main()
