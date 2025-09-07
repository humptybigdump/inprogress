package edu.kit.tm.eir;

import java.util.List;

/**
 * Class to compute or verify an inverted CRC-16 with the polynomial 
 * x^16 + x^12 + x^5 + 1 and an initial CRC value/prefix of 0x84cf. 
 * This is the CRC-16-CCITT variant which was used for example in dialup modems.
 * <p>
 * There are several ways how a CRC checksum can be computed. Thus, the following
 * notion is defined for this implementation:<br>
 * <ul>
 * <li>Input bits are processed in the following order: Most significant bit
 * first (2^7, 2^6, 2^5 ... 2^0, thus: machine bit order), at increasing byte
 * order, as continous bit stream which is consumed by the CRC algorithm. It is
 * possible to process the input in chunks of single or multiple bytes. However,
 * the bit ordering needs to be preserved.
 * <li>The initial CRC value is 0x84cf. This can either be accomplished by
 * storing this value in the virtual "shift-register", or by prepending it to
 * the input data vector.
 * <li>As last step of the computation, the CRC is inverted (bitwise!) before
 * storing it.
 * <li>The CRC is stored in machine bit order, most significant byte first.
 * </ul>
 */
public class Crc16 implements ErrorCorrectingCode {

	/**
	 * Initializes the passed data vector to carry the checksum computed by
	 * {@link #compute(List<Byte>)} by appending more bytes.
	 * 
	 * @param data
	 *            the data vector to modify
	 */
	@Override
	public void initialize(final List<Byte> data) {
		// append CRC, initialized with 0x0
		data.add((byte) 0x0);
		data.add((byte) 0x0);
	}
	
	/**
	 * Computes the CRC-16 checksum of the passed data vector and stores it at
	 * the end. {@link #initialize(List<Byte>)} must be called first, the result
	 * will be both wrong and undefined and the data will be corrupted.
	 * 
	 * @param data
	 *            the data vector of which the CRC-16 will be computed
	 */
	@Override
	public void compute(final List<Byte> data) {
		if (data.size() < 2) {
			throw new IllegalArgumentException("data list must be initialized first.");
		}
		
		final int fcs = doCompute(data);
			
		// store FCS in frame
		data.set(data.size() - 2, (byte) (0xff & (fcs >>> 8)));
		data.set(data.size() - 1, (byte) (0xff & fcs));
	}

	private int doCompute(final List<Byte> data) {
		// CRC-16-CCITT polynomial
		// x^16 + x^12 + x^5 + 1
		// 1 0001 0000 0010 0001
		// -> 0x1021
		
		final int polynomial = 0x1021;
		
		// initialize the register with 0x84cf
		// (the modem standard ITU-T V.8bis specifies 0xffff, but that does not work)
		int fcs = 0x84cf;
		
		for (int b : data) {
			// simplifies the transfer of the MSB into the shift register
			b = 0xff & reverseBits((byte) b); // bit order is reversed now: 2^0 .. 2^7
			
			for (int i = 0; i < 8; i++) {
				// XOR operation depends on OLD MSB, compute mask now
				final int mask = (fcs & 0x8000) != 0 ? polynomial : 0x0;
				// shift new MSB of input byte to LSB of register
				fcs = (fcs << 1) | (b & 0x1);
				b >>>= 1; // prepare next bit for next round
				// perform XOR operation
				fcs ^= mask;
			}
		}
		
		// FCS is inverted (one's complement)
		fcs = ~fcs;
		
		return 0xffff & fcs;
	}
	
	private byte reverseBits(byte in) {
		byte out = 0;
		
		for (int i = 0; i < 8; i++) {
			out <<= 1;
			out |= in & 0x1;
			in >>>= 1;
		}
		
		return out;
	}
	
	/**
	 * Verifies the checksum (computed by {@link #compute(List<Byte>)}) in the
	 * passed data vector and strips the CRC checksum from it.
	 * 
	 * @param data
	 *            the data vector to verifiy
	 * @return {@code true} if the checksum is valid, else {@code false}
	 */
	@Override
	public boolean verify(final List<Byte> data) {
		if (data.size() < 2) {
			return false;
		}
		
		final int fcs = doCompute(data);
		
		// strip checksum
		data.remove(data.size() - 1);
		data.remove(data.size() - 1);
		
		return fcs == 0; // should sum up to 0 after verification
	}

}
