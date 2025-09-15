package edu.kit.aifb.proksy.EchoMultiServer;

import java.io.*;
import java.net.*;

/**
 * 
 * @version 1.0
 * @author ProkSy-Team
 */
public class EchoProtokoll extends Thread {
	public final String EXIT = "exit";
	private Socket s = null;
	private ObjectOutputStream zumClient = null;
	private ObjectInputStream vomClient = null;
	private boolean isRunning;

	public EchoProtokoll(Socket s) {
		try {
			this.s = s;
			zumClient = new ObjectOutputStream(s.getOutputStream());
			vomClient = new ObjectInputStream(s.getInputStream());
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	public void run() {
		String echo = null;
		System.out.println("Protokoll gestartet");
		isRunning = true;
		while (isRunning) {
			try {
				echo = (String) vomClient.readObject();
				zumClient.writeObject(echo);
			} catch (Exception e) {
				isRunning = false;
			}
			if (echo.equals(EXIT)) {
				isRunning = false;
			}
		}
		try {
			vomClient.close();
			zumClient.close();
			s.close();
		} catch (Exception e) {
			e.printStackTrace();
		}
		System.out.println("Protokoll beendet");
	}
}
