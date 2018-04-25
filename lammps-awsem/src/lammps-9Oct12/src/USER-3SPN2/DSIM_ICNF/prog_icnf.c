
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

#define MAIN
#include "decl_ilib.h"
#include "decl_ivar.h"
#include "decl_ifun.h"

int main(int argc, char **argv)
{
    char comd[100];
    time_t iclk;
    FILE *fptr;

    if (argc != 4)
    {
        fprintf(stdout,
            "This utility requires three (3) arguments:\n");
        fprintf(stdout, "[1] sequence input file\n");
        fprintf(stdout, "[2] switch for complementarity\n");
        fprintf(stdout, "[3] directory name to store output\n");
        fprintf(stdout, "Please try again.\n");
        exit(1);
    }

    // A bit of bulletproofing
    if (NULL == (fptr = fopen(argv[1], "r")))
    {
        fprintf(stdout, "Input file %s is not accessible.\n",
            argv[1]);
        exit(1);
    }
    fclose(fptr);

    mkdir(argv[3], S_IRWXU);
    comp = atoi(argv[2]);
    time(&iclk);
    genr_rtmp();

    read_sequ(argv[1]);
    sprintf(comd, "cp -f %s %s", argv[1], argv[3]);
    system(comd);

    genr_dnac();
    genr_topo();

    wrte_rpsf(argv[3]);
    wrte_rxyz(argv[3]);
    wrte_lammps(argv[3]);
    return (0);
}
