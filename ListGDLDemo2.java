package edu.kit.aifb.proksy.genericdoublylinkedlist;

/**
 * Musterloesung
 *
 * @version 1.0
 * @author ProkSy-Team
 */
public class ListGDLDemo2
{
    /**
     * Hauptprogramm.
     *
     * @param args Kommandozeilenparameter (hier nicht verwendet).
     */
    public static void main (String [] args)
    {
        ListGDL<String> list = null;
        String sA = "Anna";
        String sB = "Berta";
        String sC = "Carla";
        
        list = new ListGDL<String>();
        System.out.println(list);
        
        list.insertLast(sA);
        System.out.println(list);
        list.insertLast(sB);
        System.out.println(list);
        list.insertLast(sC);
        System.out.println(list);
        
        list.insertFirst(sC);
        System.out.println(list);
        list.insertFirst(sB);
        System.out.println(list);
        list.insertFirst(sA);
        System.out.println(list);
        
        list.remove(sC);
        System.out.println(list);
        list.remove(sC);
        System.out.println(list);
        list.remove(sB);
        System.out.println(list);
        list.remove(sB);
        System.out.println(list);
        list.remove(sA);
        System.out.println(list);
        list.remove(sA);
        System.out.println(list);
    }
}
