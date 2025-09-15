package edu.kit.aifb.proksy.genericdoublylinkedlist;

/**
 * Musterloesung
 *
 * @version 1.0
 * @author ProkSy-Team
 */
public class ListGDLDemo1
{
    /**
     * Hauptprogramm.
     *
     * @param args Kommandozeilenparameter (hier nicht verwendet).
     */
    public static void main (String [] args)
    {
        ListGDL<Integer> list = null;
        
        list = new ListGDL<Integer>();
        System.out.println(list);
        
        list.insertLast(1);
        System.out.println(list);
        list.insertLast(2);
        System.out.println(list);
        list.insertLast(3);
        System.out.println(list);
        
        list.insertFirst(3);
        System.out.println(list);
        list.insertFirst(2);
        System.out.println(list);
        list.insertFirst(1);
        System.out.println(list);
        
        list.remove(3);
        System.out.println(list);
        list.remove(3);
        System.out.println(list);
        list.remove(2);
        System.out.println(list);
        list.remove(2);
        System.out.println(list);
        list.remove(1);
        System.out.println(list);
        list.remove(1);
        System.out.println(list);
    }
}
