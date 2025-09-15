package edu.kit.aifb.proksy.trainingstagebuch.controller;

import java.util.LinkedList;

/**
 * Musterloesung
 *
 * @version 1.0
 * @author ProkSy-Team
 */
public class LinkedListDemo1 {
	/**
	 * Hauptprogramm.
	 *
	 * @param args Kommandozeilenparameter (hier nicht verwendet).
	 */
	public static void main(String[] args) {
		LinkedList<Integer> list = null;

		list = new LinkedList<Integer>();
		System.out.println(list);

		list.addLast(1);
		System.out.println(list);
		list.addLast(2);
		System.out.println(list);
		list.addLast(3);
		System.out.println(list);

		list.addFirst(3);
		System.out.println(list);
		list.addFirst(2);
		System.out.println(list);
		list.addFirst(1);
		System.out.println(list);

		list.remove(list.indexOf(3));
		System.out.println(list);
		list.remove(list.indexOf(3));
		System.out.println(list);
		list.remove(list.indexOf(2));
		System.out.println(list);
		list.remove(list.indexOf(2));
		System.out.println(list);
		list.remove(list.indexOf(1));
		System.out.println(list);
		list.remove(list.indexOf(1));
		System.out.println(list);
	}
}
