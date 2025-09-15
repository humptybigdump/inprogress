package strategy;

public interface SortStrategy {
	
	/**
	 * Compare two elements of array.
	 * @param index1
	 * @param index2
	 * @return 	Positive value iff array[index1] is greater than array[index2],
	 * 			Negative value iff array[index1] is smaller than array[index2],
	 * 			Zero iff both elements are the same.
	 */
	int compareElements(int index1, int index2);

	/**
	 * Swap elements of array.
	 * @param index1
	 * @param index2
	 */
	void swapElements(int index1, int index2);

	/**
	 * @return	Length of array being sorted.
	 */
	int getLength();
	
}
