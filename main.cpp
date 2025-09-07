/*
 * Copyright (c)  2024  KIT IRS-VSA 
 * Author: Vanessa Del Rio Ortiz
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:

 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.

 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
 * IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
 * DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
 * OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
 * OR OTHER DEALINGS IN THE SOFTWARE.
 */

#include "src/GPIOLed.h"
#include "src/RGBLight.h"
#include "src/ServoMotor.h"
#include "src/HexDecoder.h"
#include "ti/driverlib/dl_common.h"



/* ///////////////////////////////
* **WELCOME TO THE HARDWARE TASK**
*  //////////////////////////////
* Please read the documentation for the setup of
* - Electronics
* - Software
*/

// Function that turns an ASCII string into a vector of hexadecimal numbers
std::vector<uint8_t> asciiToHex(const std::string& asciiString) {
    std::vector<uint8_t> hexVector;
    for (char c : asciiString) {
        hexVector.push_back(static_cast<uint8_t>(c));
    }
    return hexVector;
}

int main(void)
{
    
    SYSCFG_DL_init();
    GPIOLed newLed(LEDIO_PORT,LEDIO_OUT_PIN);
    HexDecoder newDecoder(PWM_0_INST, PWM_0_INST_CLK_FREQ, LEDIO_PORT, LEDIO_OUT_PIN); 
    // The PWM_0_INST_CLK_FREQ is the clock frequency for the PWM, which is set in the system data.
    // The LEDIO_PORT and LEDIO_OUT_PIN are the GPIO port and pin for the LED output.

    // The message will be decoded by the HexDecoder class.
    std::vector<uint8_t> msg = asciiToHex("ITAT IS FUN!");

    newDecoder.decode(msg); // Decode the message using the HexDecoder class
    while (1) {
        __WFI(); // Wait for an interrupt
    }
}


