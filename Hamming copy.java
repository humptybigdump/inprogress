package edu.kit.tm.eir;

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
public abstract class Hamming implements ErrorCorrectingCode {
	
	final int codebits;
	
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
		this.codebits = codebits;
	}

}
