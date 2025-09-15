package edu.kit.aifb.proksy.taschenrechner.main;

import edu.kit.aifb.proksy.taschenrechner.view.TaschenrechnerView;
import javax.swing.*;

/**
 * Diese Klasse enthält die Main-Methode für das Taschenrechner-Projekt
 * 
 * @version 1.0
 * @author ProkSy-Team
 *
 */
public class TaschenrechnerMain {

	/**
	 * Main-Methode des Projektes
	 * 
	 * @param args Kommandozeilenparameter
	 */
	public static void main(String[] args) {
		TaschenrechnerView myFrame = new TaschenrechnerView();
		myFrame.setTitle("Rechner");
		myFrame.setSize(260, 250);
		myFrame.setResizable(false);
		myFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		myFrame.setVisible(true);
	}

}
