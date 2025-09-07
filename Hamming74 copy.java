package edu.kit.tm.eir;

import java.util.List;

public class Hamming74 extends Hamming {

	public Hamming74() {
		super(7);
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
		// TODO
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
		// TODO
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
		// TODO
		
		return false;
	}
}
