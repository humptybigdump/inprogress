package edu.kit.aifb.proksy.rMIEcho.RMIProgrammierung;

import java.rmi.*;
/**
 *
 * @author ProkSy-Team
 * @version 1.0
 */
public interface EchoService extends Remote
{
    public String getResponse () throws RemoteException;
    
    public void request (String request) throws RemoteException;
}
