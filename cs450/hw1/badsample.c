/* Short code  sample to 

	define a new type with typedef
	illustrate struct's
	illustrate dynamic allocation with malloc
	illustrate stdio style input
*/
	
#include <stdlib.h>
#include <stdio.h>


typedef struct _seg {  /* definition of new type "seg" */
    int  bits[256];
    struct _seg  *next,*prev;        
      }seg  ;

#define BITSPERSEG  (8*256*sizeof(int))

void clearbits(seg *, int);

void main(int argc, char *argv[]) {

	seg *head,*pt;
	int	 i;
	int howmany;


	if (argc == 2) sscanf(argv[1],"%d",&howmany);
		else scanf("%d",&howmany);
	howmany = (howmany +BITSPERSEG -1)/BITSPERSEG;



	head= (  seg * ) malloc(sizeof(seg));
	pt=head;
	for (i=1;i<howmany;i++) { //Just Forward Links for Now
		pt->next = (  seg *) malloc(sizeof (seg)); 
		pt=pt->next;
		}

	printf("Done allocating %d nodes\n",i);

	/* clear all bits */

	clearbits(head, howmany);
}	

void	clearbits(seg *ptr , int num) { /* clear all bits at once */

	int i,j;

	for (i=0; i<= num; i++) {

		for (j=0; j<= 255; j++) {
			ptr->bits[j]=0;
			}
		ptr=ptr->next;
	}
}
