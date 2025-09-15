package edu.kit.aifb.proksy.metzgerkleinstadt;

/**
 * @version 1.0
 * @author ProkSy-Team
 */
public class Metzger {
	public String name;
	public Wursttypen spezialitaet;

	/**
	 * @param name
	 * @param spezialitaet
	 */
	public Metzger(String name, Wursttypen spezialitaet) {
		this.name = name;
		this.spezialitaet = spezialitaet;
	}
	
	/* (non-Javadoc)
	 * @see java.lang.Object#toString()
	 */
	public String toString()
	{
		return "Die Spezialitaet von Metzger " + name + " ist " + spezialitaet + ".";
	}

}
