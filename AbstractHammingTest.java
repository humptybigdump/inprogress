package edu.kit.tm.eir;

import static org.junit.Assert.assertArrayEquals;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

import java.util.List;

public abstract class AbstractHammingTest {

	static Byte[] testVector1 = new Byte[] {
		(byte) 0xff, (byte) 0xff
	};
	
	static Byte[] testVector2 = new Byte[] {
		(byte) 0xf4, (byte) 0x4f
	};
	
	// one bit error per two bytes, correctable for (7,4) and (15,11)
	static Byte[] xorMask1 = new Byte[] {
		(byte) 0b10000000, (byte) 0b00000000, (byte) 0b00000000, (byte) 0b00000001
	};
	
	// one bit error per byte, correctable for (7,4) but not for (15,11)
	static Byte[] xorMask2 = new Byte[] {
		(byte) 0b00001000, (byte) 0b00010000, (byte) 0b00100000, (byte) 0b00000010
	};
	
	// two bit errors per byte, not correctable for (7,4) and (15,11)
	static Byte[] xorMask3 = new Byte[] {
		(byte) 0b01001000, (byte) 0b00010010, (byte) 0b00100100, (byte) 0b00001001
	};
	
	void runInitialize(final Hamming hamming, final List<Byte> vector,
			final Byte[] expected, final int vecNum) {
		hamming.initialize(vector);
		
		final Byte[] vector1Result = vector.toArray(new Byte[0]);
		
		assertArrayEquals("Testing for proper initialization with vector "
				+ vecNum, expected, vector1Result);
	}
	
	void runHamming(final Hamming hamming, final List<Byte> vector,
			final Byte[] expected, final int vecNum) {
		hamming.initialize(vector);
		hamming.compute(vector);
		
		final Byte[] vectorResult = vector.toArray(new Byte[0]);
		
		assertArrayEquals("Testing for proper hamming computation with vector "
				+ vecNum, expected, vectorResult);
	}
	
	void runVerify(final Hamming hamming, final List<Byte> vector,
			final Byte[] xorMask, final Byte[] expected, final int vecNum) {
		hamming.initialize(vector);
		hamming.compute(vector);
		
		for (int i = 0; i < vector.size() && i < xorMask.length; i++) {
			vector.set(i, (byte) (vector.get(i) ^ xorMask[i]));
		}
		
		assertTrue("Testing for true as return value of verify()", 
				hamming.verify(vector));
		
		assertTrue("Testing for proper vector size with vector " + vecNum,
				vector.size() >= expected.length);
	
		for (int i = expected.length; i < vector.size(); i++) {
			assertEquals("Testing for zero padding bits with vector " + vecNum
					+ ", index " + i, 0, (byte) vector.get(i));
		}
	
		final Byte[] vectorResult = vector.subList(0, expected.length).toArray(new Byte[0]);
	
		assertArrayEquals(
				"Testing for proper hamming verification with vector " + vecNum,
				expected, vectorResult);
	}

}
