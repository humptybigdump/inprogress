/**
 * @file ServoMotor.h
 * @author Vanessa Del Rio Ortiz -  KIT IRS-VSA 
 * @brief  Permission is hereby granted, free of charge, to any person obtaining a copy
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
 * @version 0.1
 * @date 2024-12-20
 * 
 * @copyright Copyright (c) 2024
 * 
 */
#pragma once
#include "ti_msp_dl_config.h"
#include <cstdint>

class ServoMotor
{   
public:
    /* ///////////////////////////////
    *  ***   ServoMotor Class   ****
    *  //////////////////////////////
    * This class uses a Timer/PWM output to control a servo motor.
    * The PWM settings are predefined.
    * Only ports from TimerG are used.
    * For correct use of the class, the port for the timer
    * and the PWM clock frequency must be specified.
    */
    ServoMotor(GPTIMER_Regs *portTimer,uint32_t pwmClock); // config load

    /**
     * @brief Enables the servo motor
     */
    void enableMotor(void);

    /**
     * @brief Disables the servo motor
     */
    void disableMotor(void);

    /**
     * @brief Enables the servo motor and performs a rotation
     * of "angle" degrees
     * 
     * @param angle is a float value between 0 and 180 degrees
     */
    void setAngle(float angle);

private:
    /**
     * @brief Sets the number of ticks to be performed in one PWM period
     * 
     * @param load Number of ticks to be loaded into the PWM counter
     */
    void setLoad(uint32_t load);

    /**
     * @brief Moves the servo motor by angle degrees
     * 
     * @param angle Angle between 0 and 180 degrees
     * @return uint32_t load: Number of ticks corresponding to a duty cycle
     */
    uint32_t angleToLoad(float angle);

    float currentAngle; // don't forget to use x.xF

    GPTIMER_Regs *portTimer; // PWM port
    uint32_t FREQ = 50; // PWM frequency
    uint32_t pwmClock,pwmPeriod; // PWM clock frequency and PWM period
    /*****
    **** CALIBRATION PARAMETERS
    ** It is best to determine the correct values for your own servo motor
    ** to achieve accurate rotations.
    */
    float MIN_DUTY = 2.35; // with this duty cycle you achieve 0 degree rotation
    float MAX_DUTY = 12.3; // with this duty cycle you achieve 180 degree rotation

};