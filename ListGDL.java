package edu.kit.aifb.proksy.genericdoublylinkedlist;

/**
 * Musterloesung
 *
 * @version 1.0
 * @author ProkSy-Team
 *
 * @param <T> Typ der Elemente, die in der Liste gespeichert werden sollen.
 */
public class ListGDL<T>
{
    private ElementDL<T> head;
    private ElementDL<T> tail;
    
    /**
     * Konstruktor.
     */
    public ListGDL ()
    {
        head = new ElementDL<T>();
        head.setObject(null);
        tail = new ElementDL<T>();
        tail.setObject(null);
        head.setPredecessor(null);
        head.setSuccessor(tail);
        tail.setPredecessor(head);
        tail.setSuccessor(null);
    }
    
    /**
     * Kommando, das Objekt objekt am Anfang der Liste anzufuegen.
     *
     * @param objekt Objekt, das am Anfang der Liste angefuegt werden soll.
     */
    public void insertFirst (T objekt)
    {
    	ElementDL<T> actual = new ElementDL<T>();
        actual.setObject(objekt);
        actual.setPredecessor(head);
        actual.setSuccessor(head.getSuccessor());
        head.setSuccessor(actual);
        actual.getSuccessor().setPredecessor(actual);
    }
    
    /**
     * Kommando, das Objekt objekt am Ende der Liste anzufuegen.
     *
     * @param objekt Objekt, das am Ende der Liste angefuegt werden soll.
     */
    public void insertLast(T objekt)
    {
    	ElementDL<T> actual = new ElementDL<T>();
        actual.setObject(objekt);
        actual.setPredecessor(tail.getPredecessor());
        actual.setSuccessor(tail);
        tail.setPredecessor(actual);
        actual.getPredecessor().setSuccessor(actual);
    }
    
    /**
     * Kommando, das erste (nicht alle!) Vorkommen des Objekts objekt aus der Liste zu entfernen.
     *
     * @param objekt Objekt, dessen erstes Vorkommen aus der Liste entfernt werden soll.
     */
    public void remove (T objekt)
    {
        boolean objektFound = false;
        ElementDL<T> actual = head.getSuccessor();
        while (actual != tail && !objektFound)
        {
            if(actual.getObject().equals(objekt))
            {
                objektFound = true;
                actual.getPredecessor().setSuccessor(actual.getSuccessor());
                actual.getSuccessor().setPredecessor(actual.getPredecessor());
            }
            actual = actual.getSuccessor();
        }
    }
    
    /**
     * Abfrage einer textuellen Repraesentation der Liste mit den gespeicherten Objekten.
     *
     * @return Textuelle Repraesentation der Liste in der Form <A, B, C, D>.
     */
    public String toString ()
    {
        String result = "[";
        ElementDL<T> actual = head.getSuccessor();
        while (actual != tail)
        {
            result = result + actual.getObject().toString();
            actual = actual.getSuccessor();
            if (actual != tail)
            {
                result = result + ", ";
            }
        }
        result = result + "]";
        return result;
    } 
}
    
