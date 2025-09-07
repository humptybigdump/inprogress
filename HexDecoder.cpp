#include "HexDecoder.h"
#include "src/RGBLight.h"
#include <cstdint>
#include <iostream>

/**
 * @brief Construct a new HexDecoder object
 * The following constructors are also initialized: ServoMotor, GPIOLed, RGBLed (red)
 * 
 * When creating the object, the ServoMotor object (servo) MUST be calibrated.
 * Use the points 0, 90, and 180 degrees for calibration.
 * Pay attention to whether the rotation is clockwise or counterclockwise.
 * This can change due to over-rotation!
 * Before starting calibration, a red LED is initialized. After calibration, it is turned off.
 * For successful calibration, an appropriate delay should be set, e.g., 5 seconds between
 * calibration steps. Use the private function delaySecs for this.
 *
 * @param portTimer for the PWM of ServoMotor
 * @param pwmClock for the PWM of ServoMotor
 * @param gpioPort for LED control
 * @param gpioPin for LED control
 */
HexDecoder::HexDecoder(GPTIMER_Regs *portTimer, uint32_t pwmClock, GPIO_Regs* gpioPort, uint32_t gpioPin):
    servo(portTimer,pwmClock), secondSet(gpioPort,gpioPin),rgb(uint32_t(1))
    {
        this-> rgb.enable();
        this->servo.setAngle(0.0);
        this->delaySecs(5);
        this->servo.setAngle(90.0);
        this->delaySecs(5);
        this->servo.setAngle(180.0);
        this->delaySecs(5);
        this-> rgb.disable();        
    }

/**
 * @brief Adjusts an existing delayCycles(cycles) function so that
 * the delay can be specified in seconds instead.
 * Required here: CPUCLK_FREQ and the documentation of DL_Common_delayCycles
 * @param secs Seconds 
 */
void HexDecoder::delaySecs(uint32_t secs) {
    uint32_t cycles = secs * uint32_t(CPUCLK_FREQ) + 2; // see DL_Common_delayCycles documentation
    DL_Common_delayCycles(cycles);
}

/**
 * @brief decode iterates over each element of the vector hexStrings, a hex number of 2 digits, and then
 * performs a conversion (hint: binary operations) to extract the individual digits in the element.
 * 
 * These digits are then used as iterator numbers to fetch a specific angle from LUT_Angles.
 * This angle is passed to the ServoMotor object.
 * With the help of the (printed) decoder disk, the message from hexString should be reconstructable.
 *
 * Procedure: Before iterating over the elements in hexString, set the RGBLed to blue.
 * While iterating: If a hex digit > 7 appears, turn on the LED object (secondSet).
 * After actuating the ServoMotor, set a delay.
 * After the delay, turn off the LED object.
 * Repeat this process with the second digit.
 * Between elements in hexString, implement a longer delay.
 * If an error occurs during the process, set error to false.
 * In the error loop, set the RGBLed to red and abort the program.
 * If no errors occur until the end of the iteration, set the LED to green.
 * @param hexString Reference parameter of a vector object with uint8_t objects
 */
void HexDecoder::decode(std::vector<uint8_t> &hexString){
    // Change colors: Beginning of decoding - blue
    this-> rgb.changeColor(2);
    uint8_t first = 0;
    uint8_t second = 0;
    bool error = false;
    for (uint8_t& it : hexString) {
        if (((it < 255 )|| (it ==255 ))){
            // Perform a binary operation to extract the hex digits in the first and second position
            first = (it & FIRST_CIPHER_OP) >> 4;
            second = (it & SECOND_CIPHER_OP);
            if (first < LUT_VALUES.at(15) || first == LUT_VALUES.at(15)) {
            this->servo.setAngle(this->LUT_ANGLES.at(first));
            
                if (first> LUT_VALUES.at(7)){
                    this->secondSet.enable();
                }
                this->delaySecs(3);
            } else {   
                error = true;
            }
            // second value
            this->secondSet.disable();
            if (second < LUT_VALUES.at(15) || second == LUT_VALUES.at(15)) {
                this->servo.setAngle(this->LUT_ANGLES.at(second));
                
                if(second > LUT_VALUES.at(7)) {
                    this->secondSet.enable();
                }
                this->delaySecs(3);

                this-> secondSet.disable();
            } else {
                error = true;

            }
            this->delaySecs(2);

        } 
        if(error) {
            // Problem encountered: Set rgb light to red
            this-> rgb.changeColor(1);
            break;
        } 
    }
    // end of decoding- change color to green
    this-> rgb.changeColor(0);
}