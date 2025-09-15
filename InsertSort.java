/*
 * @(#)InsertSort.java 
 *
 */

/**
 * A insert sort demonstration algorithm
 * SortAlgorithm.java
 *
 * @author Daniel Merkle
 * @version 	1.0
 */
class InsertSort extends SortAlgorithm {
  
  void sort(int a[]) throws Exception {
    int j;
    int key;
    
    for (int i = 1; i < a.length; i++)
      {
	key=a[i];
	j=i;
	while( j>0 && a[j-1] > key ) {
	  a[j] = a[j-1]; 
	  j--;
	  pause(i,j);
	}
	a[j] = key;
      }
  }
}
