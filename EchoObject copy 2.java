package edu.kit.aifb.proksy.rMIEcho.LokaleProgrammierung;

/**
 *
 * @author ProkSy-Team
 * @version 1.0
 * 
 */
public class EchoObject implements EchoService
{
    private String response;
    
    public EchoObject ()
    {
        super();
        response = "";
    }
    
    public String getResponse ()
    {
        String result = null;
        result = response;
        System.out.println("Aufruf von getResponse()");
        return result;
    }
    
    public void request (String request)
    {
        response = request;
    }
}
