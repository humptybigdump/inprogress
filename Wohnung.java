package edu.kit.aifb.proksy.mietenKaufenWohnen;

import java.rmi.*;
import java.rmi.server.UnicastRemoteObject;

/**
 * Klasse, die das Remote-Objekt darstellt.
 * 
 * @author ProkSy-Team
 * @version 1.0
 */
public class Wohnung extends UnicastRemoteObject implements Wohnungsmarkt {

	private String name;
	private double zimmer;
	private double preis;

	/**
	 * Kostruktor der Klasse; erstellt ein neues Objekt mit den übergebenen
	 * Eigenschaften.
	 * 
	 * @param name
	 * @param zimmer
	 * @param preis
	 * @throws RemoteException
	 */
	public Wohnung(String name, double zimmer, double preis) throws RemoteException {
		super();
		this.name = name;
		this.zimmer = zimmer;
		this.preis = preis;
	}

	/**
	 * Überschriebene Methode des Interfaces. Gibt einen vorgefertigten String mit
	 * den Eigenschaften des angefragten Objekts zurück.
	 * 
	 * @return String mit Eigenschaften des Objekts
	 */
	@Override
	public String getWohnung() throws RemoteException {
		// TODO Auto-generated method stub
		return "Wohnungsname: " + name + "\nZimmeranzahl: " + zimmer + "\nMietpreis: " + preis;
	}

}
