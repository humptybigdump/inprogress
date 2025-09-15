package edu.kit.aifb.proksy.meerschweinchen;

import java.io.*;

/**
 * Mit dieser Klasse wird eine Datei eingelesen, alle Vokale durch einen
 * bestimmten Vokal ersetzt und das Ergenbis in eine neue Datei geschrieben.
 * 
 * @author ProkSy-Team
 * @version 1.0
 */
public class VokalWandel {
	/**
	 * Main-Methode
	 * 
	 * @param args Kommandozeilenargumente
	 */
	public static void main(String[] args) {
		String name = null;
		char ersatzVokal;
		File ein, aus;
		BufferedReader einLeser;
		PrintWriter ausSchreiber;

		try {
			name = "Meerschweinchen.txt";
			ersatzVokal = 'e';
			ein = new File(name);
			aus = new File("Geheimsprache.txt");
			einLeser = new BufferedReader(new FileReader(ein));
			ausSchreiber = new PrintWriter(new FileWriter(aus));
		} catch (FileNotFoundException fnfe) {
			System.out.println("Die Datei " + name + " existiert nicht");
			return;
		} catch (Exception e) {
			System.out.println(e);
			return;
		}

		char[] aeiouK = { 'a', 'e', 'i', 'o', 'u' };
		char[] aeiouG = { 'A', 'E', 'I', 'O', 'U' };
		char vK = Character.toLowerCase(ersatzVokal);
		char vG = Character.toUpperCase(ersatzVokal);

		try {
			String zeile = einLeser.readLine();
			while (zeile != null) {
				for (int i = 0; i < 5; i++) {
					zeile = zeile.replace(aeiouK[i], vK);
					zeile = zeile.replace(aeiouG[i], vG);
				}
				ausSchreiber.println(zeile);
				System.out.println(zeile);
				zeile = einLeser.readLine();
			}
		} catch (IOException ioe) {
			System.out.println(ioe);
		} finally {
			try {
				einLeser.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
			ausSchreiber.close();
		}
	}
}
