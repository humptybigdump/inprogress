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

#include "stdafx.h"

static int curTempStr = 0;
static char temp[16][8192];

// do not tell your computer science professor about this!
const char* tmpStrCat(const char* s1, const char* s2)
{
    int s = curTempStr;
    curTempStr ++;
    curTempStr &= 15;
    strcpy(temp[s], s1);
    strcat(temp[s], s2);
    return temp[s];
}

// returns uint in [0;2^digits]
unsigned int halton2_inverse(unsigned int index, unsigned int digits)
{
    index = (index << 16) | (index >> 16);
    index = ((index & 0x00ff00ff) << 8) | ((index & 0xff00ff00) >> 8);
    index = ((index & 0x0f0f0f0f) << 4) | ((index & 0xf0f0f0f0) >> 4);
    index = ((index & 0x33333333) << 2) | ((index & 0xcccccccc) >> 2);
    index = ((index & 0x55555555) << 1) | ((index & 0xaaaaaaaa) >> 1);
    return index >> (32 - digits);
}

// returns unsigned int in [0;3^digits]
unsigned int halton3_inverse(unsigned int index, unsigned int digits)
{
    unsigned int result = 0;
    for (unsigned int d = 0; d < digits; ++d)
    {
        result = result * 3 + index % 3;
        index /= 3;
    }
    return result;
}
