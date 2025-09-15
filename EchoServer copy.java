package edu.kit.aifb.proksy.rMIEcho.RMIProgrammierung;

import java.rmi.*;
import java.rmi.registry.*;
/**
 *
 * @author ProkSy-Team
 * @version 1.0
 * 
 */
public class EchoServer
{
	public static final int PORT = Registry.REGISTRY_PORT;
	
    public static void main (String[] args)
    {
        EchoObject eo = null;
        
        try
        {
            // Objekt erzeugen
            eo = new EchoObject();

            // rmiregistry starten (sofern noch nicht erfolgt)
            LocateRegistry.createRegistry(PORT);
            
            // Objekt bei der Registry anmelden
            Naming.rebind("rmi://localhost:" + PORT + "/EchoObject", eo);
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }
        System.out.println("Der Server ist aktiv");
    }
}
