package edu.kit.aifb.proksy.rechenspiel.controller;

import java.awt.Color;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.WindowEvent;
import java.awt.event.WindowListener;

import javax.swing.JOptionPane;

import edu.kit.aifb.proksy.rechenspiel.view.*;

public class RechentrainerController {

	private RechentrainerFrame view;

	public void setView(RechentrainerFrame view) {
		this.view = view;
	}

	public NeuButtonListener createNeuButtonListener() {
		return new NeuButtonListener();
	}

	public UeberpruefenButtonListener createUeberpruefenButtonListener() {
		return new UeberpruefenButtonListener();
	}

	public BeendenListener createBeendenListener() {
		return new BeendenListener();
	}

	/**
	 * Innere Klasse zur Eregnisbehandlung des neuButton
	 * 
	 * @author ProkSy-Team
	 * @version 1.0
	 * 
	 */
	class NeuButtonListener implements ActionListener {
		@Override
		public void actionPerformed(ActionEvent e) {
			neueRechenaufgabe();
		}
	}

	/**
	 * Innere Klasse zur Eregnisbehandlung des ueberpruefenButton
	 * 
	 * @author ProkSy-Team
	 * @version 1.0
	 * 
	 */
	class UeberpruefenButtonListener implements ActionListener {
		@Override
		public void actionPerformed(ActionEvent e) {
			ueberpruefen();
		}
	}

	/**
	 * Diese Methode erzeugt eine neue Rechenaufgabe und stellt sie dar. Der
	 * Zahlenraum ist abhängig von der gewählten Schwierigkeit
	 * 
	 */
	public void neueRechenaufgabe() {
		int index, ergebnis;

		view.getFeedbackLabel().setText("");

		int multiplikator;

		if (view.getItems()[0].isSelected()) {
			// Zahlenraum bis 10
			multiplikator = 10;
		} else {
			// Zahlenraum bis 100
			multiplikator = 100;
		}

		index = (int) (Math.random() * 2);
		int a = (int) (Math.random() * multiplikator) + 1;
		int b = (int) (Math.random() * multiplikator) + 1;
		ergebnis = 0;

		switch (index) {
		case 0:
			ergebnis = a + b;
			break;
		case 1:
			ergebnis = a - b;
			break;
		}

		view.getLinkerOperandTextField().setText(a + "");
		view.getRechterOperandTextField().setText(b + "");
		view.getErgebnisTextField().setText(ergebnis + "");
	}

	/**
	 * Diese Methode überprüft die Rechenaufgabe und stellt das Feedback dar.
	 * 
	 */
	public void ueberpruefen() {
		boolean auswahlKorrekt = false;
		int a;
		int b;
		int ergebnis;

		a = Integer.parseInt(view.getLinkerOperandTextField().getText());
		b = Integer.parseInt(view.getRechterOperandTextField().getText());
		ergebnis = Integer.parseInt(view.getErgebnisTextField().getText());

		switch (view.getOperatorComboBox().getSelectedIndex()) {
		case 0:
			auswahlKorrekt = (a + b == ergebnis);
			break;
		case 1:
			auswahlKorrekt = (a - b == ergebnis);
			break;
		}

		if (auswahlKorrekt) {
			view.getFeedbackLabel().setText("Richtig");
			view.getFeedbackLabel().setForeground(Color.GREEN);
		} else {
			view.getFeedbackLabel().setText("Falsch");
			view.getFeedbackLabel().setForeground(Color.RED);
		}
	}

	/**
	 * Diese innere Klasse kümmert sich um die Ereignisbehandlung beim Beenden des
	 * Rechentrainers.
	 * 
	 * @author ProkSy-Team
	 * @version 1.0
	 * 
	 */
	public class BeendenListener implements WindowListener {

		/*
		 * (non-Javadoc)
		 * 
		 * @see java.awt.event.WindowListener#windowOpened(java.awt.event.WindowEvent)
		 */
		@Override
		public void windowOpened(WindowEvent e) {
		}

		/*
		 * (non-Javadoc)
		 * 
		 * @see java.awt.event.WindowListener#windowClosing(java.awt.event.WindowEvent)
		 */
		@Override
		public void windowClosing(WindowEvent e) {
			int eingabe = JOptionPane.showConfirmDialog(null, "Wollen Sie das Rechentraining wirklich beenden?",
					"Beenden", JOptionPane.YES_NO_CANCEL_OPTION);
			if (eingabe == JOptionPane.YES_OPTION) {
				System.exit(0);
			}
		}

		/*
		 * (non-Javadoc)
		 * 
		 * @see java.awt.event.WindowListener#windowClosed(java.awt.event.WindowEvent)
		 */
		@Override
		public void windowClosed(WindowEvent e) {
		}

		/*
		 * (non-Javadoc)
		 * 
		 * @see
		 * java.awt.event.WindowListener#windowIconified(java.awt.event.WindowEvent)
		 */
		@Override
		public void windowIconified(WindowEvent e) {
		}

		/*
		 * (non-Javadoc)
		 * 
		 * @see
		 * java.awt.event.WindowListener#windowDeiconified(java.awt.event.WindowEvent)
		 */
		@Override
		public void windowDeiconified(WindowEvent e) {
		}

		/*
		 * (non-Javadoc)
		 * 
		 * @see
		 * java.awt.event.WindowListener#windowActivated(java.awt.event.WindowEvent)
		 */
		@Override
		public void windowActivated(WindowEvent e) {
		}

		/*
		 * (non-Javadoc)
		 * 
		 * @see
		 * java.awt.event.WindowListener#windowDeactivated(java.awt.event.WindowEvent)
		 */
		@Override
		public void windowDeactivated(WindowEvent e) {
		}
	}

}
