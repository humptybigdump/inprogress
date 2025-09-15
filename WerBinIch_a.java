package edu.kit.aifb.proksy.werBinIch;

/**
 * @version 1.0
 * @author ProkSy-Team
 *
 */
public class WerBinIch_a <T> {
	
	public WerBinIch_a(T var) {
		dasBinIch(var);
	}
	
	public void dasBinIch(T var) {
		System.out.println("Ich bin vom Datentyp " + var.getClass());
	}
	
}


