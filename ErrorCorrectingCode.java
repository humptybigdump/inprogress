package edu.kit.tm.eir;

import java.util.List;

/**
 * An interface for an error detecting or correcting code.
 * 
 * General usage: Some codes need to rearrange the memory layout of the data 
 * which should be protected. Thus, {@link #initialize(List<Byte>)} must be 
 * called first before the code can be computed with {@link #compute(List<Byte>)}.
 * To verify a protected data vector, {@link #verify(List<Byte>)} may be used. 
 */
public interface ErrorCorrectingCode {

	/**
	 * Initializes the passed data vector to carry the error correcting or
	 * detecting code computed by {@link #compute(List<Byte>)}. This call may
	 * already apply arbitrary but reversible modifications to the data vector.
	 * 
	 * @param data
	 *            the data vector to modify
	 */
	public void initialize(final List<Byte> data);
	
	/**
	 * Computes the error correcting or detecting code of the passed data vector
	 * and embeds it accordingly. {@link #initialize(List<Byte>)} must be called
	 * first to prepare the memory layout, the result may be both wrong and 
	 * undefined and the data might be corrupted otherwise.
	 * 
	 * @param data
	 *            the data vector for which the error correcting or detecting
	 *            code will be computed
	 */
	public void compute(final List<Byte> data);
	
	/**
	 * Verifies the error correcting or detecting code (computed by {@link
	 * #compute(List<Byte>)}) in the passed data vector. If the code is error
	 * correcting, it will try to correct those errors and report back its 
	 * success. This method will also try to undo all changes applied
	 * by {@link #initialize(List<Byte>)} and {@link #compute(List<Byte>)}.
	 * Thus, if it returns {@code true}, data will contain the unaltered, 
	 * original data plus maybe additional (zero) padding bytes.
	 * 
	 * @param data
	 *            the data vector to verifiy
	 * @return {@code true} if the data vector was corrected and verified to be
	 *         error free, else {@code false}
	 */
	public boolean verify(final List<Byte> data);
	
}
