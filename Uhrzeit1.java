package edu.kit.aifb.proksy.listenerDemo.innereKlasse;

import java.awt.*;
import java.awt.event.*;
import java.text.SimpleDateFormat;
import java.util.Date;

import javax.swing.*;

/**
 * Diese Variante realisiert den Listener als innere Klasse
 * 
 * @version 1.0
 * @author ProkSy-Team
 *
 */
@SuppressWarnings("serial")
public class Uhrzeit1 extends JFrame {

    private JPanel contentPane;
    private JLabel lblUhrzeit;
    private JButton btnUhrzeitAktualisieren;

    /**
     * main-Methode der KLasse
     */
    public static void main(String[] args) {
	Uhrzeit1 frame = new Uhrzeit1();
	frame.setVisible(true);

    }

    /**
     * Konstruktor der Klasse
     */
    public Uhrzeit1() {
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
	btnUhrzeitAktualisieren.addActionListener(new ButtonListener());
	contentPane.add(btnUhrzeitAktualisieren);
    }

    /**
     * Innere Klasse, die als Listener fungiert
     * 
     * @author Jonas Lehner
     * 
     */
    class ButtonListener implements ActionListener {

	/*
	 * (non-Javadoc)
	 * 
	 * @see java.awt.event.ActionListener#actionPerformed(java.awt.event.ActionEvent)
	 */
	@Override
	public void actionPerformed(ActionEvent actionEvent) {
	    SimpleDateFormat sdf = new SimpleDateFormat("HH':'mm':'ss' Uhr'");
	    lblUhrzeit.setText(sdf.format(new Date()));

	}

    }

}
