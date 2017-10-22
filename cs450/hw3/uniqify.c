/*THIS CODE IS MY OWN WORK, IT WAS WRITTEN WITHOUT CONSULTING A TUTOR OR CODE WRITTEN BY OTHER STUDENTS - NAHOM OGBAZGHI*/
#include <stdlib.h>
#include <stdio.h>
#include <ctype.h>
#include <unistd.h>
#include <string.h>

int main (int argc, char * argv[]){
	pid_t pida, pidb;
	int fdsort[2],fdsupp[2];
	
	//begins piping
	if (pipe(fdsort) == -1){
		perror("pipe");
		exit(1);
	}
	//begins piping
	if (pipe(fdsupp) == -1){
		perror("pipe");
		exit(1);
	}
	
	pida = fork();
	if(pida == 0) {//Child 1 - SORT
		dup2(fdsort[0], 0);//directing values IN fdsort to stdIN
		dup2(fdsupp[1],1);//directing values FROM fdsupp[1] to stdOUT
		close(fdsupp[0]);
		close(fdsupp[1]);
		close(fdsort[0]);
		close(fdsort[1]);
		execl("/bin/sort", "/bin/sort", 0);
		exit(1);
	}
	
	pidb = fork();
	if (pidb == 0){//Child 2 - Suppress
		close(fdsupp[1]);
		close(fdsort[0]);
		close(fdsort[1]);
		int counter = 1;
		FILE *fp = fdopen(fdsupp[0],"r");//fp receives sorted characters that are now strings seperated by new line
		char * prev = malloc(32);
		fgets(prev, 32, fp);
		char * curr = malloc(32);
		while (fgets(curr, 32, fp) != NULL) {
			if (strcmp(prev, curr) != 0){
				int index = strchr(prev,'\n')-prev;
				if (index > 2){
					printf("%5d %s", counter, prev);
				}
				counter = 1;
				strncpy(prev, curr, 32);
			} else {
				strncpy(prev, curr, 32);
				counter++;
			}
		}
		printf("%5d %s", counter, prev);//For the last prev
		fclose(fp);
		exit(1);
	}
	
	//Parent - Parse
	FILE *sinput = fdopen(0,"r");//sinput is receiving info from the standard input
	FILE *fp = fdopen(fdsort[1],"w");//fp receives modified characters
	int ch;
	int counter = 0;
	while ((ch = fgetc(sinput)) != EOF){
		if (isalpha(ch)){
			if(counter <30){
				fputc(tolower(ch), fp);
				counter++;
			} else if(counter == 30){ //31st character in a row is reached. Add a new line instead
				fputc('\n', fp);
				counter++;
			} else { // any sequential characters after the 30th in a row
				continue;}
		} else if(!(isalpha(ch))){
			fputc('\n', fp);
			counter=0;
		}
	}
	fclose(sinput);
	fclose(fp);
	close(fdsort[0]);
	close(fdsupp[0]);
	close(fdsupp[1]);
	wait(NULL);
	wait(NULL);
	exit(1);
}
