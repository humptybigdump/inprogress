package edu.kit.aifb.proksy.flushVergleich;

import java.io.*;

/**
 * Mit dieser Klasse kann die Autoflush Funktion des Printwriters mit der
 * regulären flush() Methode verglichen werden.
 * 
 * @author ProkSy-Team
 * @version 1.1
 */
public class FlushVergleich {

	/**
	 * main-Methode der Klasse Aufgabenteil b) ist auskommentiert. Um die Lösung für
	 * b) zu überprüfen, muss die Lösung mit dem bufferedReader von a)
	 * auskommentiert werden und die Lösung für b) aktiviert.
	 * 
	 * @param args
	 */
	public static void main(String[] args) {
		BufferedReader ein = null;
		BufferedWriter aus = null;
		// PrintWriter aus = null;

		try {
			ein = new BufferedReader(new InputStreamReader(System.in));
			aus = new BufferedWriter(new OutputStreamWriter(System.out));
			// aus = new PrintWriter(new OutputStreamWriter(System.out), true);
			String zeile = ein.readLine();
			int i = 1;
			while (!zeile.equalsIgnoreCase("stopp")) {
				zeile = "Zeile " + i + ": " + zeile;
				aus.write(zeile + "\n");
				aus.flush();
				// aus.println(zeile);
				zeile = ein.readLine();
				i++;
			}
		} catch (IOException ioe) {
		} catch (Exception e) {
		} finally {
			try {
				if (ein != null)
					ein.close();
				if (aus != null)
					aus.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}
}
