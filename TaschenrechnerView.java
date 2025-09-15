package edu.kit.aifb.proksy.taschenrechner.view;

import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

/**
 * Diese Klasse stellt einen Taschenrechner dar
 * 
 * @version 1.0
 * @author ProkSy-Team
 *
 */
@SuppressWarnings("serial")
public class TaschenrechnerView extends JFrame {
	private Container contentPane;
	private final Color RECHNER_GRAY = new Color(212, 208, 200);
	private final Insets RECHNER_MARGIN_VERTICAL = new Insets(4, 2, 4, 2);
	private final Insets RECHNER_MARGIN_HOR = new Insets(4, 4, 4, 4);
	private final Font RECHNER_FONT = new Font("Arial", 0, 12);

	private JMenuBar menuBar;
	private JMenu menuBearbeiten;
	private JMenu menuAnsicht;
	private JMenu menuHilfe;
	private JMenuItem menuItemKopieren;
	private JMenuItem menuItemEinfuegen;
	private JRadioButtonMenuItem menuItemStandard;
	private JRadioButtonMenuItem menuItemWissenschaftlich;
	private JMenuItem menuItemZifferngruppierung;
	private JMenuItem menuItemHilfethemen;
	private JMenuItem menuItemInfo;

	private ButtonGroup bgAnsicht;
	private JPanel panel1;
	private JPanel panel2;
	private JPanel panel3;
	private JPanel panel4;
	private JPanel panel5;
	private JPanel panel6;

	private JTextField tfDisplay;
	private JTextField tfM;
	private JButton buttonMC;
	private JButton buttonMR;
	private JButton buttonMS;
	private JButton buttonMPlus;
	private JButton buttonRuecktaste;
	private JButton buttonCE;
	private JButton buttonC;
	private JButton button7;
	private JButton button8;
	private JButton button9;
	private JButton buttonDiv;
	private JButton buttonSqrt;
	private JButton button4;
	private JButton button5;
	private JButton button6;
	private JButton buttonMul;
	private JButton buttonProzent;
	private JButton button1;
	private JButton button2;
	private JButton button3;
	private JButton buttonMinus;
	private JButton buttonKehrwert;
	private JButton button0;
	private JButton buttonPlusMinus;
	private JButton buttonKomma;
	private JButton buttonPlus;
	private JButton buttonGleich;

	public TaschenrechnerView() {
		// Fenster-Layout
		try {
			UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
			System.out.println(
					"UIManager.getSystemLookAndFeelClassName() = " + UIManager.getSystemLookAndFeelClassName());
		} catch (Exception e) {
			System.out.println("Error setting native LAF: " + e);
		}

		contentPane = getContentPane();
		contentPane.setBackground(RECHNER_GRAY);

		// Menue erstellen
		menuBearbeiten = new JMenu("Bearbeiten");
		menuBearbeiten.setMnemonic(KeyEvent.VK_B);
		menuItemKopieren = new JMenuItem("Kopieren");
		menuItemKopieren.setMnemonic(KeyEvent.VK_K);
		menuItemKopieren.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_C, InputEvent.CTRL_DOWN_MASK));
		menuItemEinfuegen = new JMenuItem("Einfügen");
		menuItemEinfuegen.setMnemonic(KeyEvent.VK_E);
		menuItemEinfuegen.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_V, InputEvent.CTRL_DOWN_MASK));
		menuBearbeiten.add(menuItemKopieren);
		menuBearbeiten.add(menuItemEinfuegen);

		menuAnsicht = new JMenu("Ansicht");
		menuAnsicht.setMnemonic(KeyEvent.VK_A);
		menuItemStandard = new JRadioButtonMenuItem("Standard");
		menuItemStandard.setMnemonic(KeyEvent.VK_S);
		menuItemStandard.setSelected(true);
		menuItemWissenschaftlich = new JRadioButtonMenuItem("Wissenschaftlich");
		menuItemWissenschaftlich.setMnemonic(KeyEvent.VK_W);
		menuItemWissenschaftlich.setSelected(false);
		menuItemZifferngruppierung = new JMenuItem("Zifferngruppierung");
		menuItemZifferngruppierung.setMnemonic(KeyEvent.VK_Z);

		bgAnsicht = new ButtonGroup();
		bgAnsicht.add(menuItemStandard);
		bgAnsicht.add(menuItemWissenschaftlich);

		menuAnsicht.add(menuItemStandard);
		menuAnsicht.add(menuItemWissenschaftlich);
		menuAnsicht.addSeparator();
		menuAnsicht.add(menuItemZifferngruppierung);

		menuHilfe = new JMenu("?");
		menuHilfe.setMnemonic(KeyEvent.VK_H);
		menuItemHilfethemen = new JMenuItem("Hilfethemen");
		menuItemHilfethemen.setMnemonic(KeyEvent.VK_H);
		menuItemInfo = new JMenuItem("Info");
		menuItemInfo.setMnemonic(KeyEvent.VK_I);
		menuHilfe.add(menuItemHilfethemen);
		menuHilfe.addSeparator();
		menuHilfe.add(menuItemInfo);

		menuBar = new JMenuBar();
		menuBar.add(menuBearbeiten);
		menuBar.add(menuAnsicht);
		menuBar.add(menuHilfe);

		setJMenuBar(menuBar);

		// Panels erzeugen
		panel1 = new JPanel(new BorderLayout());
		panel2 = new JPanel(new BorderLayout());
		panel3 = new JPanel(new GridLayout(5, 1, 5, 5));
		panel4 = new JPanel(new BorderLayout());
		panel5 = new JPanel(new GridLayout(1, 3, 5, 5));
		panel6 = new JPanel(new GridLayout(4, 5, 5, 5));

		// Panels ineinander verschachteln, um Layout zu erzielen
		contentPane.add(panel1, BorderLayout.NORTH);
		contentPane.add(panel2, BorderLayout.SOUTH);
		panel2.add(panel3, BorderLayout.WEST);
		panel2.add(panel4, BorderLayout.EAST);
		panel4.add(panel5, BorderLayout.NORTH);
		panel4.add(panel6, BorderLayout.SOUTH);

		// Erzeugen der Anzeige
		tfDisplay = new JTextField("0,");
		tfDisplay.setEditable(false);
		tfDisplay.setBackground(Color.WHITE);
		tfDisplay.setHorizontalAlignment(JTextField.RIGHT);
		tfDisplay.setFont(RECHNER_FONT);
		panel1.add(tfDisplay);

		// Erzeugen der Buttons

		// senkrechte Schalterleiste links
		tfM = new JTextField("M");
		tfM.setText("");
		tfM.setEditable(false);
		tfM.setBackground(RECHNER_GRAY);
		tfM.setHorizontalAlignment(JTextField.CENTER);
		tfM.setFont(RECHNER_FONT);
		buttonMC = new JButton("MC");
		buttonMC.setForeground(Color.RED);
		buttonMC.setMargin(RECHNER_MARGIN_VERTICAL);
		buttonMC.setFont(RECHNER_FONT);
		buttonMR = new JButton("MR");
		buttonMR.setForeground(Color.RED);
		buttonMR.setMargin(RECHNER_MARGIN_VERTICAL);
		buttonMR.setFont(RECHNER_FONT);
		buttonMS = new JButton("MS");
		buttonMS.setForeground(Color.RED);
		buttonMS.setMargin(RECHNER_MARGIN_VERTICAL);
		buttonMS.setFont(RECHNER_FONT);
		buttonMPlus = new JButton("M+");
		buttonMPlus.setForeground(Color.RED);
		buttonMPlus.setMargin(RECHNER_MARGIN_VERTICAL);
		buttonMPlus.setFont(RECHNER_FONT);

		panel3.add(tfM);
		panel3.add(buttonMC);
		panel3.add(buttonMR);
		panel3.add(buttonMS);
		panel3.add(buttonMPlus);

		// waagrechte Schalterleiste oben
		buttonRuecktaste = new JButton("Rücktaste");
		buttonCE = new JButton("CE");
		buttonC = new JButton("C");
		buttonRuecktaste.setMargin(RECHNER_MARGIN_HOR);
		buttonRuecktaste.setForeground(Color.RED);
		buttonRuecktaste.setFont(RECHNER_FONT);
		buttonCE.setMargin(RECHNER_MARGIN_HOR);
		buttonCE.setForeground(Color.RED);
		buttonCE.setFont(RECHNER_FONT);
		buttonC.setMargin(RECHNER_MARGIN_HOR);
		buttonC.setForeground(Color.RED);
		buttonC.setFont(RECHNER_FONT);

		panel5.add(buttonRuecktaste);
		panel5.add(buttonCE);
		panel5.add(buttonC);

		// unterer Schalterblock

		// unterer Schalterblock Zeile 1
		button7 = new JButton("7");
		button7.setMargin(RECHNER_MARGIN_VERTICAL);
		button7.setForeground(Color.BLUE);
		button7.setFont(RECHNER_FONT);
		button8 = new JButton("8");
		button8.setMargin(RECHNER_MARGIN_VERTICAL);
		button8.setForeground(Color.BLUE);
		button8.setFont(RECHNER_FONT);
		button9 = new JButton("9");
		button9.setMargin(RECHNER_MARGIN_VERTICAL);
		button9.setForeground(Color.BLUE);
		button9.setFont(RECHNER_FONT);
		buttonDiv = new JButton("/");
		buttonDiv.setMargin(RECHNER_MARGIN_VERTICAL);
		buttonDiv.setForeground(Color.RED);
		buttonDiv.setFont(RECHNER_FONT);
		buttonSqrt = new JButton("sqrt");
		buttonSqrt.setMargin(RECHNER_MARGIN_VERTICAL);
		buttonSqrt.setForeground(Color.RED);
		buttonSqrt.setFont(RECHNER_FONT);

		panel6.add(button7);
		panel6.add(button8);
		panel6.add(button9);
		panel6.add(buttonDiv);
		panel6.add(buttonSqrt);

		// unterer Schalterblock Zeile 2
		button4 = new JButton("4");
		button4.setMargin(RECHNER_MARGIN_VERTICAL);
		button4.setForeground(Color.BLUE);
		button4.setFont(RECHNER_FONT);
		button5 = new JButton("5");
		button5.setMargin(RECHNER_MARGIN_VERTICAL);
		button5.setForeground(Color.BLUE);
		button5.setFont(RECHNER_FONT);
		button6 = new JButton("6");
		button6.setMargin(RECHNER_MARGIN_VERTICAL);
		button6.setForeground(Color.BLUE);
		button6.setFont(RECHNER_FONT);
		buttonMul = new JButton("*");
		buttonMul.setMargin(RECHNER_MARGIN_VERTICAL);
		buttonMul.setForeground(Color.RED);
		buttonMul.setFont(RECHNER_FONT);
		buttonProzent = new JButton("%");
		buttonProzent.setMargin(RECHNER_MARGIN_VERTICAL);
		buttonProzent.setForeground(Color.RED);
		buttonProzent.setFont(RECHNER_FONT);

		panel6.add(button4);
		panel6.add(button5);
		panel6.add(button6);
		panel6.add(buttonMul);
		panel6.add(buttonProzent);

		// unterer Schalterblock Zeile 3
		button1 = new JButton("1");
		button1.setMargin(RECHNER_MARGIN_VERTICAL);
		button1.setForeground(Color.BLUE);
		button1.setFont(RECHNER_FONT);
		button2 = new JButton("2");
		button2.setMargin(RECHNER_MARGIN_VERTICAL);
		button2.setForeground(Color.BLUE);
		button2.setFont(RECHNER_FONT);
		button3 = new JButton("3");
		button3.setMargin(RECHNER_MARGIN_VERTICAL);
		button3.setForeground(Color.BLUE);
		button3.setFont(RECHNER_FONT);
		buttonMinus = new JButton("-");
		buttonMinus.setMargin(RECHNER_MARGIN_VERTICAL);
		buttonMinus.setForeground(Color.RED);
		buttonMinus.setFont(RECHNER_FONT);
		buttonKehrwert = new JButton("1/x");
		buttonKehrwert.setMargin(RECHNER_MARGIN_VERTICAL);
		buttonKehrwert.setForeground(Color.RED);
		buttonKehrwert.setFont(RECHNER_FONT);

		panel6.add(button1);
		panel6.add(button2);
		panel6.add(button3);
		panel6.add(buttonMinus);
		panel6.add(buttonKehrwert);

		// unterer Schalterblock Zeile 4
		button0 = new JButton("0");
		button0.setMargin(RECHNER_MARGIN_VERTICAL);
		button0.setForeground(Color.BLUE);
		button0.setFont(RECHNER_FONT);
		buttonPlusMinus = new JButton("+/-");
		buttonPlusMinus.setMargin(RECHNER_MARGIN_VERTICAL);
		buttonPlusMinus.setForeground(Color.BLUE);
		buttonPlusMinus.setFont(RECHNER_FONT);
		buttonKomma = new JButton(",");
		buttonKomma.setMargin(RECHNER_MARGIN_VERTICAL);
		buttonKomma.setForeground(Color.BLUE);
		buttonKomma.setFont(RECHNER_FONT);
		buttonPlus = new JButton("+");
		buttonPlus.setMargin(RECHNER_MARGIN_VERTICAL);
		buttonPlus.setForeground(Color.RED);
		buttonPlus.setFont(RECHNER_FONT);
		buttonGleich = new JButton("=");
		buttonGleich.setMargin(RECHNER_MARGIN_VERTICAL);
		buttonGleich.setForeground(Color.RED);
		buttonGleich.setFont(RECHNER_FONT);

		panel6.add(button0);
		panel6.add(buttonPlusMinus);
		panel6.add(buttonKomma);
		panel6.add(buttonPlus);
		panel6.add(buttonGleich);

	}
}
