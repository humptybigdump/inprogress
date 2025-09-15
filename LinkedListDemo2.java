package edu.kit.aifb.proksy.trainingstagebuch.controller;

import java.util.LinkedList;

/**
 * Musterloesung
 *
 * @version 1.0
 * @author ProkSy-Team
 */
public class LinkedListDemo2 {
	/**
	 * Hauptprogramm.
	 *
	 * @param args Kommandozeilenparameter (hier nicht verwendet).
	 */
	public static void main(String[] args) {
		LinkedList<String> list = null;
		String sA = "Anna";
		String sB = "Berta";
		String sC = "Carla";

		list = new LinkedList<String>();
		System.out.println(list);

		list.addLast(sA);
		System.out.println(list);
		list.addLast(sB);
		System.out.println(list);
		list.addLast(sC);
		System.out.println(list);

		list.addFirst(sC);
		System.out.println(list);
		list.addFirst(sB);
		System.out.println(list);
		list.addFirst(sA);
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
