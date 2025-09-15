package edu.kit.aifb.proksy.ErdkundeRMI.server.main;

import java.rmi.*;
import java.rmi.registry.*;

import edu.kit.aifb.proksy.ErdkundeRMI.server.controller.*;
import edu.kit.aifb.proksy.ErdkundeRMI.server.model.*;

/**
 * Diese Klasse enthält die main-Methode des Servers.
 * 
 * @author ProkSy-Team
 * @version 1.0
 */
public class ServerMain {

	/**
	 * main-Methode des Servers
	 * 
	 * @param args Kommandozeilenparameter
	 */
	public static void main(String[] args) {
		ErdkundeImpl e;
		Topographie t;

		try {
			e = new ErdkundeImpl();
			t = new Topographie();

			e.setTopographie(t);

			Registry registry = LocateRegistry.createRegistry(1705);

			registry.rebind("rmi://localhost:1705/Erdkunde", e);
		} catch (RemoteException re) {
			re.printStackTrace();
		}

		System.out.println("Der Server ist aktiv");
	}
}
