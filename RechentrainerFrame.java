package edu.kit.aifb.proksy.rechenspiel.view;

import java.awt.*;

import javax.swing.*;
import javax.swing.border.*;

import edu.kit.aifb.proksy.rechenspiel.controller.RechentrainerController;

/**
 * Diese Klasse stellt das Fester für den Rechentrainer dar. Außerdem wird die
 * Ereignisbehandlung für die Buttons hier implementiert.
 * 
 * @version 1.0
 * @author ProkSy-Team
 *
 */
@SuppressWarnings("serial")
public class RechentrainerFrame extends JFrame {
	public RechentrainerController controller;

	// Allgemein
	private Font fontBeschreibung;
	private Font fontTextfelder;

	// ContentPane
	private Container c;

	// Erstes Panel
	private JPanel beschreibungPanel;
	private JLabel beschreibungLabel;

	// Zweites Panel
	private JPanel aufgabePanel;
	private JTextField linkerOperandTextField;
	private JTextField rechterOperandTextField;
	private JComboBox<String> operatorComboBox;
	private String[] operatoren = { "+", "-" };
	private JLabel istgleichLabel;
	private JTextField ergebnisTextField;

	// Drittes Panel
	private JPanel ergebnisPanel;
	private JLabel feedbackLabel;

	// Viertes Panel
	private JPanel buttonPanel;
	private JButton neuButton;
	private JButton ueberpruefenButton;

	// Menue
	private JMenuBar menuBar;
	private JMenu menu;
	private ButtonGroup group;
	private JRadioButtonMenuItem items[];

	/**
	 * Konstruktor der Klasse
	 * 
	 * @param name Titel des Fensters
	 */
	public RechentrainerFrame(String name) {
		// Allgemein
		setTitle(name);
		c = getContentPane();
		c.setLayout(new GridLayout(4, 1, 10, 10));
		((JPanel) c).setBorder(new EmptyBorder(5, 5, 5, 5));
		fontBeschreibung = new Font("Tahoma", Font.PLAIN, 20);
		fontTextfelder = new Font("Tahoma", Font.PLAIN, 16);

		// Erstes Panel aufbauen
		beschreibungPanel = new JPanel(new BorderLayout());
		beschreibungLabel = new JLabel("Wählen Sie den richtigen Rechenoperator aus:", JLabel.CENTER);
		beschreibungLabel.setFont(fontBeschreibung);
		beschreibungPanel.add(beschreibungLabel, BorderLayout.CENTER);

		// Zweites Panel aufbauen
		aufgabePanel = new JPanel(new GridLayout(1, 5, 10, 0));
		aufgabePanel.setBorder(new TitledBorder(null, "Aufgabe", TitledBorder.LEADING, TitledBorder.TOP, null, null));
		linkerOperandTextField = new JTextField();
		linkerOperandTextField.setEditable(false);
		linkerOperandTextField.setFont(fontTextfelder);
		rechterOperandTextField = new JTextField();
		rechterOperandTextField.setEditable(false);
		rechterOperandTextField.setFont(fontTextfelder);
		operatorComboBox = new JComboBox<String>(operatoren);
		istgleichLabel = new JLabel("=", JTextField.CENTER);
		ergebnisTextField = new JTextField();
		ergebnisTextField.setEditable(false);
		ergebnisTextField.setFont(fontTextfelder);
		aufgabePanel.add(linkerOperandTextField);
		aufgabePanel.add(operatorComboBox);
		aufgabePanel.add(rechterOperandTextField);
		aufgabePanel.add(istgleichLabel);
		aufgabePanel.add(ergebnisTextField);

		// Drittes Panel aufbauen
		ergebnisPanel = new JPanel(new BorderLayout());
		ergebnisPanel.setBorder(new TitledBorder(null, "Ergebnis", TitledBorder.LEADING, TitledBorder.TOP, null, null));
		feedbackLabel = new JLabel("", JLabel.CENTER);
		feedbackLabel.setFont(fontBeschreibung);
		ergebnisPanel.add(feedbackLabel, BorderLayout.CENTER);

		// Viertes Panel aufbauen
		buttonPanel = new JPanel(new GridLayout(1, 2));
		neuButton = new JButton("Neue Rechenaufgabe");
		ueberpruefenButton = new JButton("Überprüfen");
		buttonPanel.add(neuButton);
		buttonPanel.add(ueberpruefenButton);

		// Menue aufbauen
		menuBar = new JMenuBar();
		menu = new JMenu("Schwierigkeit");
		group = new ButtonGroup();
		items = new JRadioButtonMenuItem[2];
		items[0] = new JRadioButtonMenuItem("Einfach");
		items[0].setMnemonic(java.awt.event.KeyEvent.VK_E);
		items[0].setSelected(true);
		items[1] = new JRadioButtonMenuItem("Schwer");
		items[1].setMnemonic(java.awt.event.KeyEvent.VK_S);
		for (int i = 0; i < items.length; i++) {
			group.add(items[i]);
		}
		for (int i = 0; i < items.length; i++) {
			menu.add(items[i]);
		}
		menuBar.add(menu);

		// Fenster aufbauen
		setJMenuBar(menuBar);
		c.add(beschreibungPanel);
		c.add(aufgabePanel);
		c.add(ergebnisPanel);
		c.add(buttonPanel);

	}

	public void setController(RechentrainerController controller) {
		this.controller = controller;
		neuButton.addActionListener(this.controller.createNeuButtonListener());
		ueberpruefenButton.addActionListener(this.controller.createUeberpruefenButtonListener());
		this.addWindowListener(this.controller.createBeendenListener());
	}

	public JLabel getFeedbackLabel() {
		return feedbackLabel;
	}

	public JRadioButtonMenuItem[] getItems() {
		return items;
	}

	public JTextField getLinkerOperandTextField() {
		return linkerOperandTextField;
	}

	public JTextField getRechterOperandTextField() {
		return rechterOperandTextField;
	}

	public JTextField getErgebnisTextField() {
		return ergebnisTextField;
	}

	public JComboBox<String> getOperatorComboBox() {
		return operatorComboBox;
	}
}