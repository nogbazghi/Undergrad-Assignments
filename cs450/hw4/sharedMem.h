/*THIS CODE IS MY OWN WORK, IT WAS WRITTEN WITHOUT CONSULTING A TUTOR OR CODE WRITTEN BY OTHER STUDENTS - NAHOM OGBAZGHI*/
#include <string.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/shm.h>
#include <unistd.h>
#define SMKey (key_t)429464
#define MessKEY (key_t)42946	/*key for message queue */
typedef struct process {
	pid_t pid;
	int pNumsFound;
	int candTested;
	int candNotTested;
}process;

typedef struct sharedMem{
	int bits[1048576];
	int perfectNums[20];
	process summary[20];
	int sumInfo[3];
	pid_t manPID;
	int totalProcRun;
}sM;

//REQ
typedef struct req {
	int t;
	pid_t pid;
	int perfNum;
} req;


