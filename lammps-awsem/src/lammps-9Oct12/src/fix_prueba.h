#ifdef FIX_CLASS

FixStyle(fixprueba,FixPRUEBA)     // This registers this fix class with LAMMPS. The FixStyle(name_in_input_script,class_name) function 			                  // allows you to specify the keyword in the input script that will trigger the creation of this class

#else

#ifndef LMP_FIX_PRUEBA_H     //  These are header guards.
#define LMP_FIX_PRUEBA_H     //  These are header guards.

#include "fix.h"         // Must have this because our FixPrueba is derived from Fix...

namespace LAMMPS_NS {

class FixPRUEBA : public Fix {
// The contents of your class go here i.e. member variables and methods etc...

 public:
  FixPRUEBA(class LAMMPS *, int, char **);
  int setmask();
  void end_of_step();
  //int numero;
  //double real;
  //virtual void hacer_algo_virtual();
  //int hacer_algo_entero();
	  
 protected:
  double numero_protegido;

	
};


}


#endif
#endif

