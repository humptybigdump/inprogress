package edu.kit.tm.eir;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import org.junit.Test;

public class TestHamming1511 extends AbstractHammingTest {

	// 76543210 FEDCBA98 -> p321p0pp _A987654 | pEDCpBpp _______F
	// 11111111 11111111 -> 01110100 01111111 | 01110100 00000001
	private static Byte[] testVector1Initialized1511 = new Byte[] {
		(byte) 0b01110100, (byte) 0b01111111, (byte) 0b01110100, (byte) 0b00000001
	};
	
	// 76543210 FEDCBA98 -> p321p0pp _A987654 | pEDCpBpp _______F
	// 11111111 11111111 -> 11111111 01111111 | 11111110 00000001
	private static Byte[] testVector1Hamming1511 = new Byte[] {
		(byte) 0b11111111, (byte) 0b01111111, (byte) 0b11111110, (byte) 0b00000001
	};
	
	// 76543210 FEDCBA98 -> p321p0pp _A987654 | pEDCpBpp _______F
	// 11110100 01001111 -> 00100000 01111111 | 01000100 00000000
	private static Byte[] testVector2Initialized1511 = new Byte[] {
		(byte) 0b00100000, (byte) 0b01111111, (byte) 0b01000100, (byte) 0b00000000
	};
	
	// 76543210 FEDCBA98 -> p321p0pp _A987654 | pEDCpBpp _______F
	// 11110100 01001111 -> 10101010 01111111 | 01001100 00000000
	private static Byte[] testVector2Hamming1511 = new Byte[] {
		(byte) 0b10101010, (byte) 0b01111111, (byte) 0b01001100, (byte) 0b00000000
	};
	
	private static Byte[] testVector1Xor2Bitflip1511 = new Byte[] {
		(byte) 0xef, (byte) 0xde, (byte) 0x05
	};
	
	private static Byte[] testVector2Xor2Bitflip1511 = new Byte[] {
		(byte) 0xe4, (byte) 0x6e, (byte) 0x05
	};
	
	private static Byte[] testVector1Xor3Bitflip1511 = new Byte[] {
		(byte) 0xc7, (byte) 0x77, (byte) 0x01
	};
	
	private static Byte[] testVector2Xor3Bitflip1511 = new Byte[] {
		(byte) 0xcc, (byte) 0xc7, (byte) 0x01
	};
	
	private final Hamming createHamming1511() {
		return new Hamming(15);
	}
	
	@Test
	public void testInitialize1511() {
		final Hamming hamming = createHamming1511();
		
		final List<Byte> vector1 = new ArrayList<Byte>(Arrays.asList(AbstractHammingTest.testVector1));
		final List<Byte> vector2 = new ArrayList<Byte>(Arrays.asList(AbstractHammingTest.testVector2));
		
		runInitialize(hamming, vector1, testVector1Initialized1511, 1);
		runInitialize(hamming, vector2, testVector2Initialized1511, 2);
	}

	@Test
	public void testHamming1511() {
		final Hamming hamming = createHamming1511();
		
		final List<Byte> vector1 = new ArrayList<Byte>(Arrays.asList(AbstractHammingTest.testVector1));
		final List<Byte> vector2 = new ArrayList<Byte>(Arrays.asList(AbstractHammingTest.testVector2));
		
		runHamming(hamming, vector1, testVector1Hamming1511, 1);
		runHamming(hamming, vector2, testVector2Hamming1511, 2);
	}
	
	@Test
	public void testVerifyValid1511(){
		final Hamming hamming = createHamming1511();
		
		final List<Byte> vector1 = new ArrayList<Byte>(Arrays.asList(AbstractHammingTest.testVector1));
		final List<Byte> vector2 = new ArrayList<Byte>(Arrays.asList(AbstractHammingTest.testVector2));
		
		runVerify(hamming, vector1, new Byte[0], AbstractHammingTest.testVector1, 1);
		runVerify(hamming, vector2, new Byte[0], AbstractHammingTest.testVector2, 2);
	}
	
	@Test
	public void testVerifyBitflip1511() {
		final Hamming hamming = createHamming1511();
		
		final List<Byte> vector1 = new ArrayList<Byte>(Arrays.asList(AbstractHammingTest.testVector1));
		final List<Byte> vector2 = new ArrayList<Byte>(Arrays.asList(AbstractHammingTest.testVector2));
		
		runVerify(hamming, vector1, AbstractHammingTest.xorMask1, AbstractHammingTest.testVector1, 1);
		runVerify(hamming, vector2, AbstractHammingTest.xorMask1, AbstractHammingTest.testVector2, 1);
	}
	
	@Test
	public void testVerifyBitflipFail1511() {
		final Hamming hamming = createHamming1511();
		
		final List<Byte> vector1 = new ArrayList<Byte>(Arrays.asList(AbstractHammingTest.testVector1));
		final List<Byte> vector2 = new ArrayList<Byte>(Arrays.asList(AbstractHammingTest.testVector2));
		
		runVerify(hamming, vector1, AbstractHammingTest.xorMask2, testVector1Xor2Bitflip1511, 1);
		runVerify(hamming, vector2, AbstractHammingTest.xorMask2, testVector2Xor2Bitflip1511, 2);
		runVerify(hamming, vector1, AbstractHammingTest.xorMask3, testVector1Xor3Bitflip1511, 1);
		runVerify(hamming, vector2, AbstractHammingTest.xorMask3, testVector2Xor3Bitflip1511, 2);
	}
	
}
