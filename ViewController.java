package edu.kit.aifb.proksy.Erdkunde.client.controller;

import java.awt.event.*;
import java.text.*;
import java.util.*;

import edu.kit.aifb.proksy.Erdkunde.client.view.*;

/**
 * Diese Klasse enthält die ActionListener für das Frame.
 * 
 * @author ProkSy-Team
 * @version 1.0
 */
public class ViewController {
	private ClientFrame frame;
	private ClientController controller;

	private boolean bundesland = true;
	private boolean connected = false;

	/**
	 * Methode, mit der der ViewController eine Instanz des Frames zugeordnet
	 * bekommt.
	 * 
	 * @param frame
	 */
	public void setView(ClientFrame frame) {
		this.frame = frame;
	}

	/**
	 * Methode, mit der der ViewController eine Instanz des ClientControllers
	 * zugeordnet bekommt.
	 * 
	 * @param controller
	 */
	public void setClientController(ClientController controller) {
		this.controller = controller;
	}

	/**
	 * gibt einen neuen TauschListener zurück
	 * 
	 * @return new TauschListener()
	 */
	public TauschListener createTauschListener() {
		return new TauschListener();
	}

	/**
	 * gibt einen neuen StartListener zurück
	 * 
	 * @return new StartListener()
	 */
	public StartListener createStartListener() {
		return new StartListener();
	}

	/**
	 * innere Klasse, die den Listener für den Tausch Button repräsentiert
	 * 
	 * @author Janna
	 * @version 1.0
	 */
	class TauschListener implements ActionListener {
		/**
		 * Diese Methode wird aufgerufen, wenn der Tausch Button betätigt wird. Sie
		 * vertauscht die Zustände für die Editierbarkeit der beiden Textfelder.
		 */
		@Override
		public void actionPerformed(ActionEvent e) {
			if (frame.getBundesland().isEditable() == true) {
				frame.getBundesland().setEditable(false);
				frame.getHauptstadt().setEditable(true);
				frame.getHauptstadt().setText("");
				frame.getBundesland().setText("");
				bundesland = false;
			} else {
				frame.getBundesland().setEditable(true);
				frame.getHauptstadt().setEditable(false);
				frame.getHauptstadt().setText("");
				frame.getBundesland().setText("");
				bundesland = true;
			}
		}
	}

	/**
	 * Innere Klasse, die den ActionListener für den Start Button repräsentiert.
	 * 
	 * @author Janna
	 * @version 1.0
	 */
	class StartListener implements ActionListener {
		String eingabe = null;
		String ausgabe = null;

		/**
		 * Diese Methode wird aufgerufen, wenn der Start Button betätigt wird. Das Frame
		 * wird jetzt mit dem Server verbunden und bekommt den angefragten Wert
		 * geliefert.
		 */
		@Override
		public void actionPerformed(ActionEvent e) {
			if (!connected) {
				controller.connectToServer(bundesland);
				connected = true;
			}
			if (bundesland) {
				eingabe = frame.getBundesland().getText();
			} else {
				eingabe = frame.getHauptstadt().getText();
			}
			controller.sendMessage(eingabe, bundesland);
			ausgabe = controller.receiveMessage();

			if (bundesland) {
				frame.getHauptstadt().setText(ausgabe);
			} else {
				frame.getBundesland().setText(ausgabe);
			}
		}
	}

}
