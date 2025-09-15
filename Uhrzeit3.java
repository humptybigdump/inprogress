package edu.kit.aifb.proksy.listenerDemo.separateKlasse;

import java.awt.*;
import java.awt.event.*;
import java.text.SimpleDateFormat;
import java.util.Date;

import javax.swing.*;

/**
 * Diese Variante realisiert den Listener in einer separaten Klasse
 * 
 * @version 1.0
 * @author ProkSy-Team
 *
 */
@SuppressWarnings("serial")
public class Uhrzeit3 extends JFrame {

    private JPanel contentPane;
    private JLabel lblUhrzeit;
    private JButton btnUhrzeitAktualisieren;

    /**
     * main-Methode der KLasse
     */
    public static void main(String[] args) {
	Uhrzeit3 frame = new Uhrzeit3();
	frame.setVisible(true);

    }

    /**
     * Konstruktor der Klasse
     */
    public Uhrzeit3() {
	setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
	setBounds(100, 100, 300, 150);
	setTitle("Uhrzeit");
	contentPane = new JPanel();
	setContentPane(contentPane);
	contentPane.setLayout(new GridLayout(2, 1, 0, 0));

	lblUhrzeit = new JLabel("UHRZEIT");
	lblUhrzeit.setHorizontalAlignment(SwingConstants.CENTER);
	contentPane.add(lblUhrzeit);

	btnUhrzeitAktualisieren = new JButton("Uhrzeit aktualisieren");
	btnUhrzeitAktualisieren.addActionListener(new ButtonListener(this));
	contentPane.add(btnUhrzeitAktualisieren);
    }

    /**
     * @return the lblUhrzeit
     */
    public JLabel getLblUhrzeit() {
	return lblUhrzeit;
    }
}
