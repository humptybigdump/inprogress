package edu.kit.aifb.proksy.werBinIch;

/**
 * @version 1.0
 * @author ProkSy-Team
 *
 */
public class WerBinIchMain {
	
	public static void main(String[] args) {
		WerBinIch_a<Integer> a = new WerBinIch_a<>(12);
		WerBinIch_a<String> b = new WerBinIch_a<>("Hallo");
		WerBinIch_a<Double> c = new WerBinIch_a<>(1.2);
		WerBinIch_a<Character> d = new WerBinIch_a<>('+');
		
		WerBinIch_b.dasBinIch(12);
		WerBinIch_b.dasBinIch("Hallo");
		WerBinIch_b.dasBinIch(1.2);
		WerBinIch_b.dasBinIch('+');
	}
}
