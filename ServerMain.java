package edu.kit.aifb.proksy.Erdkunde.server.main;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;

import edu.kit.aifb.proksy.Erdkunde.server.controller.ServerProtokoll;
import edu.kit.aifb.proksy.Erdkunde.server.model.*;

/**
 * Diese Klasse enthält die main-Methode des Servers.
 * 
 * @author ProkSy-Team
 * @version 1.0
 */
public class ServerMain {
	private static final int PORT = 7777;
	private static final String SERVER_STARTED = "Erdkunde-Server gestartet";
	private static final String SERVER_STOPPED = "Erdkunde-Server gestoppt";
	private static boolean isInterrupted;
	private static Socket s;
	private static ServerProtokoll protokoll;
	private static Topographie topo;

	/**
	 * main-Methode des Servers
	 * 
	 * @param args Kommandozeilenparameter
	 */
	public static void main(String[] args) {
		ServerSocket serverSocket = null;

		try {
			// Serversocket erzeugen
			serverSocket = new ServerSocket(PORT);
			System.out.println(SERVER_STARTED);

			isInterrupted = false;
			while (!isInterrupted) {
				// Clients akzeptieren
				s = serverSocket.accept();
				protokoll = new ServerProtokoll(s);
				topo = new Topographie();
				protokoll.setTopographie(topo);
				protokoll.transact();
			}
			System.out.println(SERVER_STOPPED);

			// Socket schließen
			serverSocket.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}
