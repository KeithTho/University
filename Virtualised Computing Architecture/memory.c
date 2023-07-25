#include<stdio.h>
#include <stdlib.h>
#include <string.h>
#pragma warning(disable:4996)

#define ARRAY_SIZE 1024*1024*512

int main(int argc, char** argv) {

	printf("\n---Benchmark Started---\n");
	long long twoGig = 66000;
	void* mem = malloc(twoGig);
	FILE* fp = fopen("test.bin", "wb");

	long long count = twoGig;
	while (count > 0)
	{
		long long current = fwrite(mem, count, 1, fp);
		if (current == 0)
			break;
		count -= current;
	}
	fclose(fp);
	printf("---Benchmark Finished--- \n");
	return 0;

}
