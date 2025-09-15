/*
 * Copyright (c) 1995, 1996 Sun Microsystems, Inc. All Rights Reserved.
 *
 * Permission to use, copy, modify, and distribute this software
 * and its documentation for NON-COMMERCIAL purposes and without
 * fee is hereby granted provided that this copyright notice
 * appears in all copies. Please refer to the file "copyright.html"
 * for further important copyright and licensing information.
 *
 * SUN MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE SUITABILITY OF
 * THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
 * TO THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
 * PARTICULAR PURPOSE, OR NON-INFRINGEMENT. SUN SHALL NOT BE LIABLE FOR
 * ANY DAMAGES SUFFERED BY LICENSEE AS A RESULT OF USING, MODIFYING OR
 * DISTRIBUTING THIS SOFTWARE OR ITS DERIVATIVES.
 */
import java.awt.*;

class FramedArea extends Panel {
    PhilosopherArea philosopherArea;

    public FramedArea(PhilAnimator controller) {
        super();

        //Set layout to one that makes its contents as big as possible.
        setLayout(new GridLayout(1,0));

	philosopherArea = new PhilosopherArea(controller);
        add(philosopherArea);
        validate();
    }

    public Insets insets() {
        return new Insets(4,4,5,5);
    }

    public void paint(Graphics g) {
        Dimension d = size();
        Color bg = getBackground();

        g.setColor(bg);
        g.draw3DRect(0, 0, d.width - 1, d.height - 1, true);
        g.draw3DRect(3, 3, d.width - 7, d.height - 7, false);
    }

    public void stopButton() {
	philosopherArea.stopPhilosophers();
	philosopherArea.createPhilosophersAndChopsticks();
	philosopherArea.repaint();
    }

    public void startButton() {
	philosopherArea.startPhilosophers();
    }
}
