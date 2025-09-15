package edu.kit.aifb.proksy.rMIEcho.RMIProgrammierung;

import java.rmi.*;
import java.rmi.server.UnicastRemoteObject;
/**
 *
 * @author ProkSy-Team
 * @version 1.0
 * 
 */
@SuppressWarnings("serial")
public class EchoObject extends UnicastRemoteObject
                        implements EchoService
{
    private String response;
    
    public EchoObject () throws RemoteException
    {
        super();
        response = "";
    }
    
    public String getResponse () throws RemoteException
    {
        String result = response;
        System.out.println("Aufruf von getResponse()");
        return result;
    }
    
    public void request (String request) throws RemoteException
    {
        response = request;
    }
}
