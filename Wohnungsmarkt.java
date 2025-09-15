package edu.kit.aifb.proksy.mietenKaufenWohnen;

import java.rmi.*;

/**
 * Interface mit Methoden, die vom Remote Object implementiert werden.
 * 
 * @author ProkSy-Team
 * @version 1.0
 */
public interface Wohnungsmarkt extends Remote {

	public String getWohnung() throws RemoteException;

}
