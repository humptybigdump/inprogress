package edu.kit.aifb.proksy.EchoMultiServer;

import java.io.*;
import java.net.*;

/**
 * 
 * @version 1.0
 * @author ProkSy-Team
 */
public class EchoServer {
	static final int PORT = 7; // wird standardmäßig für EchoServer verwendet
	static final String SERVER_STARTED = "EchoServer gestartet";
	static final String SERVER_STOPPED = "EchoServer gestoppt";
	static public boolean isInterrupted;

	public static void main(String[] args) {
		ServerSocket serverSocket = null;
		Socket s = null;

		try {
			serverSocket = new ServerSocket(PORT);
			System.out.println(SERVER_STARTED);
			isInterrupted = false;
			while (!isInterrupted) {
				s = serverSocket.accept();
				new EchoProtokoll(s).start();
			}
			System.out.println(SERVER_STOPPED);
			serverSocket.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}
