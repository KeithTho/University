#include<stdio.h>
#pragma warning(disable:4996)

int main(int argc, char** argv) {

	printf("\n---Benchmark Started---\n");
	unsigned int count = 1;
	char result = '1';
	FILE* fp;
	fp = fopen("test.txt", "w");
	fclose(fp);

	while (count != 500001) {
		count++;
		fp = fopen("test.txt", "r");
		result = getc(fp);
		fclose(fp);
		fp = fopen("test.txt", "a+");
		putc(result, fp);
		fclose(fp);

	}
	printf("---Benchmark Finished--- \n");
	return 0;
}
