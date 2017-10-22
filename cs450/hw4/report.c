/*THIS CODE IS MY OWN WORK, IT WAS WRITTEN WITHOUT CONSULTING A TUTOR OR CODE WRITTEN BY OTHER STUDENTS - NAHOM OGBAZGHI*/
#include <errno.h>
#include <string.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <stdio.h>
#include <stdlib.h>
#include "sharedMem.h"
#include <sys/shm.h>
#include <unistd.h>

int qid, sid;
sM *segment;
//SIGNAL HANDLER
void sig_hand(int signo){
    if (signo == SIGHUP){

        exit(0);
    }else if (signo == SIGQUIT){

        exit(0);
    }else if (signo == SIGINT){

        exit(0);
    }
}


int main(int argv, char *argc[]){
		void sig_hand();
	if (signal(SIGINT, sig_hand) == SIG_ERR){
			printf("\ncan't catch SIGINT\n");
	}else if (signal(SIGHUP, sig_hand) == SIG_ERR){
			printf("\ncan't catch SIGHUP\n");
	}else if (signal(SIGQUIT, sig_hand) == SIG_ERR){
			printf("\ncan't catch SIGQUIT\n");
	}

	if(argv>1){//-k
		if(strcmp(argc[1],"-k") == 0){
				kill(segment->manPID, SIGINT);
			}
		}

	if ((sid=shmget(SMKey, sizeof(sM),IPC_CREAT |0660))== -1){
		perror("shmget");
		exit(1);
		}
			/* map it into our address space*/
	if ((segment=((sM *)shmat(sid,0,0)))== (sM *) -1) {
		perror("shmat");
		exit(2);
		}
			/* create queue if necessary */
	if ((qid=msgget(MessKEY,IPC_CREAT |0660))== -1) {
		perror("msgget");
		exit(1);
		}

	int k = 0;
	int sumCandTested = 0;
	int sumCandNotTested = 0;
	int sumpNumsFound = 0;
	while(k < 20){
		if(segment->summary[k].pid==0){
		} else {
			printf("pid: %d",segment->summary[k].pid);
			printf(" Perfects found: %d",segment->summary[k].pNumsFound);
			printf(" Numbers Tested: %d",segment->summary[k].candTested);
			printf(" Numbers not tested %d\n",segment->summary[k].candNotTested);
			sumpNumsFound += segment->summary[k].pNumsFound;
			sumCandNotTested += segment->summary[k].candNotTested;
			sumCandTested += segment->summary[k].candTested;
		}
	k++;
	}
	printf("Total perfect numbers found %d\n", (segment->sumInfo[0] + sumpNumsFound));
	printf("Total Numbers Tested %d\n", (segment->sumInfo[1] + sumCandTested));
	printf("Total Numbers Not Tested %d\n", (segment->sumInfo[2] + sumCandNotTested));
return 0;
}
