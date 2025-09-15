package edu.kit.aifb.proksy.genericdoublylinkedlist;

/**
 * Musterloesung
 * Diese generische Klasse implementiert ein generisches Element einer Liste.
 *
 * @version 1.0
 * @author ProkSy-Team
 *
 * @param <T> Typ der Elemente, die in der Liste gespeichert werden sollen.
 */
public class ElementDL<T>
{
    private T object = null;
    private ElementDL<T> successor = null;
    private ElementDL<T> predecessor = null;
    
    /**
     * Abfrage des Vorgaengers dieses Listenelements.
     *
     * @return Vorgaenger dieses Listenelements.
     */
    public ElementDL<T> getPredecessor ()
    {
        ElementDL<T> result;
        result = predecessor;
        return result;
    }
    
    /**
     * Kommando, das Vorgaenger-Listenelement zu setzen.
     *
     * @param predecessor Vorgaenger dieses Listenelements.
     */
    public void setPredecessor (ElementDL<T> predecessor)
    {
        this.predecessor = predecessor;
    }
    
    /**
     * Abfrage des Nachfolgers dieses Listenelements.
     *
     * @return Nachfolger dieses Listenelements.
     */
    public ElementDL<T> getSuccessor ()
    {
        ElementDL<T> result;
        result = successor;
        return result;
    }
    
    /**
     * Kommando, das Nachfolger-Listenelement zu setzen.
     *
     * @param successor Nachfolger dieses Listenelements.
     */
    public void setSuccessor (ElementDL<T> successor)
    {
        this.successor = successor;
    }
    
    /**
     * Abfrage des in diesem Listenelement gespeicherten Objekts.
     *
     * @return Objekt, das in diesem Listenelement gespeichert ist.
     */
    public T getObject ()
    {
        T result;
        result = object;
        return result;
    }
    
    /**
     * Kommando, das in diesem Listenelement gespeicherte Objekt zu setzen.
     *
     * @param object Das Objekt, das in diesem Listenelement gespeichert werden soll.
     */
    public void setObject (T object)
    {
        this.object = object;
    }

}

