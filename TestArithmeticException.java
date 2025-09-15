//import java.lang.ArithmeticException;
class TestArithmeticException {
	public static void main(String[] args){
	for (int i = -2; i <= 2; i++)
		try {
			System.out.println (1/i);
		}	
		catch (ArithmeticException e) {
			System.out.println ("Ausnahme abgefangen!");
		}
	}
}

