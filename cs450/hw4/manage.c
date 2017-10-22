/*THIS CODE IS MY OWN WORK, IT WAS WRITTEN WITHOUT CONSULTING A TUTOR OR CODE WRITTEN BY OTHER STUDENTS - NAHOM OGBAZGHI*/
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <stdio.h>
#include <stdlib.h>
#include "sharedMem.h"
#include  <sys/shm.h>
#include <unistd.h>
#include <signal.h>

sM *segment;
int sid,qid;

//SIGNAL HANDLER
void sig_hand(int signo){
    if (signo == SIGHUP || signo == SIGQUIT || signo == SIGINT){
        int k= 0;
		while(k< 20){
			if(segment->summary[k].pid==0){
			}else {
				kill(segment->summary[k].pid, SIGINT);
			}
		k++;
		}
		sleep(5);
		/* Unmap and deallocate the shared segment*/ 

		if (shmdt((char  *) segment) == -1) {
			perror("shmdt");
			_exit(3);
		}
		if (shmctl(sid,IPC_RMID,0) == -1) {
			perror("shmctl");
			_exit(3);
		}
		if (msgctl(qid, IPC_RMID, 0) == -1) {
        perror("msgctl");
        exit(1);
    }
        _exit(0);
    }
} 

int main(int argv, char *argc[]){
	void sig_hand();
	if (signal(SIGINT, sig_hand) == SIG_ERR){
		printf("\ncan't catch SIGINT\n");
	}
	else if (signal(SIGHUP, sig_hand) == SIG_ERR){
		printf("\ncan't catch SIGHUP\n");
	}
	else if (signal(SIGQUIT, sig_hand) == SIG_ERR){
		printf("\ncan't catch SIGQUIT\n");
	}
	
	//SM
	if ((sid=shmget(SMKey, sizeof(sM),IPC_CREAT |0660))== -1) {
		perror("shmget");
		exit(1);
		}
			/* map it into our address space*/
	if ((segment=((sM *)shmat(sid,0,0)))== (sM *) -1) {
		perror("shmat");
		exit(2);
		}
	//MQ		/* create queue if necessary */
	if ((qid=msgget(MessKEY,IPC_CREAT |0660)) <0) {
		perror("msgget");
		exit(1);
		}
		
	//PID for REPORT
	segment->manPID = getpid();
	while(1){
		req test;
		if(msgrcv(qid, &test, 12, 0, 0) == -1){
			perror("test");
			exit(1);
		}
		if(test.t ==1 ){
			int k= 0;
			while(k< 20){//PID
				if(segment->summary[k].pid==0){
					process new;
					new.pid = test.pid;
					segment->summary[k] = new;
					break;
				} k++;
			}
		} else if(test.t ==2 ){//PERF NUM
			int j= 0;
			while(j< 20){
				if(segment->perfectNums[j]==test.perfNum){
					break;
				} else if(segment->perfectNums[j]==0){
					segment->perfectNums[j]=test.perfNum;
					break;
				}
				j++;
			}	
		}
	}	
return 0;
}
