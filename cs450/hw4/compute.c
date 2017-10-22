/*THIS CODE IS MY OWN WORK, IT WAS WRITTEN WITHOUT CONSULTING A TUTOR OR CODE WRITTEN BY OTHER STUDENTS - NAHOM OGBAZGHI*/
#include <stdio.h>
#include <math.h>
#include <sys/types.h>
#include <errno.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>
#include "sharedMem.h"
#include <sys/shm.h>

//MESSAGE QUEUE
int qid;	/* message queue id */
sM *segmentL;
process *sumData;


//TEST AND SET BIT

int whichInt (int N){
	//N;//offset for starting at 1
	int withinInt = N/32;//finds N in relation of 0 - N/32
	return withinInt;
}

int whichBit (int N){
	//N;//offset for starting at 1
	int withinBit = N%32;//finds N in relation of 0 - 31
	return withinBit;
}

void mark(int N, int *bits){
	bits[whichInt(N)] |= 1 << (whichBit(N));
}

int TestBit(int N, int *bits){
	return (bits[whichInt(N)] & (1 << whichBit(N) ));
}

//Generate Perfect Numbers
void perfNum (int start, sM *segment, process *sumData){
	int current, i, sum, stop, last;
	current = start;
	last = ((int)(pow (2.0, 25.0)));
	stop = 0;
	while (current <= last){
		if (stop == 1){
			//terminate
			printf("%d\n", current);
			if (current == start){ printf("Complete"); exit(0);}
		}
		sum= 1;
		if (!TestBit(current, segment->bits)){
			for (i=2;i<current;i++){
				if (!(current%i)) sum+=i; //mark every multiple of the perfectNumber
			}
			if (sum==current && sum != 1){
				printf("Perfect Number: %d, Index: %d, Bit: %d\n",sum, whichInt(current),whichBit(current));
				sumData->pNumsFound+=1;//increment if a perfect number is found
				printf("why?");
				//Send REquest to Send Data
				req r;
				r.t = 2;
				r.perfNum = sum;
				msgsnd(qid,&r,12,0);
			}
			sumData->candTested++;
			current++;
		} else{//already checked
			sumData->candNotTested++;
			current++;
		}
		mark(current, segment->bits); //Mark checked Number
		//printf("current %d, last %d",current, last);
		if(last != current){  continue;} else{
		current = 1; stop = 1; }//if the current value reaches the final number set flag to begin second loop
	}
}


//SIGNAL HANDLER
void sig_hand(int signo){
    if (signo == SIGQUIT||signo == SIGHUP||signo == SIGINT){
        int k= 0;
		while(k< 20){
			if(segmentL->summary[k].pid==getpid()){
				segmentL->sumInfo[0] +=segmentL->summary[k].pNumsFound;
				segmentL->sumInfo[1] +=segmentL->summary[k].candTested;
				segmentL->sumInfo[2] +=segmentL->summary[k].candNotTested;
				segmentL->summary[k].pid = 0;
				segmentL->summary[k].pNumsFound = 0;
				segmentL->summary[k].candTested = 0;
				segmentL->summary[k].candNotTested = 0;
				segmentL->totalProcRun--;
			}k++;
		}
        exit(0);
    }
}

int main(int argv, char *argc[]){
	void sig_hand();
	int start;
	if(argv>1){
		start = atoi(argc[1]);
	} else {
		printf("No input"); exit(0);
	}
	//HANDLES SIG ERRORS
	if (signal(SIGINT, sig_hand) == SIG_ERR){
		    printf("\ncan't catch SIGINT\n");
	}else if (signal(SIGHUP, sig_hand) == SIG_ERR){
		    printf("\ncan't catch SIGHUP\n");
	}else if (signal(SIGQUIT, sig_hand) == SIG_ERR){
		    printf("\ncan't catch SIGQUIT\n");
	}


	int sid;	/* segment id of shared memory segment */
			/* create shared segment if necessary */

	if ((sid=shmget(SMKey, sizeof(sM),IPC_CREAT |0660))== -1) {
		perror("shmget");
		exit(1);
		}
			/* map it into our address space*/
	if ((segmentL=((sM *)shmat(sid,0,0)))== (sM *) -1) {
		perror("shmat");
		exit(2);
		}
			/* create queue if necessary */
	if ((qid=msgget(MessKEY,IPC_CREAT |0660))== -1) {
		perror("msgget");
		exit(1);
		}

	//Send Request for PID ONLY
	req t;
	t.t = (int)1;
	t.pid = getpid();
	msgsnd(qid,&t,12,0);

	sleep(1);
	int k = 0;
	while(k<20){
		if(segmentL->summary[k].pid == getpid()){
			sumData = &(segmentL->summary[k]);
		} k++;
	}
	perfNum(start, segmentL, sumData);
return 0;
}
