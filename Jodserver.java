import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.lang.InterruptedException;
//import java.text.DateFormat;
//import java.text.SimpleDateFormat;
//import java.util.Calendar;
import java.io.PrintWriter;
import java.io.BufferedReader;
import java.io.InputStreamReader;

public class Jodserver { //start Jodserver
    static int newThread;
    static int userID = 0;
    ServerSocket serverPort;
    ServerSocket mainframePort;
    Socket gameAddress;
    static PrintWriter outToGame = null;
    static BufferedReader inFromGame = null;

    public Jodserver(int portNumber) throws IOException { //start Jodserver constructor
        mainframePort = new ServerSocket(6790);//hardcoded port for the mainframe.
        System.out.println("Waiting for python server to start...");
        //The accept() method hangs until an incoming connection is found
        gameAddress = mainframePort.accept();

        outToGame = new PrintWriter(gameAddress.getOutputStream(), true);
        inFromGame = new BufferedReader(new InputStreamReader(gameAddress.getInputStream()));
        //javaToGameSpeak jtk = new javaToGameSpeak();

        System.out.println("Creating server.");
        serverPort = new ServerSocket(portNumber);
        newThread = 1;

        while (newThread != 2) {//change later on to make true possible
			//needs to sleep to check the below if statement. Why? no idea...
			try{Thread.sleep(1);}catch(Exception e){e.printStackTrace();}
			System.out.println(newThread);
            if (newThread == 1) {
                new Thread(new servThread(serverPort)).start();
                newThread = 0;
            }
            try{}catch(Exception e){e.printStackTrace();} //makes stuff work, don't ask why. UPDATE:might be unneccesary.
        } //end while

        serverPort.close();
        System.out.println("Server shut down.");
    } //end Jodserver constructor


    public static synchronized String javaToGameSpeak(String input, String name) throws IOException {
        Jodserver.outToGame.println(name);
        Jodserver.outToGame.println(input);
        return Jodserver.inFromGame.readLine();
    }

    public static void main(String[] args) throws IOException {
        // Create a new server listening on port number 6789
        new Jodserver(6789);
    }
} //end of class Jodserver

class servThread extends Thread {
    ServerSocket threadPort;

    public servThread(ServerSocket sock) {
        threadPort = sock;
    }

    public void run() {
        try {
            Socket address;
            System.out.println("Waiting for an incoming connection.");
            //The accept() method hangs until an incoming connection is found
            address = threadPort.accept();

            Jodserver.newThread = 1;
            PrintWriter outToClient = null;
            BufferedReader inFromClient = null;
            String inputString, outputString;

            outToClient = new PrintWriter(address.getOutputStream(), true);
            inFromClient = new BufferedReader(new InputStreamReader(address.getInputStream()));
            String user = Integer.toString(Jodserver.userID);
            Jodserver.userID++;
            int loop = 1;
            while (loop == 1) {
                Thread.sleep(100); //a small cooldown timer to prevent client from spamming too much.
                inputString = inFromClient.readLine();
                System.out.print(user + ": ");
                
                if (inputString == "I quit" || inputString == null) {
                    System.out.println("quitting player...");
                    outputString = Jodserver.javaToGameSpeak(inputString, user);
                    System.out.println("Player is out.");
                    loop = 0;
                }
                else {
                    System.out.println("Received and forwarding \"" + inputString + "\" from player " + user);
                    outputString = Jodserver.javaToGameSpeak(inputString, user);
                    System.out.println("sending message back");
                    outToClient.println(outputString);
                }
            }

            //Closing connections.
            outToClient.close();
            inFromClient.close();
	    address.close();
            System.out.println("Ending thread");
        }
        catch(Exception e) {
            e.printStackTrace();
        }
    }
}//end of class servThread
