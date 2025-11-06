#include <stdio.h>
#include <limits.h>

int main() {
    printf("sizeof(char): %zu\n", sizeof(char));
    printf("sizeof(short): %zu\n", sizeof(short));
    printf("sizeof(int): %zu\n", sizeof(int));
    printf("sizeof(long): %zu\n", sizeof(long));
    printf("sizeof(long long): %zu\n", sizeof(long long));
    printf("sizeof(float): %zu\n", sizeof(float));
    printf("sizeof(double): %zu\n", sizeof(double));

    printf("UCHAR_MAX: %zu\n", UCHAR_MAX);
    printf("USHRT_MAX: %zu\n", USHRT_MAX);
    printf("UINT_MAX: %zu\n", UINT_MAX);
    printf("ULONG_MAX: %zu\n", ULONG_MAX);
    printf("ULLONG_MAX: %zu\n", ULLONG_MAX);

    // overflow
    signed char c = 127;
    c += 1;
    printf("\n127 (signed) + 1 = %d\n", c);

    unsigned char u = 127;
    u += 1;
    printf("\n127 (unsigned) + 1 = %d\n", u);
}
