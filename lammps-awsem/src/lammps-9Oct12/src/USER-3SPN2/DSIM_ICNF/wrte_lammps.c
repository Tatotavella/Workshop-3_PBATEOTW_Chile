
/*********************************************************************
**********************************************************************
****        <<<<< 3SPN.2 Configuration Generator    >>>>>         ****
****                                                              ****  
****        Dan Hinckley    `                                     ****
****        Instutite for Molecular Engineering                   ****
****        University of Chicago                                 ****
****        Chicago, IL 60637                                     ****
****                                                              ****
**********************************************************************
*********************************************************************/

#include "decl_ilib.h"
#include "decl_ivar.h"
#include "decl_ifun.h"

void wrte_lammps(char *dnme)
{
    long i, ncyc;
    char fnme[_TW_];
    FILE *fptr;

    // Conversion factor for converting from kJ to kCal
    double kJ2kCal = 0.239005736; 
    double k2bond, k3bond, k4bond,kbend, ktors, bhfx, bhfy, bhfz;
    long stea, steb, stec, sted, typa, typb, typc, typd, match, j;

    // Getting the correct units for bonded interactions
    k2bond = 0.600000 * kJ2kCal;
    k3bond = 0.000000 * kJ2kCal;
    k4bond = k2bond * 100.0;
    kbend = 200.000000 * kJ2kCal;
    ktors = 6.000000 * kJ2kCal;

    sprintf(fnme, "%s/conf_lammps.in", dnme);
    fptr = fopen(fnme, "w");

    fprintf(fptr, "LAMMPS Description for 3SPN.2\n\n");
    ncyc = site.totl;

    // Writing down the number of atoms and bonded interactions
    fprintf(fptr, "\t%ld atoms\n",ncyc);
    fprintf(fptr, "\t%ld bonds\n",cbon);
    fprintf(fptr, "\t%ld angles\n",cben);
    fprintf(fptr, "\t%ld dihedrals\n\n",ctor);
    
    long ntype_atom, ntype_bond, ntype_angle, ntype_dihedral;
    ntype_atom = 14;
    ntype_bond = 6;
    ntype_angle = 26;
    ntype_dihedral = 2;
    // Specifying the number of types
    fprintf(fptr, "\t%ld atom types\n",ntype_atom);
    fprintf(fptr, "\t%ld bond types\n",ntype_bond);
    fprintf(fptr, "\t%ld angle types\n",ntype_angle);
    fprintf(fptr, "\t%ld dihedral types\n\n",ntype_dihedral);

    // Specifying the box size
    bhfx = boxs.lenx / 2.0;
    bhfy = boxs.leny / 2.0;
    bhfz = boxs.lenz / 2.0;
    fprintf(fptr, "\t%lf\t%lf xlo xhi\n", -bhfx ,bhfx);
    fprintf(fptr, "\t%lf\t%lf ylo yhi\n", -bhfy ,bhfy);
    fprintf(fptr, "\t%lf\t%lf zlo zhi\n\n", -bhfz ,bhfz);

    // Specifying the masses (gm/mol)
    fprintf(fptr,"Masses\n\n");
    fprintf(fptr,"\t%d\t%lf\n", 1,94.9696); // P
    fprintf(fptr,"\t%d\t%lf\n", 2,83.1104); // S
    fprintf(fptr,"\t%d\t%lf\n", 3,134.1220); // A
    fprintf(fptr,"\t%d\t%lf\n", 4,125.1078); // T
    fprintf(fptr,"\t%d\t%lf\n", 5,150.1214); // G
    fprintf(fptr,"\t%d\t%lf\n", 6,110.0964); // C
    fprintf(fptr,"\t%d\t%lf\n", 7,134.1220); // 5A
    fprintf(fptr,"\t%d\t%lf\n", 8,125.1078); // 5T
    fprintf(fptr,"\t%d\t%lf\n", 9,150.1214); // 5G
    fprintf(fptr,"\t%d\t%lf\n", 10,110.0964); // 5C
    fprintf(fptr,"\t%d\t%lf\n", 11,134.1220); // 3A
    fprintf(fptr,"\t%d\t%lf\n", 12,125.1078); // 3T
    fprintf(fptr,"\t%d\t%lf\n", 13,150.1214); // 3G
    fprintf(fptr,"\t%d\t%lf\n\n", 14,110.0964); // 3C

    // I use this same ordering of the indices for the rest of my forcefield. 
    // not consistent with the in-house 3SPN.2. I won't worry about it. 

    // Specifying the pair coefficients

    // xXX epsilon sigma R_solv lambda Gsolve
    // epsilons sigma

    double eps_r = 1.000000 * kJ2kCal; 
    fprintf(fptr,"Pair Coeffs\n\n");
    fprintf(fptr,"\t%d\t%lf\t%lf\n",1,eps_r, 2.0 * 2.25);
    fprintf(fptr,"\t%d\t%lf\t%lf\n",2,eps_r, 2.0 * 3.10); 
    fprintf(fptr,"\t%d\t%lf\t%lf\n",3,eps_r, 2.0 * 2.70); 
    fprintf(fptr,"\t%d\t%lf\t%lf\n",4,eps_r, 2.0 * 3.55); 
    fprintf(fptr,"\t%d\t%lf\t%lf\n",5,eps_r, 2.0 * 2.45); 
    fprintf(fptr,"\t%d\t%lf\t%lf\n",6,eps_r, 2.0 * 3.20); 
    fprintf(fptr,"\t%d\t%lf\t%lf\n",7,eps_r, 2.0 * 2.70); 
    fprintf(fptr,"\t%d\t%lf\t%lf\n",8,eps_r, 2.0 * 3.55); 
    fprintf(fptr,"\t%d\t%lf\t%lf\n",9,eps_r, 2.0 * 2.45); 
    fprintf(fptr,"\t%d\t%lf\t%lf\n",10,eps_r, 2.0 * 3.20);
    fprintf(fptr,"\t%d\t%lf\t%lf\n",11,eps_r, 2.0 * 2.70);
    fprintf(fptr,"\t%d\t%lf\t%lf\n",12,eps_r, 2.0 * 3.55);
    fprintf(fptr,"\t%d\t%lf\t%lf\n",13,eps_r, 2.0 * 2.45);
    fprintf(fptr,"\t%d\t%lf\t%lf\n",14,eps_r, 2.0 * 3.20);
    /*
    fprintf(fptr,"\t%d\t%lf\t%lf\t%lf\t%lf\t%lf\n",1,eps_r, 2.0 * 2.25, 2.25, 6.0,0.05 * -83.225 * kJ2kCal);
    fprintf(fptr,"\t%d\t%lf\t%lf\t%lf\t%lf\t%lf\n",2,eps_r, 2.0 * 3.10, 3.10, 4.5,0.05 * 65.375 * kJ2kCal);
    fprintf(fptr,"\t%d\t%lf\t%lf\t%lf\t%lf\t%lf\n",3,eps_r, 2.0 * 2.70, 3.12, 4.5,0.05 * 45.8 * kJ2kCal);
    fprintf(fptr,"\t%d\t%lf\t%lf\t%lf\t%lf\t%lf\n",4,eps_r, 2.0 * 3.55, 3.86, 4.5,0.05 * 39.2 * kJ2kCal);
    fprintf(fptr,"\t%d\t%lf\t%lf\t%lf\t%lf\t%lf\n",5,eps_r, 2.0 * 2.40, 3.10, 4.5,0.05 * 40.2 * kJ2kCal);
    fprintf(fptr,"\t%d\t%lf\t%lf\t%lf\t%lf\t%lf\n",6,eps_r, 2.0 * 3.45, 3.52, 4.5,0.05 * 51.6 * kJ2kCal);
    fprintf(fptr,"\t%d\t%lf\t%lf\t%lf\t%lf\t%lf\n",7,eps_r, 2.0 * 2.70, 3.12, 4.5,0.05 * 45.8 * kJ2kCal);
    fprintf(fptr,"\t%d\t%lf\t%lf\t%lf\t%lf\t%lf\n",8,eps_r, 2.0 * 3.55, 3.86, 4.5,0.05 * 39.2 * kJ2kCal);
    fprintf(fptr,"\t%d\t%lf\t%lf\t%lf\t%lf\t%lf\n",9,eps_r, 2.0 * 2.40, 3.10, 4.5,0.05 * 40.2 * kJ2kCal);
    fprintf(fptr,"\t%d\t%lf\t%lf\t%lf\t%lf\t%lf\n",10,eps_r, 2.0 * 3.45, 3.52, 4.5,0.05 * 51.6 * kJ2kCal);
    fprintf(fptr,"\t%d\t%lf\t%lf\t%lf\t%lf\t%lf\n",11,eps_r, 2.0 * 2.70, 3.12, 4.5,0.05 * 45.8 * kJ2kCal);
    fprintf(fptr,"\t%d\t%lf\t%lf\t%lf\t%lf\t%lf\n",12,eps_r, 2.0 * 3.55, 3.86, 4.5,0.05 * 39.2 * kJ2kCal);
    fprintf(fptr,"\t%d\t%lf\t%lf\t%lf\t%lf\t%lf\n",13,eps_r, 2.0 * 2.40, 3.10, 4.5,0.05 * 40.2 * kJ2kCal);
    fprintf(fptr,"\t%d\t%lf\t%lf\t%lf\t%lf\t%lf\n",14,eps_r, 2.0 * 3.45, 3.52, 4.5,0.05 * 51.6 * kJ2kCal);
    */
    fprintf(fptr,"\n");
    // Remember, the units are in kcal/mol and angtroms or radians

    // Specifying the pair coefficients
    fprintf(fptr,"Bond Coeffs\n\n");
    // <k2> <k4> <r0>
    /*
    fprintf(fptr,"\t%d\t%lf\t%lf\t%lf\n",1,k2bond,k4bond,3.899); // PS
    fprintf(fptr,"\t%d\t%lf\t%lf\t%lf\n",2,k2bond,k4bond,3.559); // SP
    fprintf(fptr,"\t%d\t%lf\t%lf\t%lf\n",3,k2bond,k4bond,4.670); // SA
    fprintf(fptr,"\t%d\t%lf\t%lf\t%lf\n",4,k2bond,k4bond,4.189); // ST
    fprintf(fptr,"\t%d\t%lf\t%lf\t%lf\n",5,k2bond,k4bond,4.829); // SG
    fprintf(fptr,"\t%d\t%lf\t%lf\t%lf\n\n",6,k2bond,k4bond,3.844); // SC
    */
    fprintf(fptr,"\t%d\t%lf\t%lf\t%lf\t%lf\n",1,3.899,k2bond,k3bond,k4bond); // PS
    fprintf(fptr,"\t%d\t%lf\t%lf\t%lf\t%lf\n",2,3.559,k2bond,k3bond,k4bond); // SP
    fprintf(fptr,"\t%d\t%lf\t%lf\t%lf\t%lf\n",3,4.670,k2bond,k3bond,k4bond); // SA
    fprintf(fptr,"\t%d\t%lf\t%lf\t%lf\t%lf\n",4,4.189,k2bond,k3bond,k4bond); // ST
    fprintf(fptr,"\t%d\t%lf\t%lf\t%lf\t%lf\n",5,4.829,k2bond,k3bond,k4bond); // SG
    fprintf(fptr,"\t%d\t%lf\t%lf\t%lf\t%lf\n\n",6,3.844, k2bond,k3bond,k4bond); // SC

    // Specifying the angle coefficients
    fprintf(fptr,"Angle Coeffs\n\n");

    // Harmonic <K> <theta0>
    fprintf(fptr,"\t%d\tharmonic\t%lf\t%lf\n",1,kbend,94.49); // SPS
    fprintf(fptr,"\t%d\tharmonic\t%lf\t%lf\n",2,kbend,120.15); // PSP
    fprintf(fptr,"\t%d\tharmonic\t%lf\t%lf\n",3,kbend,112.07); // ASP
    fprintf(fptr,"\t%d\tharmonic\t%lf\t%lf\n",4,kbend,116.68); // TSP
    fprintf(fptr,"\t%d\tharmonic\t%lf\t%lf\n",5,kbend,110.12); // GSP
    fprintf(fptr,"\t%d\tharmonic\t%lf\t%lf\n",6,kbend,110.33); // CSP
    fprintf(fptr,"\t%d\tharmonic\t%lf\t%lf\n",7,kbend,103.53); // PSA
    fprintf(fptr,"\t%d\tharmonic\t%lf\t%lf\n",8,kbend,92.06); // PST
    fprintf(fptr,"\t%d\tharmonic\t%lf\t%lf\n",9,kbend,107.40); // PSG
    fprintf(fptr,"\t%d\tharmonic\t%lf\t%lf\n",10,kbend,103.79); // PSC

    // A = 0; T = 1; G = 2; C = 3; (different than in-house 3SPN.2)
    double bstk_sigm[16], bstk_thta[16], bstk_eps[16], bstk_alpha, bstk_range;
    bstk_alpha = 3.0;
    bstk_range = 6.0;
    
    /*
    bstk_sigm[0][0] = 3.718; // AA
    bstk_sigm[0][1] = 3.668; // AT
    bstk_sigm[0][2] = 3.829; // AG
    bstk_sigm[0][3] = 3.723; // AC
    bstk_sigm[1][0] = 4.253; // TA
    bstk_sigm[1][1] = 3.986; // TT
    bstk_sigm[1][2] = 4.429; // TG
    bstk_sigm[1][3] = 4.102; // TC
    bstk_sigm[2][0] = 3.579; // GA
    bstk_sigm[2][1] = 3.588; // GT
    bstk_sigm[2][2] = 3.666; // GG
    bstk_sigm[2][3] = 3.627; // GC
    bstk_sigm[3][0] = 4.116; // CA
    bstk_sigm[3][1] = 3.852; // CT
    bstk_sigm[3][2] = 4.289; // CG 
    bstk_sigm[3][3] = 3.959; // CC
    */

    /*
    Old distances
    bstk_sigm[0] = 3.716;  // AA
    bstk_sigm[1] = 3.668;  // AT
    bstk_sigm[2] = 3.829;  // AG
    bstk_sigm[3] = 3.723;  // AC
    bstk_sigm[4] = 4.253;  // TA
    bstk_sigm[5] = 3.986;  // TT
    bstk_sigm[6] = 4.429;  // TG
    bstk_sigm[7] = 4.102;  // TC
    bstk_sigm[8] = 3.579;  // GA
    bstk_sigm[9] = 3.588;  // GT
    bstk_sigm[10] = 3.666; // GG
    bstk_sigm[11] = 3.627; // GC
    bstk_sigm[12] = 4.116; // CA
    bstk_sigm[13] = 3.852; // CT
    bstk_sigm[14] = 4.289; // CG
    bstk_sigm[15] = 3.959; // CC
    */

    bstk_sigm[0] = 3.716;
    bstk_sigm[1] = 3.675;
    bstk_sigm[2] = 3.827;
    bstk_sigm[3] = 3.975;
    bstk_sigm[4] = 4.238;
    bstk_sigm[5] = 3.984;
    bstk_sigm[6] = 4.416;
    bstk_sigm[7] = 4.468;
    bstk_sigm[8] = 3.576;
    bstk_sigm[9] = 3.598;
    bstk_sigm[10] = 3.664;
    bstk_sigm[11] = 3.822;
    bstk_sigm[12] = 3.859;
    bstk_sigm[13] = 3.586;
    bstk_sigm[14] = 4.030;
    bstk_sigm[15] = 3.957;

    // Equilibrium angles for base-stacking interactions used for modulating
    /*
    bstk_thta[0][0] = 101.70; // AA
    bstk_thta[0][2] = 86.31;  // AT
    bstk_thta[0][1] = 105.86; // AG
    bstk_thta[0][3] = 88.14;  // AC
    bstk_thta[2][0] = 101.91; // TA
    bstk_thta[2][2] = 89.79;  // TT
    bstk_thta[2][1] = 104.69; // TG
    bstk_thta[2][3] = 90.72;  // TC
    bstk_thta[1][0] = 101.31; // GA
    bstk_thta[1][2] = 85.05;  // GT
    bstk_thta[1][1] = 105.94; // GG
    bstk_thta[1][3] = 87.16;  // GC
    bstk_thta[3][0] = 105.67; // CA
    bstk_thta[3][2] = 92.84;  // CT
    bstk_thta[3][1] = 108.64; // CG
    bstk_thta[3][3] = 93.92;  // CC
    */

    /*
    Old topology
    bstk_thta[0] = 101.70;    // AA
    bstk_thta[1] = 86.31;     // AT
    bstk_thta[2] = 105.86;    // AG
    bstk_thta[3] = 88.14;     // AC
    bstk_thta[4] = 101.91;    // TA
    bstk_thta[5] = 89.79;     // TT
    bstk_thta[6] = 104.69;    // TG
    bstk_thta[7] = 90.72;     // TC
    bstk_thta[8] = 101.31;    // GA
    bstk_thta[9] = 85.05;     // GT
    bstk_thta[10] = 105.94;   // GG
    bstk_thta[11] = 87.16;    // GC
    bstk_thta[12] = 105.67;   // CA
    bstk_thta[13] = 92.84;    // CT
    bstk_thta[14] = 108.64;   // CG
    bstk_thta[15] = 93.92;    // CC
    */
    
    // New
    bstk_thta[0] = 101.15;      // AA
    bstk_thta[1] = 85.94;       // AT
    bstk_thta[2] = 105.26;      // AG
    bstk_thta[3] = 90.26;       // AC
    bstk_thta[4] = 101.59;      // TA
    bstk_thta[5] = 89.5;        // TT
    bstk_thta[6] = 104.31;      // TG
    bstk_thta[7] = 90.82;       // TC
    bstk_thta[8] = 100.89;      // GA
    bstk_thta[9] = 84.83;       // GT
    bstk_thta[10] = 105.48;     // GG
    bstk_thta[11] = 90.18;      // GC
    bstk_thta[12] = 115.95;     // CA
    bstk_thta[13] = 101.51;     // CT
    bstk_thta[14] = 119.32;     // CG
    bstk_thta[15] = 104.49;     // CC

    // Strengths of interactions
    /*
    A		A		19.644	3.000	6.000
    A		T		20.607	3.000	6.000
    A		G		22.573	3.000	6.000
    A		C		19.435	3.000	6.000
    T		A		15.795	3.000	6.000
    T		T		19.644	3.000	6.000
    T		G		20.983	3.000	6.000
    T		C		17.301	3.000	6.000
    G		A		17.301	3.000	6.000
    G		T		19.435	3.000	6.000
    G		G		21.025	3.000	6.000
    G		C		18.807	3.000	6.000
    C		A		20.983	3.000	6.000
    C		T		22.573	3.000	6.000
    C		G		24.079	3.000	6.000
    C		C		21.025	3.000	6.000
    */

    bstk_eps[0] = 14.39;  // AA
    bstk_eps[1] = 14.34;  // AT
    bstk_eps[2] = 13.25;  // AG
    bstk_eps[3] = 14.51;  // AC
    bstk_eps[4] = 10.37;  // TA
    bstk_eps[5] = 13.36;  // TT
    bstk_eps[6] = 10.34;  // TG
    bstk_eps[7] = 12.89;  // TC
    bstk_eps[8] = 14.81;  // GA
    bstk_eps[9] = 15.57;  // GT
    bstk_eps[10] = 14.93; // GG
    bstk_eps[11] = 15.39; // GC
    bstk_eps[12] = 11.42; // CA
    bstk_eps[13] = 12.79; // CT
    bstk_eps[14] = 10.52; // CG
    bstk_eps[15] = 13.24; // CC

    for (i = 0; i < 16; i++)
    {
        fprintf(fptr,"\t%ld\tstacking/3spn2\t%lf\t%lf\t%lf\t%lf\t%lf\n",i+11,bstk_eps[i] * kJ2kCal,bstk_sigm[i], bstk_thta[i], bstk_alpha, bstk_range);
    }
    fprintf(fptr,"\n");

    // Specifying the dihedral coefficients
    // <k> <phi> <sigm>
    fprintf(fptr,"Dihedral Coeffs\n\n");
    fprintf(fptr,"\t%d\t%lf\t%lf\t%lf\n",1,ktors, -359.17,0.3000); // SPSP
    fprintf(fptr,"\t%d\t%lf\t%lf\t%lf\n\n",2,ktors, -334.79,0.3000); // PSPS

    // First, we identify the 5' and 3' sites...
    int prime_shift[ncyc];
    long ndna = site.dna_totl;
    for (i = 0; i < ndna; i++)
    {
        prime_shift[i] = 0;
        if (i == 1) prime_shift[i] = 4;
        if (i == ndna - 1) prime_shift[i] = 8;
        if (comp)
        {
            if (i == ndna/2 - 1) prime_shift[i] = 8;
            if (i == ndna/2 + 1) prime_shift[i] = 4;
        }

    }

    // Specifying the Atoms
    fprintf(fptr,"Atoms\n\n");
    long moln = 1;
    for (i = 0; i < ndna; i++)
    {
        fprintf(fptr, "\t%ld",i+1); // Atom number
        if (comp)
        {
            if (i == ndna/ 2)
            {
                moln++;
            }
        }
        fprintf(fptr, "\t%ld",moln); // Molecule number
        fprintf(fptr, "\t%ld",atom[i].stid2 + prime_shift[i]); // Atom type
        fprintf(fptr, "\t%lf",atom[i].chrg); // Atom charge
        fprintf(fptr, "\t%lf",atom[i].xval); // Atom x coord
        fprintf(fptr, "\t%lf",atom[i].yval); // Atom y coord
        fprintf(fptr, "\t%lf\n",atom[i].zval); // Atom z coord
    }
    fprintf(fptr,"\n");

    // Specifying the bonds

    // First I classify each of the bonds
    long bt[6][2];
    bt[0][0] = 1; bt[0][1] = 2; // PS
    bt[1][0] = 2; bt[1][1] = 1; // SP
    bt[2][0] = 2; bt[2][1] = 3; // SA
    bt[3][0] = 2; bt[3][1] = 4; // ST
    bt[4][0] = 2; bt[4][1] = 5; // SG
    bt[5][0] = 2; bt[5][1] = 6; // SC

    long b[cbon];
	for(i=0; i < cbon; i++)
	{	
        stea = bond[i].aste;
		steb = bond[i].bste;
		typa = atom[stea].stid2;
		typb = atom[steb].stid2;
		match = 0;
		for(j = 0; j < ntype_bond; j++)
		{	
            if( (typa == bt[j][0]) && (typb == bt[j][1]) )
			{	
                match = 1;
				b[i] = j+1;
				break;
			}
		}
		if(!match)
		{	
            printf("WARNING: classify(): could not classify bond %ld\n", i+1);
		}
	}

    fprintf(fptr,"Bonds\n\n");
    for (i = 0; i < cbon; i++)
    {
        fprintf(fptr,"\t%ld\t%ld\t%ld\t%ld\n",i+1,b[i],bond[i].aste + 1, bond[i].bste + 1);
    }
    fprintf(fptr,"\n");

    // Specifying the angles
    // First I classify each of the bonds
    long at[26][3];
    at[0][0] = 2; at[0][1] = 1; at[0][2] = 2;// SPS
    at[1][0] = 1; at[1][1] = 2; at[1][2] = 1;// PSP
    at[2][0] = 3; at[2][1] = 2; at[2][2] = 1;// ASP
    at[3][0] = 4; at[3][1] = 2; at[3][2] = 1;// TSP
    at[4][0] = 5; at[4][1] = 2; at[4][2] = 1;// GSP
    at[5][0] = 6; at[5][1] = 2; at[5][2] = 1;// CSP
    at[6][0] = 1; at[6][1] = 2; at[6][2] = 3;// PSA
    at[7][0] = 1; at[7][1] = 2; at[7][2] = 4;// PST
    at[8][0] = 1; at[8][1] = 2; at[8][2] = 5;// PSG
    at[9][0] = 1; at[9][1] = 2; at[9][2] = 6;// PSC

    for (i = 0; i < 16; i++)
    {
        at[10 + i][0] = 2;
        at[10 + i][1] = i / 4 + 3;
        at[10 + i][2] = i % 4 + 3;
    }

    long a[cben];
	for(i=0; i < cben; i++)
	{	
        stea = bend[i].aste;
		steb = bend[i].bste;
		stec = bend[i].cste;
		typa = atom[stea].stid2;
		typb = atom[steb].stid2;
		typc = atom[stec].stid2;
		match = 0;
		for(j = 0; j < ntype_angle; j++)
		{	
            if( (typa == at[j][0]) && (typb == at[j][1]) && (typc == at[j][2]) )
			{	
                match = 1;
				a[i] = j+1;
				break;
			}
		}
		if(!match)
		{	
            printf("WARNING: classify(): could not classify bend %ld\n", i+1);
		}
	}

    fprintf(fptr,"Angles\n\n");
    for (i = 0; i < cben; i++)
    {
        fprintf(fptr,"\t%ld\t%ld\t%ld\t%ld\t%ld\n",i+1,a[i],bend[i].aste + 1, bend[i].bste + 1, bend[i].cste + 1); 
    }
    fprintf(fptr,"\n");

    // Specifying the dihedarls

    // First I classify each of the bonds
    long dt[2][4];
    dt[0][0] = 2; dt[0][1] = 1; dt[0][2] = 2; dt[0][3] = 1; // SPSP
    dt[1][0] = 1; dt[1][1] = 2; dt[1][2] = 1; dt[1][3] = 2; // PSPS

    long d[ctor];
	for(i=0; i < ctor; i++)
	{	
        stea = tors[i].aste;
		steb = tors[i].bste;
		stec = tors[i].cste;
		sted = tors[i].dste;
		typa = atom[stea].stid2;
		typb = atom[steb].stid2;
		typc = atom[stec].stid2;
		typd = atom[sted].stid2;
		match = 0;
		for(j = 0; j < ntype_dihedral; j++)
		{	
            if( (typa == dt[j][0]) && (typb == dt[j][1]) && (typc = dt[j][2]) && (typd = dt[j][3]) )
			{	
                match = 1;
				d[i] = j+1;
				break;
			}
		}
		if(!match)
		{	
            printf("WARNING: classify(): could not classify dihedral %ld\n", i+1);
		}
	}

    fprintf(fptr,"Dihedrals\n\n");
    for (i = 0; i < ctor; i++)
    {
        fprintf(fptr,"\t%ld\t%ld\t%ld\t%ld\t%ld\t%ld\n",i+1,d[i],tors[i].aste + 1, tors[i].bste + 1, tors[i].cste + 1, tors[i].dste +1);
    }
}
