#include <stdio.h>
#include <stdlib.h>
int mult(int x, int y){
    return(x*y);
}

int main(void){
    int b = mult(2,3);
    printf("%d\n\n", b);
    printf("Hello World\n\n");
    if(b==6){
        printf("b is not 6");
        exit(1);
    };
    exit(0);
}
