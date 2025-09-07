package edu.kit.tm.eir;

import static org.junit.Assert.*;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

import org.junit.Test;

public class TestCrc16 {

	private static final Byte[] modemData = new Byte[] { 
			//(byte) 0b01111110, (byte) 0b01111110, (byte) 0b01111110, Start of Frame
			(byte) 0b01001000,
			(byte) 0b10010011, (byte) 0b00000001, (byte) 0b00000001,
			(byte) 0b00000001, (byte) 0b10010000, (byte) 0b10101101,
			(byte) 0b01000000, (byte) 0b00000000, (byte) 0b00101001,
			(byte) 0b10000001, (byte) 0b11000001, (byte) 0b11000010,
			(byte) 0b11100010, (byte) 0b00100011, 
			(byte) 0b11100100, (byte) 0b00110111, // FCS
			// 0xE4 0x37, bit-reversed: 0x27 0xEC
			//(byte) 0b01111110, (byte) 0b01111110 End of Frame
	};
	
	private static final Byte[] testVector2 = new Byte[] { 
		'1', '2', '3', '4', '5', '6', '7', '8', '9',
		(byte) 0xD6, (byte) 0x4E, // FCS
	};
	
	@Test
	public void testInitialize() {
		final Crc16 crc = new Crc16();
		
		final List<Byte> list = new ArrayList<Byte>(Arrays.asList(modemData).subList(0, modemData.length - 2));
		
		crc.initialize(list);
		
		assertEquals("Testing for proper length of appended CRC", modemData.length, list.size());
		assertEquals("Testing for proper initialization of CRC", 0x0,
				0xffff & ((list.get(list.size() - 2) << 8) 
						| list.get(list.size() - 1)));
	}
	
	@Test
	public void testEmptyChecksum() {
		final Crc16 crc = new Crc16();
		
		final List<Byte> list = new ArrayList<Byte>();
		
		crc.initialize(list);
		crc.compute(list);
		
		assertEquals("Testing for proper computation of CRC", 0x0000,
				0xffff & ((list.get(list.size() - 2) << 8) 
						| list.get(list.size() - 1)));
	}
	
	@Test
	public void testModemChecksum() {
		runCompute(modemData);
	}
	
	@Test
	public void testVector2Checksum() {
		runCompute(testVector2);
	}

	private void runCompute(final Byte[] data) {
		final Crc16 crc = new Crc16();
		
		final List<Byte> list = new ArrayList<Byte>(Arrays.asList(data).subList(0, data.length - 2));
		
		crc.initialize(list);
		crc.compute(list);
		
		assertEquals("Testing for proper computation of CRC", 
				0xffff & ((data[data.length - 2] << 8) | data[data.length - 1]),
				0xffff & ((list.get(list.size() - 2) << 8) 
						| list.get(list.size() - 1)));
	}
	
	@Test
	public void testModemVerify() {
		runVerify(modemData);
	}
	
	@Test
	public void testVector2Verify() {
		runVerify(testVector2);
	}

	private void runVerify(final Byte[] data) {
		final Crc16 crc = new Crc16();
		
		final List<Byte> list = new ArrayList<Byte>(Arrays.asList(data));
		final int dataSize = list.size() - 2;
		
		assertTrue("Testing for proper verification of CRC", crc.verify(list));
		assertEquals("Testing for stripped checksum", dataSize, list.size());
	}
	
	@Test
	public void testBadInputVerify() {
		final Crc16 crc = new Crc16();
		
		assertFalse("Testing for proper detection of wrong input",
				crc.verify(new ArrayList<Byte>(
						Arrays.asList((byte) 0x23, (byte) 0x42, (byte) 0x47, 
								(byte) 0x11, (byte) 0x08, (byte) 0x15))));
	}
	
	@Test
	public void testEmptyInputVerify() {
		final Crc16 crc = new Crc16();
		
		final List<Byte> list = Collections.emptyList();
		
		assertFalse("Testing for proper detection of wrong input", crc.verify(list));
	}

}
