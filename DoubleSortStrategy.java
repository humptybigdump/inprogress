package strategy;

public class DoubleSortStrategy implements SortStrategy {

	private double[] array;
	
	public DoubleSortStrategy(double[] testArray) {
		this.array = testArray;
	}

	public int compareElements(int index1, int index2) {
		return (int)(array[index1] - array[index2]);
	}

	public void swapElements(int index1, int index2) {
		double temp = array[index1];
		array[index1] = array[index2];
		array[index2] = temp;

	}

	public int getLength() {
		return array.length;
	}

}
