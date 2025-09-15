package edu.kit.aifb.proksy.ErdkundeRMI.server.controller;

import java.rmi.*;

/**
 * @version 1.0
 * @author ProkSy-Team
 *
 */
public interface Erdkunde extends Remote {

	public String topographie(String eingabe, boolean bundesland) throws RemoteException;
}
