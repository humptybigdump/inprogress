package edu.kit.aifb.proksy.umrechner.controller;

import java.awt.event.*;
import java.text.*;
import java.util.*;

import javax.swing.JOptionPane;
import javax.swing.JTextField;

import edu.kit.aifb.proksy.umrechner.model.UnitOfLength;
import edu.kit.aifb.proksy.umrechner.view.UmrechnerView;

/**
 * Die Klasse UmrechnerController kümmert sich um die Verarbeitung von
 * Benutzereingaben im zugehörigen View
 * 
 * @version 1.0
 * @author ProkSy-Team
 *
 */
public class UmrechnerController {

	private UmrechnerView view; // Referenz auf das zugehörige View

	private boolean direction; // Gibt an, in welche Richtung umgerechnet wird (von links nach
	// rechts oder umgekehrt)

	/**
	 * Erzeugt ein neues UnitListener-Objekt und gibt es zurück
	 * 
	 * @return neues UnitListener-Objekt
	 */
	public UnitListener createUnitListener() {
		return new UnitListener();
	}

	/**
	 * Erzeugt ein neues CalculateListener-Objekt und gibt es zurück
	 * 
	 * @return neues CalculateListener-Objekt
	 */
	public CalculateListener createCalculateListener() {
		return new CalculateListener();
	}

	/**
	 * Setzt die vom Controller zu verwaltende View
	 * 
	 * @param view zu verwaltende View
	 */
	public void setView(UmrechnerView view) {
		this.view = view;
		direction = false;
		view.getUnitButton().setText(">");
		view.getTextFieldRight().setEditable(false);
		view.getTextFieldLeft().setEditable(true);
	}

	/**
	 * Diese innere Klasse implementiert das ActionListener-Interface, kann also
	 * verwendet werden, um Benutzerinteraktion mit dem GUI zu verarbeiten. Sie soll
	 * sich um Ereignisse des unitButtons kümmern
	 * 
	 * @author Jonas Lehner
	 * 
	 */
	class UnitListener implements ActionListener {

		/*
		 * Diese Methode wird aufgerufen, wenn ein Button, dem eine Instanz dieser
		 * Klasse als Listener hinzugefügt wurde, betätigt wird
		 * 
		 * (non-Javadoc)
		 * 
		 * @see java.awt.event.ActionListener#actionPerformed(java.awt.event.ActionEvent
		 * )
		 */
		@Override
		public void actionPerformed(ActionEvent e) {
			if (direction) {
				direction = false;
				view.getUnitButton().setText(">");
				view.getTextFieldRight().setEditable(false);
				view.getTextFieldLeft().setEditable(true);
			} else {
				direction = true;
				view.getUnitButton().setText("<");
				view.getTextFieldRight().setEditable(true);
				view.getTextFieldLeft().setEditable(false);
			}
		}
	}

	/**
	 * Diese innere Klasse implementiert das ActionListener-Interface, kann also
	 * verwendet werden, um Benutzerinteraktion mit dem GUI zu verarbeiten. Sie soll
	 * sich um Ereignisse des calculateButtons kümmern
	 * 
	 * @author Jonas Lehner
	 * 
	 */
	class CalculateListener implements ActionListener {

		/*
		 * Diese Methode wird aufgerufen, wenn ein Button, dem eine Instanz dieser
		 * Klasse als Listener hinzugefügt wurde, betätigt wird
		 * 
		 * (non-Javadoc)
		 * 
		 * @see java.awt.event.ActionListener#actionPerformed(java.awt.event.ActionEvent
		 * )
		 */
		@Override
		public void actionPerformed(ActionEvent e) {
			JTextField sourceTextField;
			JTextField destinationTextField;
			UnitOfLength sourceUnit;
			UnitOfLength destinationUnit;
			if (direction) { // stellt fest, in welche Richtung umgerechnet werden soll
				sourceTextField = view.getTextFieldRight();
				destinationTextField = view.getTextFieldLeft();
				sourceUnit = (UnitOfLength) view.getCbUnitRight().getSelectedItem();
				destinationUnit = (UnitOfLength) view.getCbUnitLeft().getSelectedItem();
			} else {
				sourceTextField = view.getTextFieldLeft();
				destinationTextField = view.getTextFieldRight();
				sourceUnit = (UnitOfLength) view.getCbUnitLeft().getSelectedItem();
				destinationUnit = (UnitOfLength) view.getCbUnitRight().getSelectedItem();
			}

			NumberFormat format = NumberFormat.getInstance(Locale.GERMANY); // Kümmert sich um das
			// deutsche
			// Dezimaltrennzeichen

			try { // Beim Umwandeln eines Strings (aus dem Textfeld) in eine Zahl kann es zu
					// Exceptions kommen. Deswegen muss die Umwandlung in einem try-Block
					// stattfinden
				Number number = format.parse(sourceTextField.getText());
				double sourceValue = number.doubleValue();
				double destinationValue;
				destinationValue = sourceValue * sourceUnit.getInMm() / destinationUnit.getInMm(); // eigentliche
				// Umrechnung
				DecimalFormat dfOutput = new DecimalFormat("0.000", new DecimalFormatSymbols(Locale.GERMANY)); // Legt das Ausgabeformat fest
				// (Beachten Sie, dass hier ein Punkt als Dezimaltrennzeichen stehen muss)
				String destinationString = dfOutput.format(destinationValue);
				destinationTextField.setText(destinationString); // schreibt Ergebnis in das entsprechende Textfeld
			} catch (ParseException pEx) { // fängt ParseException, die beim Umrechnen von nicht
				// zulässigen Eingabewerten geworfen werden kann
				if (!view.getCbIgnoreExceptions().isSelected()) {
					JOptionPane.showMessageDialog(view, "Diese Eingabe ist nicht gültig.", "Eingabefehler",
							JOptionPane.ERROR_MESSAGE);// Gibt den Fehlerdialog aus
				}
			}
		}
	}

}
