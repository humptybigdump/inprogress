package edu.kit.aifb.proksy.EchoMultiServer;

import java.io.*;
import java.net.*;

/**
 * 
 * @version 1.0
 * @author ProkSy-Team
 */
public class EchoClient {
	static final String HOST = "localhost";
	static final int PORT = 7; // wird standardmäßig für EchoServer verwendet
	static final String CLIENT_PROMPT = "EchoClient> ";
	static final String SERVER_PROMPT = "EchoServer> ";
	static final String CLIENT_DISCONNECTED = "EchoClient disconnected";
	static final String EXIT = "exit";

	public static void main(String[] args) {
		Socket socket = null;
		ObjectOutputStream zumServer = null;
		ObjectInputStream vomServer = null;
		BufferedReader in = null;
		String request = null;
		String response = null;
		boolean isRunning;

		try {
			socket = new Socket(HOST, PORT);
			zumServer = new ObjectOutputStream(socket.getOutputStream());
			vomServer = new ObjectInputStream(socket.getInputStream());
		} catch (UnknownHostException e) {
			System.err.println("Don't know host: " + HOST);
			System.exit(1);
		} catch (IOException e) {
			System.err.println("Couldn't get I/O for connection  to: " + HOST);
			System.exit(1);
		}

		try {
			in = new BufferedReader(new InputStreamReader(System.in));
			isRunning = true;
			System.out.print(CLIENT_PROMPT);
			request = in.readLine();
			while (isRunning) {
				zumServer.writeObject(request);
				if (!request.equals(EXIT)) {
					response = (String) vomServer.readObject();
					System.out.println(SERVER_PROMPT + response);
					System.out.print(CLIENT_PROMPT);
					request = in.readLine();
				} else {
					response = CLIENT_DISCONNECTED;
					System.out.println(SERVER_PROMPT + response);
					isRunning = false;
				}
			}
			zumServer.close();
			vomServer.close();
			in.close();
			socket.close();
		} catch (ClassNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}
