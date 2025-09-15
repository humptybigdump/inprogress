package edu.kit.aifb.proksy.rMIEcho.RMIProgrammierung;

import java.rmi.*;
import java.rmi.registry.Registry;
import java.io.*;
/**
 *
 * @author ProkSy-Team
 * @version 1.0
 */
public class EchoClient
{
    public static final String EXIT = "exit";
    public static final String PROMPT_CLIENT = "EchoClient> ";
    public static final String PROMPT_SERVER = "EchoServer> ";
    public static final int PORT = Registry.REGISTRY_PORT;
    
    public static void main (String[] args)
    {
        EchoService es = null;
        String request = null;
        String response = null;
        boolean isRunning = false;
        BufferedReader in = null;
        
        try
        {
            es = (EchoService) Naming.lookup("rmi://localhost:" + PORT + "/EchoObject");
            isRunning = true;
            in = new BufferedReader(new InputStreamReader(System.in));
            System.out.print(PROMPT_CLIENT);
            request = in.readLine();
            while (isRunning)
            {
                if (request != null && !request.equals(EXIT))
                {
                    es.request(request);
                    response = es.getResponse();
                    System.out.println("EchoServer> " + response);
                    System.out.print(PROMPT_CLIENT);
                    request = in.readLine();
                }
                else
                {
                    isRunning = false;
                }
            }
        }
        catch (Exception e)
        {
            e.printStackTrace();
        } 
    }
}
