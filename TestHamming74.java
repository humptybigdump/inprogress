package edu.kit.tm.eir;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import org.junit.Test;

public class TestHamming74 extends AbstractHammingTest {

	// 76543210 -> _321p0pp | _765p4pp
	// 11111111 -> 01110100 | 01110100
	private static Byte[] testVector1Initialized74 = new Byte[] {
		(byte) 0b01110100, (byte) 0b01110100, (byte) 0b01110100, (byte) 0b01110100
	};
	
	// 76543210 -> _321p0pp | _765p4pp
	// 11111111 -> 01111111 | 01111111
	private static Byte[] testVector1Hamming74 = new Byte[] {
		(byte) 0b01111111, (byte) 0b01111111, (byte) 0b01111111, (byte) 0b01111111
	};
	
	// 76543210 -> _321p0pp | _765p4pp
	// 11110100 -> 00100000 | 01110100
	private static Byte[] testVector2Initialized74 = new Byte[] {
		(byte) 0b00100000, (byte) 0b01110100, (byte) 0b01110100, (byte) 0b00100000
	};
	
	// 76543210 -> _321p0pp | _765p4pp
	// 11110100 -> 00101010 | 01111111
	private static Byte[] testVector2Hamming74 = new Byte[] {
		(byte) 0b00101010, (byte) 0b01111111, (byte) 0b01111111, (byte) 0b00101010
	};
	
	private static Byte[] testVector1Xor3Bitflip74 = new Byte[] {
		(byte) 0x56, (byte) 0xd8
	};
	
	private static Byte[] testVector2Xor3Bitflip74 = new Byte[] {
		(byte) 0x5d, (byte) 0x68
	};
	
	private final Hamming createHamming74() {
		return new Hamming74();
	}
	
	@Test
	public void testInitialize74() {
		final Hamming hamming = createHamming74();
		
		final List<Byte> vector1 = new ArrayList<Byte>(Arrays.asList(AbstractHammingTest.testVector1));
		final List<Byte> vector2 = new ArrayList<Byte>(Arrays.asList(AbstractHammingTest.testVector2));
		
		runInitialize(hamming, vector1, testVector1Initialized74, 1);
		runInitialize(hamming, vector2, testVector2Initialized74, 2);
	}
	
	@Test
	public void testHamming74() {
		final Hamming hamming = createHamming74();
		
		final List<Byte> vector1 = new ArrayList<Byte>(Arrays.asList(AbstractHammingTest.testVector1));
		final List<Byte> vector2 = new ArrayList<Byte>(Arrays.asList(AbstractHammingTest.testVector2));
		
		runHamming(hamming, vector1, testVector1Hamming74, 1);
		runHamming(hamming, vector2, testVector2Hamming74, 2);
	}
	
	@Test
	public void testVerifyValid74(){
		final Hamming hamming = createHamming74();
		
		final List<Byte> vector1 = new ArrayList<Byte>(Arrays.asList(AbstractHammingTest.testVector1));
		final List<Byte> vector2 = new ArrayList<Byte>(Arrays.asList(AbstractHammingTest.testVector2));
		
		runVerify(hamming, vector1, new Byte[0], AbstractHammingTest.testVector1, 1);
		runVerify(hamming, vector2, new Byte[0], AbstractHammingTest.testVector2, 2);
	}

	@Test
	public void testVerifyBitflip74() {
		final Hamming hamming = createHamming74();
		
		final List<Byte> vector1 = new ArrayList<Byte>(Arrays.asList(AbstractHammingTest.testVector1));
		final List<Byte> vector2 = new ArrayList<Byte>(Arrays.asList(AbstractHammingTest.testVector2));
		
		runVerify(hamming, vector1, AbstractHammingTest.xorMask1, AbstractHammingTest.testVector1, 1);
		runVerify(hamming, vector1, AbstractHammingTest.xorMask2, AbstractHammingTest.testVector1, 2);
		runVerify(hamming, vector2, AbstractHammingTest.xorMask1, AbstractHammingTest.testVector2, 1);
		runVerify(hamming, vector2, AbstractHammingTest.xorMask2, AbstractHammingTest.testVector2, 2);
	}
	
	@Test
	public void testVerifyBitflipFail74() {
		final Hamming hamming = createHamming74();
		
		final List<Byte> vector1 = new ArrayList<Byte>(Arrays.asList(AbstractHammingTest.testVector1));
		final List<Byte> vector2 = new ArrayList<Byte>(Arrays.asList(AbstractHammingTest.testVector2));
		
		runVerify(hamming, vector1, AbstractHammingTest.xorMask3, testVector1Xor3Bitflip74, 1);
		runVerify(hamming, vector2, AbstractHammingTest.xorMask3, testVector2Xor3Bitflip74, 2);
	}
	
}
