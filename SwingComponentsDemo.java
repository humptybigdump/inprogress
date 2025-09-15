package edu.kit.aifb.proksy.swingComponentsDemo;

import javax.swing.*;

/**
 * Diese Klasse erzeugt ein Fenster, in dessen Menü die Struktur der
 * Swing-Komponenten abgebildet wird.
 *
 * @version 1.0
 * @author ProkSy-Team
 *
 */
@SuppressWarnings("serial")
public class SwingComponentsDemo extends JFrame {

	// Menueleiste
	private JMenuBar menuBar = new JMenuBar();

	// Menue-Ebene 0
	private JMenu menu = new JMenu("JComponent");

	// Menue-Ebene 1
	private JMenu menuAbstractButton = new JMenu("AbstractButton");
	private JMenuItem menuItemJLabel = new JMenuItem("JLabel");
	private JMenuItem menuItemJComboBox = new JMenuItem("JComboBox");
	private JMenuItem menuItemJMenuBar = new JMenuItem("JMenuBar");
	private JMenuItem menuItemJList = new JMenuItem("JList");
	private JMenuItem menuItemJScrollPane = new JMenuItem("JScrollPane");
	private JMenu menuJTextComponent = new JMenu("JTextComponent");
	private JMenuItem menuItemJPanel = new JMenuItem("JPanel");
	private JMenuItem menuItemJTable = new JMenuItem("JTable");

	// Menue-Ebene 2
	private JMenuItem menuItemJButton = new JMenuItem("JButton");
	private JMenu menuJToggleButton = new JMenu("JToggleButton");
	private JMenu menuJMenuItem = new JMenu("JMenuItem");
	private JMenuItem menuItemJTextArea = new JMenuItem("JTextArea");
	private JMenu menuJTextField = new JMenu("JTextField");
	private JMenu menuJTextPane = new JMenu("JTextPane");

	// Menue-Ebene 3
	private JMenuItem menuItemJCheckBox = new JMenuItem("JCheckBox");
	private JMenuItem menuItemJRadioButton = new JMenuItem("JRadioButton");
	private JMenuItem menuItemJMenu = new JMenuItem("JMenu");
	private JMenuItem menuItemJCheckBoxMenuItem = new JMenuItem("JCheckBoxMenuItem");
	private JMenuItem menuItemJRadioButtonMenuItem = new JMenuItem("JRadioButtonMenuItem");
	private JMenuItem menuItemJPasswordField = new JMenuItem("JPasswordField");
	private JMenuItem menuItemJHTMLPane = new JMenuItem("JHTMLPane");

	public SwingComponentsDemo() {
		setDefaultCloseOperation(EXIT_ON_CLOSE);

		// Menue top-down zusammensetzen

		// Menue-Ebene 1
		menu.add(menuAbstractButton);
		menu.add(menuItemJLabel);
		menu.add(menuItemJComboBox);
		menu.add(menuItemJMenuBar);
		menu.add(menuItemJList);
		menu.add(menuItemJScrollPane);
		menu.add(menuJTextComponent);
		menu.add(menuItemJPanel);
		menu.add(menuItemJTable);

		// Menue-Ebene 2
		menuAbstractButton.add(menuItemJButton);
		menuAbstractButton.add(menuJToggleButton);
		menuAbstractButton.add(menuJMenuItem);
		menuJTextComponent.add(menuItemJTextArea);
		menuJTextComponent.add(menuJTextField);
		menuJTextComponent.add(menuJTextPane);

		// Menue-Ebene 3
		menuJToggleButton.add(menuItemJCheckBox);
		menuJToggleButton.add(menuItemJRadioButton);
		menuJMenuItem.add(menuItemJMenu);
		menuJMenuItem.add(menuItemJCheckBoxMenuItem);
		menuJMenuItem.add(menuItemJRadioButtonMenuItem);
		menuJTextField.add(menuItemJPasswordField);
		menuJTextPane.add(menuItemJHTMLPane);

		// Menue der Menueleiste hinzufuegen und anzeigen
		menuBar.add(menu);
		setJMenuBar(menuBar);
	}

	public static void main(String[] args) {
		SwingComponentsDemo myFrame = new SwingComponentsDemo();
		myFrame.setSize(200, 300);
		myFrame.setVisible(true);
	}
}
