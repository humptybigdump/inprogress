package edu.kit.aifb.proksy.lambdagui;

import java.awt.GridLayout;
import java.awt.event.ActionListener;
import javax.swing.*;

/**
 * Klasse enthält alle Läsungsbestandteile der Aufgabe.
 * 
 * @author ProkSy-Team
 * @version 1.0
 *
 */
public class Hauptklasse {
	public static void main(String[] args){
		JFrame frame = new JFrame("Lambda-Frame");
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.setLayout(new GridLayout(1, 3));
		JButton[] button = new JButton[3];

		// Aufgabenteil a)
		ActionListener al = e -> {
			JButton b = (JButton) e.getSource();
			int number = Integer.valueOf(b.getText());
			String text = String.valueOf(++number);
			b.setText(text);
		};

		// Erzeugung der Buttons und Registrierung der Listener
		for (int i = 0; i < button.length; i++) {
			button[i] = new JButton("0");
			button[i].addActionListener(al);
			frame.add(button[i]);
		}

		frame.setSize(300, 100);
		frame.setVisible(true);

		/*
		 * Aufgabenteil b)
		 */
		Runnable r = () -> {
			// Kleine Pause für den Thread
			while (true) {
				try {
					Thread.sleep(10);
				} catch (InterruptedException e) {
					e.printStackTrace();
				}
				
				//Zufällige Auswahl eines Buttons
				int buttonNumber = (int) (Math.random() * 3);
				String text = button[buttonNumber].getText();
				int number = Integer.valueOf(text);
				button[buttonNumber].setText("" + (++number));
				
				// Prüfen, ob der Button schon die 1000er Grenze erreicht hat.
				if (number >= 1000)
					break;
			}
		};
		new Thread(r).start();
	}
}