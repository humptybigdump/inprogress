package strategy;

public class BubbleSorter {

	private SortStrategy sortStrategy=null;

	public BubbleSorter(SortStrategy sortHandle) {
		this.sortStrategy = sortHandle;
	}
	
	public BubbleSorter() {

	}
	
  public void setSortStrategy(SortStrategy sortHandle){
    this.sortStrategy=sortHandle;
  }


	/**
	 * Sort using bubblesort in ascending order.
	 */
	public void sortAscending() {
	  if (sortStrategy == null)
	    return;
	    
		if (sortStrategy.getLength() <= 1) {
			return;
		}
		
		for (int nextToLast = sortStrategy.getLength() - 2; nextToLast >= 0; nextToLast--) {
			for (int index = 0; index <= nextToLast; index++) {
				if (sortStrategy.compareElements(index, index + 1) > 0)
					sortStrategy.swapElements(index, index + 1);
			}
		}
	}

	public static void main(String args[]) {
		double[] testArray = {3, 4, 1};
		new BubbleSorter(new DoubleSortStrategy(testArray)).sortAscending();
		for (double i : testArray) System.out.println(i);

		int[] testArray2 = {3, 4, 1};
		new BubbleSorter(new IntegerSortStrategy(testArray2)).sortAscending();
		for (int i : testArray2) System.out.println(i);
	}

}
