package edu.kit.aifb.proksy.EchoServerOhneProtokoll;

import java.io.*;
import java.net.*;

/**
 * 
 * @version 1.0
 * @author ProkSy-Team
 */
public class EchoServer {
	static final int PORT = 7;
	static final String SERVER_STARTED = "EchoServer gestartet";
	static final String SERVER_STOPPED = "EchoServer gestoppt";
	static public boolean isInterrupted;
	static public final String EXIT = "exit";

	/**
	 * main-Methode
	 * 
	 * @param args Kommandozeilenparameter
	 */
	public static void main(String[] args) {
		ServerSocket serverSocket = null;
		Socket s = null;

		try {
			serverSocket = new ServerSocket(PORT);
			System.out.println(SERVER_STARTED);
			isInterrupted = false;
			while (!isInterrupted) {
				s = serverSocket.accept();
				transact(s);
			}
			System.out.println(SERVER_STOPPED);
			serverSocket.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	/**
	 * transact-Methode
	 * 
	 * @param s übergebenes Socket
	 */
	public static void transact(Socket s) {
		PrintWriter zumClient = null;
		BufferedReader vomClient = null;
		boolean isRunning;
		String echo = null;

		System.out.println("Protokoll gestartet");

		try {
			zumClient = new PrintWriter(s.getOutputStream(), true);
			vomClient = new BufferedReader(new InputStreamReader(s.getInputStream()));
		} catch (IOException e) {
			e.printStackTrace();
		}

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
