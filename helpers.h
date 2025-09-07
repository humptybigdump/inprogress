/*
	________             _____      ________________________
	___  __ \______________  /________  ____/__  /___  ____/
	__  /_/ /_  ___/  __ \  __/  __ \  / __ __  / __  /_
	_  ____/_  /   / /_/ / /_ / /_/ / /_/ / _  /___  __/
	/_/     /_/    \____/\__/ \____/\____/  /_____/_/

   ___/ minimalistic prototyping framework for OpenGL demos and practical courses
   ___/ Carsten Dachsbacher
   ___/ (ASCII font generator: http://patorjk.com/software/taag/)

   ___/ helpers...
*/

#ifndef __HELPERS_H
#define __HELPERS_H

#include "stdafx.h"

const char* tmpStrCat(const char* s1, const char* s2);

// returns uint in [0;2^digits]
unsigned int halton2_inverse(unsigned int index, unsigned int digits);

// returns unsigned int in [0;3^digits]
unsigned int halton3_inverse(unsigned int index, unsigned int digits);

#endif
