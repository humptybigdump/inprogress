import java.awt.*;
import javax.swing.*;
import java.util.List;

/**
 * @author Lukas Struppek
 * @version 1.0
 *
 */
public class Plot extends JPanel {
	private static final long serialVersionUID = 1L;
	JFrame frame;
	double[] data;
	final int p = 10;

	/**
	 * @param data Liste mit Aktienkursen
	 * 
	 *             Erzeugt ein neues Frame, auf welchem der Verlauf des Aktienkurses
	 *             dargestellt ist
	 */
	public Plot(List<Double> data) {
		this.data = new double[data.size()];
		for (int i = 0; i < data.size(); i++)
			this.data[i] = data.get(i).doubleValue();

		frame = new JFrame();
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.setTitle("Aktienkurs Prognose");
		frame.add(this);
		frame.setSize(400, 400);
		frame.setVisible(true);

	}

	/**
	 * Methode zur Darstellung der Elemente in der Liste
	 */
	protected void paintComponent(Graphics g) {
		super.paintComponent(g);
		Graphics2D graphics = (Graphics2D) g;
		int breite = getWidth();
		int hoehe = getHeight();
		graphics.drawLine(p, p, p, hoehe - p);
		graphics.drawLine(p, hoehe - p, breite - p, hoehe - p);
		double xSkala = (breite - 2 * p) / (data.length + 1);
		double maxWert = 100.0;
		double ySkala = (hoehe - 2 * p) / maxWert;

		int x0 = p;
		int y0 = hoehe - p;
		graphics.setPaint(Color.BLUE);

		for (int j = 0; j < data.length; j++) {
			int x = x0 + (int) (xSkala * (j + 1));
			int y = y0 - (int) (ySkala * data[j]);
			graphics.fillOval(x - 2, y - 2, 4, 4);
		}
	}
}