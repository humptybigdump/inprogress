package edu.kit.tm.eir;

import java.util.ArrayList;
import java.util.List;

/**
 * Class to compute (2^n - 1, 2^n - n - 1) Hamming codes up to n=32.
 * <p>
 * Some remarks:<br>
 * The Hamming encoding itself is clearly defined, however, this is not true for
 * the encoding of the data. There are several possibilities how to map the
 * input data bits to the data bits within a Hamming code word, and how to
 * concatenate the code words themselves. Thus, the following notion is defined
 * for this implementation:<br>
 * <ul>
 * <li>Input bits are fed into the Hamming encoder in the following order: Least
 * significant bit first, (2^0, 2^1, 2^2 ... 2^7) at increasing byte order, as
 * an continous bit stream. The Hamming encoding is NOT interrupted at input
 * data byte boundaries. An input data byte may be encoded into several Hamming
 * code words!
 * <li>Hamming code words stored in machine bit order (most significant bit
 * first, 2^7, 2^6 ... 2^0), at increasing byte order. Thus, even tough the
 * typical textbook example of an (15,11) Hamming code word looks like
 * {@code pp0p123p456789A} for data bits {@code 0-A} and parity bits {@code p},
 * it is stored as {@code p321p0pp, _A987654}. The bit ordering in textbook
 * examples is NOT the machine bit order which is used here.
 * <li>Hamming code words are zero-padded to byte boundaries, thus, the most
 * significant bit of the last byte is zero ({@code _ in the previous example}.
 * <li>The data after Hamming decoding may contain an arbitrary number of
 * trailing zero bits for padding purposes.
 * </ul>
 */
public class Hamming implements ErrorCorrectingCode {

	private final int codebits;
	private final int databits;
	private final int paddingbits;
	private final int wordBytes;
	
	/**
	 * Creates a new Hamming instance for (2^n - 1, 2^n - n - 1) Hamming codes.
	 * 
	 * @param codebits
	 *            the size of the Hamming code in bits. Must satisfy the
	 *            conditions {@code codebits = 2^n - 1} and {@code codebits > 2}.
	 * @throws IllegalArgumentException
	 *             if {@codebits != 2^n - 1} or {@codebits < 3}
	 */
	public Hamming(final int codebits) {
		if (codebits < 3 || Integer.bitCount(codebits + 1) != 1) {
			throw new IllegalArgumentException("Number of codebits violates hamming constraints, must be a power of two minus one");
		}
		
		// Integer.numberOfTrailingZeros equals log_2 if only one bit is set
		this.codebits = codebits;
		this.databits = codebits - Integer.numberOfTrailingZeros(codebits + 1);
		this.paddingbits = ((codebits + 7) / 8) * 8 - codebits;
		this.wordBytes = (codebits + paddingbits) / 8;
		
		if (codebits - databits > 32) {
			throw new IllegalArgumentException("This implementation does not support hamming codes with more than 32 parity bits");
		}
	}
	
	/**
	 * Returns bit {@code index} of {@code bytes}, or zero if the bit index is
	 * out of bounds. The {@code index} counts the bits starting with the least 
	 * significant bit first, and in increasing byte order.
	 *  
	 * @param bytes the byte vector to address
	 * @param index the bit index, starting at bit 0
	 * @return {@code 0} if the bit is not set, else {@code 1}
	 */
	private byte getBitOrZero(final List<Byte> bytes, final int index) {
		final int byteInd = index / 8;
		final int bitInd = index % 8;
		
		// quite simple implementation: get the byte, shift the desired bit
		// to the rightmost (least significant) bit and mask all other bits away
		
		byte result = byteInd < bytes.size() ? bytes.get(byteInd) : 0;
		
		result >>>= bitInd;
		result &= 0x1;
		
		return result;
	}
	
	/**
	 * Copies the least significant bit of {@code bit} to {@code index} of
	 * {@code bytes}. The {@code index} counts the bits starting with the least
	 * significant bit first, and in increasing byte order.
	 * 
	 * @param bytes
	 *            the byte vector to address
	 * @param index
	 *            the bit index, starting at bit 0. Must satisfy
	 *            {@code index / 8 < bytes.size()}
	 * @param bit
	 *            the bit to copy, only the least significant bit is considered
	 */
	private void setBit(final List<Byte> bytes, final int index, final byte bit) {
		final int byteInd = index / 8;
		final int bitInd = index % 8;
		
		assert byteInd < bytes.size();
		
		// similar to getBitOrZero: get the byte, but this time, clear the 
		// destination bit by computing a binary and with a mask preserving all
		// other bits, and copy the bit to this location using a binary or
		
		byte value = bytes.get(byteInd);
		
		value &= ~(1 << bitInd); // clear previous value
		value |= (0x1 & bit) << bitInd; // set new value
		
		bytes.set(byteInd, value);
	}
	
	/**
	 * Prepares the passed {@code data} vector by extending and padding it
	 * according to the Hamming encoding scheme. This especially includes moving
	 * data bits around to make room for parity bits at the required positions.
	 * The parity bits themselves need to be computed in a second step by
	 * {@code #compute(List<Byte>)}.
	 * 
	 * @param data
	 *            the input (and output) data vector to be prepared for the
	 *            computation of the Hamming encoding
	 */
	@Override
	public void initialize(List<Byte> data) {
		final int words = (data.size() * 8 + databits - 1) / databits;
		
		// write the padded code words into a new buffer first, doing this task
		// inline would be much more complicated ...
		final List<Byte> buf = new ArrayList<Byte>(words);
		
		int databitIndex = 0;
		
		// prepare the code words word by word
		for (int word = 0; word < words; word++) {
			// add enough bytes for the new word to the buffer
			for (int i = 0; i < wordBytes; i++) {
				buf.add((byte) 0);
			}
			
			// offset within the buffer for the current code word, in bits
			final int dataOffset = word * (codebits + paddingbits);
			
			// loop over all bits in the code word and copy data bits to all
			// non-parity bits in the code word
			for (int bit = 0; bit < codebits; bit++) {
				if (Integer.bitCount(bit + 1) != 1) { // not a parity bit
					setBit(buf, dataOffset + bit, getBitOrZero(data, databitIndex++));
				}
			}
		}
		
		// write the buffer to the input vector
		data.clear();
		data.addAll(buf);
	}

	/**
	 * Computes the Hamming parity bits in a vector previously prepared by
	 * {@link #initialize(List<Byte>)}. It will fail, produce undefined results
	 * and/or corrupt your data if the {@code data} vector was not initialized
	 * properly.
	 * 
	 * @param data
	 *            the input/output vector for which the Hamming code should be
	 *            computed
	 */
	@Override
	public void compute(List<Byte> data) {
		if (data.size() % wordBytes != 0) { 
			throw new IllegalArgumentException("input data vector has not been initialized properly");
		}
		
		final int words = data.size() / wordBytes;
		
		// compute parity bits word by word
		for (int word = 0; word < words; word++) {
			// offset within the data vector for the current code word, in bits
			final int dataOffset = word * (codebits + paddingbits);
			
			// loop over all parity bits and compute them according to the Hamming scheme
			for (int bit = 0; bit < codebits; bit++) {
				if (Integer.bitCount(bit + 1) == 1) { // a parity bit
					byte parity = 0; // variable keeping the computed parity bit
					
					// bit + 1 = 2^0, 2^1 .. 2^(codebits-databits) -> parity bit index
					for (int pBit = bit + 1; pBit < codebits; pBit++) {
						// parity bit "bit + 1" includes all subsequent bits which
						// have the according bit set in their index.
						// Note: The Hamming indexing scheme starts at 1!
						if (((pBit + 1) & (bit + 1)) > 0) {
							parity ^= getBitOrZero(data, dataOffset + pBit);
						}
					}
					
					setBit(data, dataOffset + bit, parity);
				}
			}
		}
	}

	/**
	 * Undoes the Hamming encoding of {@code data} and tries to correct bit
	 * errors during this process. Additional zero bits may be remain afterwards
	 * as result of the padding applied to map the input data to the Hamming
	 * code size. This method will fail, produce undefined results and/or
	 * corrupt your data if the {@code data} vector was not initialized
	 * properly.
	 * 
	 * @param data
	 *            the Hamming encoded input vector to decode and verify
	 * @return always {@code true} since the Hamming decoder is unable to tell
	 *         if all bit errors were corrected
	 */
	@Override
	public boolean verify(List<Byte> data) {
		if (data.size() % wordBytes != 0) { 
			throw new IllegalArgumentException("input data vector has not been initialized properly");
		}
		
		final int words = data.size() / wordBytes;
		// write the decoded data into a new buffer first, doing this task
		// inline would be much more complicated ...
		final List<Byte> buf = new ArrayList<Byte>(words * databits);
		
		int databitIndex = 0;
		
		// loop over all code words to verify parity, correct errors and extract
		// the encoded information
		for (int word = 0; word < words; word++) {
			// offset within the data vector for the current code word, in bits
			final int dataOffset = word * (codebits + paddingbits);

			// parity information, both the newly computed one and the old one
			// extracted from the code word
			int newParityVect = 0;
			int oldParityVect = 0;
			
			// loop over all parity bits and extract/compute parity information
			for (int bit = 0; bit < codebits; bit++) {
				if (Integer.bitCount(bit + 1) == 1) { // a parity bit
					byte parity = 0; // variable keeping the computed parity bit
					
					// bit + 1 = 2^0, 2^1 .. 2^(codebits-databits) -> parity bit index
					for (int pBit = bit + 1; pBit < codebits; pBit++) {
						// parity bit "bit + 1" includes all subsequent bits which
						// have the according bit set in their index.
						// Note: The Hamming indexing scheme starts at 1!
						if (((pBit + 1) & (bit + 1)) > 0) {
							parity ^= getBitOrZero(data, dataOffset + pBit);
						}
					}
					
					// extract old parity bit from code word and store it in 
					// machine bit order (least significant bit first)
					oldParityVect |= getBitOrZero(data, dataOffset + bit) << Integer.numberOfTrailingZeros(bit + 1);
					// do the same with the newly computed parity bit
					newParityVect |= parity << Integer.numberOfTrailingZeros(bit + 1);
				}
			}
			
			// verify parity and correct bit errors
			
			// compute the index (starting at one) of the flipped bit
			final int errBit = newParityVect ^ oldParityVect;
			
			if (errBit > codebits) {
				// should not be possible normally?!
				throw new IllegalStateException("Something went wrong, computed an errorneous bit which is out of bounds");
			}
			
			// errBit indicates the index of the flipped bit, or zero if there
			// is no error to correct. Go ahead an fix the error, if neccessary.
			if (errBit > 0) { // need to flip a bit
				byte b = getBitOrZero(data, dataOffset + errBit - 1);
				
				b ^= 0x1; // XOR flips the bit
				
				setBit(data, dataOffset + errBit - 1, b);
			}
			
			// decode the Hamming code and restore original data stream
			
			// loop over code bits and extract all data (non-parity) bits
			for (int bit = 0; bit < codebits; bit++) {
				if (Integer.bitCount(bit + 1) != 1) { // not a parity bit
					if (databitIndex % 8 == 0) {
						buf.add((byte) 0);
					}
					
					setBit(buf, databitIndex++, getBitOrZero(data, dataOffset + bit));
				}
			}
		}
		
		// write the buffer to the input vector
		data.clear();
		data.addAll(buf);

		// Hamming can not tell if something went wrong after correcting an bit error
		return true; 
	}

}
