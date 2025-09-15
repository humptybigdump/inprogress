package plain;

public class IntegerBubbleSorter {
  private int[] array;

  /**
  * Sort array in ascending order.
  * @param array
  */
  public void sortAscending(int[] array) {
    this.array = array;
    if (array.length <= 1) {
      return;
    }

    for (int nextToLast = array.length - 2; nextToLast >= 0; nextToLast--) {
      for (int index = 0; index <= nextToLast; index++) {
        if (compareElements(index, index + 1) > 0)
          swapElements(index, index + 1);
      }
    }
  }

  /**
  * Compare two elements of array.
  * @param index1
  * @param index2
  * @return 	Positive value iff array[index1] is greater than array[index2],
  * 			Negative value iff array[index1] is smaller than array[index2],
  * 			Zero iff both elements are the same.
  */
  private int compareElements(int index1, int index2) {
    return array[index1] - array[index2];
  }

  /**
  * Swap elements of array.
  * @param index1
  * @param index2
  */
  private void swapElements(int index1, int index2) {
    int temp = array[index1];
    array[index1] = array[index2];
    array[index2] = temp;
  }

  /**
  * Test simple approach.
  * @param args
  */
  public static void main(String args[]) {
    int[] testArray = {3, 4, 1};
    new IntegerBubbleSorter().sortAscending(testArray);
    for (int i : testArray) System.out.println(i);
  }
}
