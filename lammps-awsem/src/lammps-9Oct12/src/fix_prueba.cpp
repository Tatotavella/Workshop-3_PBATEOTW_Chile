#include "fix_prueba.h"

// Some common includes.
#include "stdio.h"
#include "string.h"
#include "atom.h"
#include "comm.h"
#include "force.h"
#include "update.h"
#include "respa.h"
#include "error.h"
#include "memory.h"

//In order to use MathExtra routines, include math_extra.h. This file contains math functions to work with arrays of doubles as with math vectors.
#include "math_extra.h"

using namespace LAMMPS_NS;

// The class constructor.
FixPRUEBA::FixPRUEBA(LAMMPS *lmp, int narg, char **arg) : Fix(lmp,narg,arg)
{
  // Constructor implementation here...  like parse keywords from arg[] array etc... (see `nh.cpp' for inspiration)
  // No se que va adentro de un constructor. Capaz va algo asi

  if (narg < 4) error->all(FLERR,"Illegal fix print command"); //Los primeros 3 valores de arg los lee lammps, el cuarto es el que mete el usuario, si no me pasa ningun valor (narg=3) tiro error.

  nevery = atoi(arg[3]); //Aca hago que el valor que metio el usuario, el cuarto argumento sea cada cuantos pasos llamamos al end_of_step().  
//nevery:  There is a special variable in Fix class called nevery which specify how often method end_of_step will be called. Thus all we need to do is just set it up.

  if (nevery <= 0) error->all(FLERR,"Illegal fix print command"); //si el tipo pone un valor negativo quiero tirar error, o 0.
}

// El setmask es siempre necesario.
//  Setmask is mandatory, as it determines when the fix will be invoked during the timestep. Fixes that perform time integration (nve, nvt, npt) implement initial_integrate() and final_integrate() to perform velocity Verlet updates. Fixes that constrain forces implement post_force().
//There are 8 most important methods:
//initial_integrate, post_integrate, pre_exchange, pre_neighbor, pre_force, post_force final_integrate, end_of_step. Orden en el algoritmo de Verlet
int FixPRUEBA::setmask()
{
  int mask = 0;
  mask |= FixConst::END_OF_STEP; //Uso end_of_step
  return mask;
}


// A method.
//FixPRUEBA::do_something()
//{
//  // Implementation...
//}
void FixPRUEBA::end_of_step()
{
  // for add3, scale3 uso mathextra
  using namespace MathExtra;
  double** v = atom->v; //Agarro las velocidades del sistema con el pointer a atom.
  int nlocal = atom->nlocal; //Cantidad de indices de atomos. 
  double localAvgVel[4]; // Armo un vector de largo 4 para poner velocidades en las 3 dimensiones y en el cuarto contar.
  memset(localAvgVel, 0, 4 * sizeof(double)); // Seteo del lugar en la memoria, el primer argumento es lo que se va a guardar, el segundo no tengo ni idea y el cuarto es el tamaño que es 4 veces el tamaño de un double porque voy a guardar 4 doubles.
  for (int particleInd = 0; particleInd < nlocal; ++particleInd) { //Recorro todos los indices de los atomos
    add3(localAvgVel, v[particleInd], localAvgVel); //Con esta funcion voy sumando adentro de localAvgVel las velocidades v[i]
  }
  localAvgVel[3] = nlocal; //El cuarto parametro lo pongo como el numero total de atomos.
  double globalAvgVel[4];
  memset(globalAvgVel, 0, 4 * sizeof(double)); // Otra vez seteo de lugar en memoria
  MPI_Allreduce(localAvgVel, globalAvgVel, 4, MPI_DOUBLE, MPI_SUM, world); //No tengo idea que hace esto
  scale3(1.0 / globalAvgVel[3], globalAvgVel); //Tampoco se que hace esto
  if (comm->me == 0) {
    printf("\%e, \%e, \%e\n",       //Printea a la pantalla los 3 valores
      globalAvgVel[0], globalAvgVel[1], globalAvgVel[2]);
  }
}

// ¿Y los destructores?



//void FixPRUEBA::hacer_algo_virtual()
//{
  //Ver que significa hacer algo virtual

//}

//int FixPRUEBA::hacer_algo_entero()
//{
//  real = 23.2; //¿Aca no tengo que llamarlo con la clase porque adentro de esto esta todo heredado?
//  int devolucion = 45;
//  return devolucion;
//}

// ¿Seteo de un valor? ¿Si esta afuera tengo que referenciarlo con el FixPRUEBA?

//FixPRUEBA::numero = 1;
//FixPRUEBA.numero = 2;

// Pointer hacia mi clase, ¿puedo aca?

//FixPRUEBA *pointer;
//pointer->numero = 3; 

//Ver que prohibe el numero protegido en el .h

// ME FALTAN TODOS LOS DESTRUCTORES!!!! ¿Cuando se usan?





