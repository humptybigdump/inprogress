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

public class PhilAnimator extends java.applet.Applet {

    Button stopStartButton = new Button("start");

        // delays can go from 500 to 10,000 (they get multiplied by 100 in Philosopher
    Scrollbar grabDelaySlider = new Scrollbar(Scrollbar.HORIZONTAL, 5, 100, 0, 100);
    Label label = new Label("  500 milliseconds");

    FramedArea framedArea;

    public void init() {
        GridBagLayout gridBag = new GridBagLayout();
        GridBagConstraints c = new GridBagConstraints();

        setLayout(gridBag);

        framedArea = new FramedArea(this);
        c.fill = GridBagConstraints.BOTH;
        c.weighty = 1.0;
        c.gridwidth = GridBagConstraints.REMAINDER; //end row
        gridBag.setConstraints(framedArea, c);
        add(framedArea);

        c.fill = GridBagConstraints.HORIZONTAL;
        c.weightx = 1.0;
        c.weighty = 0.0;
        gridBag.setConstraints(stopStartButton, c);
        add(stopStartButton);


        c.gridwidth = GridBagConstraints.RELATIVE; //don't end row
        c.weightx = 1.0;
        c.weighty = 0.0;
        gridBag.setConstraints(grabDelaySlider, c);
        add(grabDelaySlider);

        c.weightx = 0.0;
        c.gridwidth = GridBagConstraints.REMAINDER; //end row
        gridBag.setConstraints(label, c);
        add(label);

        validate();
    }

    public boolean handleEvent(Event e) {
        if (e.target == stopStartButton) {
            if (stopStartButton.getLabel().equals("stop/reset")) {
                framedArea.stopButton();
                stopStartButton.setLabel("start");
            } else if (stopStartButton.getLabel().equals("start")) {
                framedArea.startButton();
                stopStartButton.setLabel("stop/reset");
            }
        } else if (e.target == grabDelaySlider) {
            label.setText(String.valueOf(100*grabDelaySlider.getValue()) + " milliseconds");
        }
        return false;
    }
}
