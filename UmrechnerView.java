package edu.kit.aifb.proksy.umrechner.view;

import java.awt.*;
import java.util.*;

import javax.swing.*;
import javax.swing.border.*;

import edu.kit.aifb.proksy.umrechner.controller.UmrechnerController;
import edu.kit.aifb.proksy.umrechner.model.*;

/**
 * Diese Klasse repräsentiert ein Fenster, mit dem Längeneinheiten ineinander
 * umgerechnet werden können
 * 
 * @version 1.0
 * @author ProkSy-Team
 *
 */
@SuppressWarnings("serial")
public class UmrechnerView extends JFrame {

	// Allgemein
	private UmrechnerController controller;
	private Font font; // Schriftart, die in einigen der Komponenten verwendet wird

	// ContentPane
	private Container contentPane;

	// Erstes Panel (Textfelder)
	private JPanel inputPanel;
	private JTextField textFieldLeft;
	private JTextField textFieldRight;

	// Zweites Panel (Einheiten)
	private JPanel unitPanel;
	private JComboBox<UnitOfLength> cbUnitLeft;
	private JComboBox<UnitOfLength> cbUnitRight;
	private JButton unitButton;

	// Drittes Panel (Einstellungen)
	private JPanel settingsPanel;
	private JCheckBox cbSeparator;
	private JCheckBox cbIgnoreExceptions;
	private ButtonGroup btnGroupColor;
	private JRadioButton rbGreen;
	private JRadioButton rbRed;

	// Viertes Panel (Berechnen)
	private JButton calculateButton;

	/**
	 * Konstruktor der Klasse UmrechnerView
	 * 
	 * @param units Set von Einheiten-Objekten (UnitOfLength), die berücksichtigt
	 *              werden sollen
	 */
	public UmrechnerView(TreeSet<UnitOfLength> units) {
		// Allgemeine Einstellungen
		setTitle("Umrechner");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(100, 100, 400, 300);
		contentPane = getContentPane();
		((JPanel) contentPane).setBorder(new EmptyBorder(5, 5, 5, 5));
		contentPane.setLayout(new GridLayout(4, 1, 10, 10));
		font = new Font("Tahoma", Font.PLAIN, 16);

		// Erstes Panel (Textfelder)
		inputPanel = new JPanel();
		inputPanel.setLayout(new GridLayout(1, 2, 10, 10));

		textFieldLeft = new JTextField();
		textFieldLeft.setFont(font);
		inputPanel.add(textFieldLeft);

		textFieldRight = new JTextField();
		textFieldRight.setFont(font);
		inputPanel.add(textFieldRight);

		contentPane.add(inputPanel);

		// Zweites Panel (Einheiten)
		unitPanel = new JPanel();
		unitPanel.setBorder(new TitledBorder(null, "Umrechnung", TitledBorder.LEADING, TitledBorder.TOP, null, null));
		unitPanel.setLayout(new GridLayout(1, 3, 10, 0));

		cbUnitLeft = new JComboBox<UnitOfLength>(units.toArray(new UnitOfLength[0]));
		cbUnitLeft.setFont(font);
		unitPanel.add(cbUnitLeft);

		unitButton = new JButton(">");
		unitButton.setFont(font);
		unitPanel.add(unitButton);

		cbUnitRight = new JComboBox<UnitOfLength>(units.toArray(new UnitOfLength[0]));
		cbUnitRight.setFont(font);
		unitPanel.add(cbUnitRight);

		contentPane.add(unitPanel);

		// Drittes Panel (Einstellungen)
		settingsPanel = new JPanel();
		settingsPanel
				.setBorder(new TitledBorder(null, "Einstellungen", TitledBorder.LEADING, TitledBorder.TOP, null, null));
		settingsPanel.setLayout(new GridLayout(2, 2, 0, 0));

		cbSeparator = new JCheckBox("Tausendertrennzeichen");
		settingsPanel.add(cbSeparator);

		btnGroupColor = new ButtonGroup();

		rbGreen = new JRadioButton("Ergebnis grün");
		settingsPanel.add(rbGreen);
		btnGroupColor.add(rbGreen);

		cbIgnoreExceptions = new JCheckBox("Fehler ignorieren");
		settingsPanel.add(cbIgnoreExceptions);

		rbRed = new JRadioButton("Ergebnis rot");
		settingsPanel.add(rbRed);
		btnGroupColor.add(rbRed);

		contentPane.add(settingsPanel);

		// Viertes Panel (Berechnen)
		calculateButton = new JButton("Berechnen");
		calculateButton.setFont(font);
		contentPane.add(calculateButton);

	}

	/**
	 * Setzt den für die View zuständigen Controller
	 * 
	 * @param controller zu setzender Controller
	 */
	public void setController(UmrechnerController controller) {
		this.controller = controller;
		unitButton.addActionListener(this.controller.createUnitListener());
		calculateButton.addActionListener(this.controller.createCalculateListener());
	}

	/**
	 * Liefert eine Referenz auf den unitButton zurück
	 * 
	 * @return unitButton
	 */
	public JButton getUnitButton() {
		return unitButton;
	}

	/**
	 * Liefert eine Referenz auf die cbIgnoreExceptions zurück
	 * 
	 * @return cbIgnoreExceptions
	 */
	public JCheckBox getCbIgnoreExceptions() {
		return cbIgnoreExceptions;
	}

	/**
	 * Liefert eine Referenz auf das textFieldLeft zurück
	 * 
	 * @return textFieldLeft
	 */
	public JTextField getTextFieldLeft() {
		return textFieldLeft;
	}

	/**
	 * Liefert eine Referenz auf das textFieldRight zurück
	 * 
	 * @return textFieldRight
	 */
	public JTextField getTextFieldRight() {
		return textFieldRight;
	}

	/**
	 * Liefert eine Referenz auf die cbUnitLeft zurück
	 * 
	 * @return cbUnitLeft
	 */
	public JComboBox<UnitOfLength> getCbUnitLeft() {
		return cbUnitLeft;
	}

	/**
	 * Liefert eine Referenz auf die cbUnitRight zurück
	 * 
	 * @return cbUnitRight
	 */
	public JComboBox<UnitOfLength> getCbUnitRight() {
		return cbUnitRight;
	}

}
