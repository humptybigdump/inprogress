package templatemethod;

public class IntegerBubbleSorter extends BubbleSorter {
	
	private int[] array=new int[]{};
	/**
	 * Sort array in ascending order.
	 * @param array
	 */
	public void sortAscending(int[] array) {
		this.array = array;
		
		sortAscending();
	}

	/**
	 * @return 	the length of the array
	 */
	@Override
  protected int getLength(){
  	return array.length;
  }

	/**
	 * Compare two elements of array.
	 * @param index1
	 * @param index2
	 * @return 	Positive value iff array[index1] is greater than array[index2],
	 * 			Negative value iff array[index1] is smaller than array[index2],
	 * 			Zero iff both elements are the same.
	 */
	@Override
	protected int compareElements(int index1, int index2) {
		return array[index1] - array[index2];
	}

	/**
	 * Swap elements of array.
	 * @param index1
	 * @param index2
	 */
	@Override
	protected void swapElements(int index1, int index2) {
		int temp = array[index1];
		array[index1] = array[index2];
		array[index2] = temp;
	}
	
	/**
	 * Test template method approach.
	 * @param args
	 */
	public static void main(String args[]) {
		int[] testArray = {3, 4, 1};
		new IntegerBubbleSorter().sortAscending(testArray);
		for (int i : testArray) System.out.println(i);
	}
	
}
