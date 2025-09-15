package edu.kit.aifb.proksy.EchoServerMitProtokoll;

import java.io.*;
import java.net.*;

/**
 * 
 * @version 1.0
 * @author ProkSy-Team
 */
public class EchoProtokoll {
	public final String EXIT = "exit";
	@SuppressWarnings("unused")
	private Socket s = null;
	private PrintWriter zumClient = null;
	private BufferedReader vomClient = null;
	private boolean isRunning;

	public EchoProtokoll(Socket s) {
		try {
			this.s = s;
			zumClient = new PrintWriter(s.getOutputStream(), true);
			vomClient = new BufferedReader(new InputStreamReader(s.getInputStream()));
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	public void transact() {
		String echo = null;
		System.out.println("Protokoll gestartet");
		isRunning = true;
		while (isRunning) {
			try {
				echo = vomClient.readLine();
				zumClient.println(echo);
			} catch (IOException e) {
				isRunning = false;
			}
			if (echo.equals(EXIT)) {
				isRunning = false;
			}
		}
		System.out.println("Protokoll beendet");
	}
}
