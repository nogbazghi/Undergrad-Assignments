
import java.io.*;

class DataDescription {
	String fieldName;
	String fieldType;
	int fieldSize;
}

public class pj1 {
	static int MAXNFIELDS = 10; // Max. # fields in 1 record

	static int n_fields; // Actual number of fields

	/*
	 * ------------------------------------------------------------ (1)
	 * Variables used to store the DESCRIPTION of the data
	 * ------------------------------------------------------------
	 */
	static DataDescription[] dataDes = new DataDescription[MAXNFIELDS];

	// This is a CONSTRUCTOR method for static variables
	static {
		// Need to create objects for the dataDes[]
		for (int i = 0; i < MAXNFIELDS; i++) {
			dataDes[i] = new DataDescription();
		}
	}

	/*
	 * ------------------------------------------------------- (2) Variables
	 * used to store the ACTUAL data
	 * -------------------------------------------------------
	 */
	static String[] c_buf = new String[MAXNFIELDS]; // Used to store String
													// fields
	static int[] i_buf = new int[MAXNFIELDS]; // Used to store int fields

	// TODO: add variable(s) to support double data
	static double[] d_buf = new double[MAXNFIELDS]; // Used to store double
													// fields

	public static void main(String[] args) throws IOException
   {

      /* ===========================================================
	 We must first find out the STRUCTURE of the data file
	 This information is stored in the data DESCRIPTION file
	 =========================================================== */

      DataFile descrFile = new DataFile("db-description");
			 // 1. Open the data description file

      /* -------------------------------------------------------
	 Read in the data description and store them in the
	 DataDes[] array (define in (1))
         ------------------------------------------------------- */

      n_fields = 0;                 // Count the actual number of fields in data
      while ( true )
      {
         try
         {
            dataDes[n_fields].fieldName = descrFile.ReadString(24);
            dataDes[n_fields].fieldType = descrFile.ReadString(4);
            dataDes[n_fields].fieldSize = descrFile.ReadInt();

            System.out.println("Field: " + dataDes[n_fields].fieldName
                + ", type: " + dataDes[n_fields].fieldType
                + ", size: " + dataDes[n_fields].fieldSize);

	    n_fields++;
         }
         catch ( IOException e )
         {
            System.out.println("\nFinish reading data description file....\n");
            break;   // Read error: no more data !!!
         }
      }


      DataFile dataFile =  new DataFile("db-data");   // First open data file
      System.out.println( "The data file contains these records:\n");

      // TODO:  Write a loop to print out the records
      //        You can use the PrintRecord() method below
      //        but you must add support for double in that method
      // 
      // The correct output is:
      //
      //               123 Disk Drive 109.99 14
      //               444 CPU 899.99 5
      //               333 Printer 219.97 2

      while(true){
 		 try
 	       {
      for ( int i = 0; i < n_fields; i++ )
      {
    	  //System.out.print(dataFile[i]);
         if ( dataDes[i].fieldType.equals("I") )
         {
        	 
            /* --------------------------------------------------------
               Field i is an integer, use i_buf[i] to store the value
               -------------------------------------------------------- */
            System.out.print( dataFile.ReadInt() + " ");
         }
		 else if ( dataDes[i].fieldType.equals("F") )
         {
            /* --------------------------------------------------------
               Field i is an integer, use i_buf[i] to store the value
               -------------------------------------------------------- */
            System.out.print( dataFile.ReadDouble() + " ");
         }
         else
         {
            /* --------------------------------------------------------
               Field i is an String, use c_buf[i] to store the value
               -------------------------------------------------------- */
            System.out.print( dataFile.ReadString(dataDes[i].fieldSize) + " ");
         }

      }System.out.println( );    // Print newline to separate records
 	      } 
		 catch ( IOException e )
	       {
			 System.out.println("Done");
		  break;
	       }
      }


      System.out.print("\nSumming values in the field " + args[0] + "\n");

      dataFile.rewind();      // Rewind data file
      
      
      double sum = 0;         // Variable used to compute the sum


      // TODO:  Write a loop to sum the values in the specified fieldName 
      //        (which is given in args[0])
      //
      // The sum is stored in the double value "sum"
      // Even if the field that is summed is integer typed, you will still 
      // use the double variable "sum"
      
    boolean exist = false;
    boolean numType = true;
      while(numType){
    	  
    	  try{
		  for ( int i = 0; i < n_fields; i++ ){

	    	  if ( dataDes[i].fieldType.equals("I") ){
	             /* --------------------------------------------------------
	                Field i is an integer, use i_buf[i] to store the value
	                -------------------------------------------------------- */
	             i_buf[i] = dataFile.ReadInt();
	             if(dataDes[i].fieldName.equals(args[0])){
	            	 exist = true;
	            	 sum += i_buf[i];
	            	 System.out.println("Adding: "+i_buf[i]);
	             }
	          }
	 		  else if ( dataDes[i].fieldType.equals("F") ){
	             /* --------------------------------------------------------
	                Field i is an integer, use i_buf[i] to store the value
	                -------------------------------------------------------- */
	             d_buf[i]=dataFile.ReadDouble();
	             if(dataDes[i].fieldName.equals(args[0])){
	            	 exist = true;
	            	 sum += d_buf[i];
	            	 System.out.println("Adding: "+d_buf[i]);
	             }
	          }
	          else{
	             /* --------------------------------------------------------
	                Field i is an String, use c_buf[i] to store the value
	                -------------------------------------------------------- */
	             c_buf[i] = dataFile.ReadString(dataDes[i].fieldSize);
	             if(dataDes[i].fieldName.equals(args[0])){
	            	 exist = true;
	            	 numType = false;
	            	 System.out.print("--- Error: Non-numerical data type.");
	            	 break;
	             } 
	          }
		  }
    	  } catch(EOFException e){
    		  	if (exist == false){
    		  		System.out.print("--- Error: Non-existing field name.");
    		  	} else {
    		  		System.out.println("\nDone...\n");
    		  		System.out.println("Sum of the " + args[0] + " fields = " + sum);  
    		  	}	
    		  	break;
    	  }
      }
   }
}
