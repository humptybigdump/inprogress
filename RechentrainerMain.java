package edu.kit.aifb.proksy.rechenspiel.main;

import edu.kit.aifb.proksy.rechenspiel.view.RechentrainerFrame;
import edu.kit.aifb.proksy.rechenspiel.controller.*;

/**
 * Diese Klasse enthält die main-Methode des Rechentrainers
 * 
 * @version 1.0
 * @author ProkSy-Team
 *
 */
public class RechentrainerMain {

	private static RechentrainerController controller;
	private static RechentrainerFrame view;

	/**
	 * main-Methode des Rechentrainers
	 * 
	 * @param args Kommandozeilenparameter
	 */
	public static void main(String[] args) {
		controller = new RechentrainerController();
		view = new RechentrainerFrame("Rechner");

		view.setController(controller);
		controller.setView(view);

		view.setVisible(true);
		view.setSize(600, 350);
		view.setDefaultCloseOperation(RechentrainerFrame.DO_NOTHING_ON_CLOSE);
	}
}