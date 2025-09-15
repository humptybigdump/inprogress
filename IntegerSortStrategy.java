package strategy;

public class IntegerSortStrategy implements SortStrategy {

	private int[] array;
	
	public IntegerSortStrategy(int[] testArray) {
		this.array = testArray;
	}

	public int compareElements(int index1, int index2) {
		return (array[index1] - array[index2]);
	}

	public void swapElements(int index1, int index2) {
		int temp = array[index1];
		array[index1] = array[index2];
		array[index2] = temp;

	}

	public int getLength() {
		return array.length;
	}

}
