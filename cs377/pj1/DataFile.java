
import java.io.*;


public class DataFile
{
   RandomAccessFile f;

   public DataFile(String fname)
   {
      try
      {
         f = new RandomAccessFile( fname, "r" );
      }
      catch ( FileNotFoundException e )
      {
         System.out.println("File not found error: " + e.getMessage() );
         System.exit(1);
      }
   }

   public void rewind()
   {
      try
      {
         f.seek(0);
      }
      catch ( IOException e )
      {
         System.out.println("Rewind failed: " + e.getMessage() );
         System.exit(1);
      }
   }

   /* ============================================================
      Handle writing
      ============================================================ */
   public void WriteInt(int x) throws IOException
   {
      f.writeInt( x );
   }

   public void WriteDouble(double x) throws IOException
   {
      f.writeDouble( x );
   }


   public void WriteString(String x, int len) throws IOException
   {
      if ( x.length() <= len )
      {
         f.writeBytes( x );

         for ( int i = x.length(); i < len; i++ )
            f.writeByte( '\0' );
      }
      else
      {
         f.writeBytes( x.substring(0, len) );
      }
   }



   /* ============================================================
      Handle reading
      ============================================================ */
   public int ReadInt() throws IOException
   {
      return f.readInt( );
   }


   public double ReadDouble() throws IOException
   {
      return f.readDouble( );
   }


   public String ReadString(int maxLen) throws IOException
   {
      StringBuffer s = new StringBuffer(maxLen);
      byte x;
      int  k;

      k = 0;

      for (int i = 0; i < maxLen; i++ )
      {
         x = f.readByte();
//       System.out.println( "x = " + (char) x );
         s.append( (char) x );

         if ( x != '\0' )
            k++;
      }

      return s.substring(0, k);
   }

}

