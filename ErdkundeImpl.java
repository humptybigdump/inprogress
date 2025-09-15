package edu.kit.aifb.proksy.ErdkundeRMI.server.controller;

import java.rmi.*;
import java.rmi.server.UnicastRemoteObject;

import edu.kit.aifb.proksy.ErdkundeRMI.server.model.Topographie;

/**
 * @version 1.0
 * @author ProkSy-Team
 *
 */
public class ErdkundeImpl extends UnicastRemoteObject implements Erdkunde {

	private Topographie t;

	public ErdkundeImpl() throws RemoteException {
		super();
	}

	public void setTopographie(Topographie t) {
		this.t = t;
	}

	@Override
	public String topographie(String eingabe, boolean bundesland) throws RemoteException {
		String ausgabe = null;
		if (bundesland == true) {
			ausgabe = t.getStadt(eingabe);
			return ausgabe;
		} else {
			ausgabe = t.getLand(eingabe);
			return ausgabe;
		}
	}

}
