#include <stdio.h>

int main() {
    int i = 5;  // integer
    // printf("i = %d\n", i);
    int *p;     // pointer to integer (location: undefined)

    p = &i;     // address-operator &
                // p contains the address of i
    // printf("p = %p\n", p);

    int j = *p; // dereference-operator *
                // j contains value that p points to
                // j == 5
    // printf("j = %d\n", j);

    *p = 10;    // dereference-operator *
                // change value that p points to
                // i == 10
    // printf("i = %d\n", i);

    // --------- POINTER TO POINTER

    int **pp; // pointer to pointer to integer (location: undefined)
    pp = &p;  // pp contains the address of p
    **pp = 15; // i == 15
    // printf("pp = %p\n", pp);
    // printf("*pp = %p\n", *pp);
    // printf("i = %p\n", i);

    // --------- DECLARATION

    int* p1, p2, p3; // only one of these is a pointer!
    
    // --------- POINTER ARITHMETIC
    
    int arr[5] = { 0, 2, 4, 6, 8 };
    int *ptr_to_middle = &arr[2];
    int *ptr_to_first = ptr_to_middle - 2;
    int *prt_to_last = ptr_to_middle + 2; // this is a jump of 8 bytes, not 2!
    
    // printf("ptr_to_middle = %p\n", ptr_to_middle);
    // printf("*ptr_to_middle = %d\n", *ptr_to_middle);
    // printf("ptr_to_middle + 1 = %p\n", ptr_to_middle + 1); // element at index 3
                                                       // pointer increased by sizeof(int)
    // printf("*(ptr_to_middle + 1) = %d\n", *(ptr_to_middle + 1));
    
    // --------- VOID AND NULL

    void *vp;           // pointer to unspecified type
    vp = (void *) &i;   // points to i, no type information
    
    p = NULL; // pointer to nothing (invalid pointer)
    // *p = 5;             // error
}
