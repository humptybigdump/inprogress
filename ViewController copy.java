package edu.kit.aifb.proksy.ErdkundeRMI.client.controller;

import java.awt.event.*;
import java.rmi.registry.LocateRegistry;
import java.text.*;
import java.util.*;
import java.rmi.*;
import java.rmi.registry.Registry;

import edu.kit.aifb.proksy.ErdkundeRMI.client.view.*;
import edu.kit.aifb.proksy.ErdkundeRMI.server.controller.Erdkunde;

/**
 * Diese Klasse enthält die ActionListener für das Frame.
 * 
 * @author ProkSy-Team
 * @version 1.0
 */
public class ViewController {
	private ClientFrame frame;

	private boolean bundesland = true;

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
	 * @author ProkSy-Team
	 * @version 1.0
	 */
	class StartListener implements ActionListener {
		String eingabe = null;
		String ausgabe = null;

		Registry registry;
		Erdkunde erdkunde;

		public StartListener() {
			try {
				registry = LocateRegistry.getRegistry("localhost", 1705);
				erdkunde = (Erdkunde) registry.lookup("rmi://localhost:1705/Erdkunde");
			} catch (RemoteException re) {
				re.printStackTrace();
			} catch (NotBoundException nbe) {
				// TODO Auto-generated catch block
				nbe.printStackTrace();
			}
		}

		/**
		 * Diese Methode wird aufgerufen, wenn der Start Button betätigt wird. Das Frame
		 * wird jetzt mit dem Server verbunden und bekommt den angefragten Wert
		 * geliefert.
		 */
		@Override
		public void actionPerformed(ActionEvent e) {
			if (bundesland) {
				eingabe = frame.getBundesland().getText();
			} else {
				eingabe = frame.getHauptstadt().getText();
			}
			try {
				ausgabe = erdkunde.topographie(eingabe, bundesland);
			} catch (RemoteException re) {
				re.printStackTrace();
			}

			if (bundesland) {
				frame.getHauptstadt().setText(ausgabe);
			} else {
				frame.getBundesland().setText(ausgabe);
			}
		}
	}

}
