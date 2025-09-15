package edu.kit.aifb.proksy.rMIEcho.LokaleProgrammierung;

/**
 *
 * @author ProkSy-Team
 * @version 1.0
 * 
 */
public class EchoServer
{
    private EchoObject eo;
    
    public EchoServer ()
    {
        this.eo = new EchoObject();
        System.out.println("Der Server ist aktiv");
    }
    
    public EchoObject getEchoObject ()
    {
        EchoObject result;
        result = eo;
        return result;
    }
}
