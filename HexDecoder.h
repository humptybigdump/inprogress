/**
 * @file HexDecoder.h
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
#include "ServoMotor.h"
#include "GPIOLed.h"
#include "RGBLight.h"
#include <vector>

/**
 * @brief The HexDecoder class is for educational purposes only. It is not optimized for embedded software.
 * Instead of arrays, STL vectors are used, as these are more common in C++, as well as the use of reference parameters (pass by ref).
 * The goal of this class is to develop a better confidence with C++.
 */
class HexDecoder
{   
public:
    /**
    * @brief Construct a new HexDecoder object.
    * The following constructors are also initialized: ServoMotor, GPIOLed, RGBLed (red).
    * This class uses a ServoMotor, which uses hexadecimal numbers.
    * @param portTimer for the PWM of ServoMotor
    * @param pwmClock for the PWM of ServoMotor
    * @param gpioPort for LED control
    * @param gpioPin  for LED control
    */
    HexDecoder(GPTIMER_Regs *portTimer, uint32_t pwmClock, GPIO_Regs* gpioPort, uint32_t gpioPin); // config load
    
    /**
     * @brief This method takes a hexadecimal representation from a string and converts it into a rotation for the ServoMotor.
     * 
     * @param hexString a vector object of hexadecimal numbers, passed as a reference parameter
     */
    void decode(std::vector<uint8_t> &hexString);
    

private:
    /**
     * @brief Checks if a hexadecimal number between 8-F has occurred.
     * 
     * @param hexNumber the hexadecimal number
     * @return true if hexNumber >= 8 
     * @return false if hexNumber <= 7
     */
    bool isSecondSet(uint32_t hexNumber);

    /**
     * @brief Delays the execution of the next command by approximately secs seconds.
     * 
     * @param secs seconds 
     */
    void delaySecs(uint32_t secs);

    ServoMotor servo; 
    GPIOLed secondSet;
    RGBLight rgb;

    // Look-Up-Table of hexadecimal numbers 
    const std::vector<uint8_t> LUT_VALUES = {
        0x0,0x1,0x2,0x3,0x4,0x5, 0x6,0x7,0x8,0x9,0xA,0xB,0xC,0xD,0xE,0xF
    };
    // Decoder Look-Up-Table from numbers to angles
    const std::vector<float> LUT_ANGLES = {1, 26, 52, 77, 102, 128, 115, 167, 
                            13, 35, 58, 77, 103, 124, 148, 167};

    // Required parameter for binary operations in decimal representation, binary = 0b11110000
    const uint8_t FIRST_CIPHER_OP = 240; 
    
    // Required parameter for binary operations in decimal representation, binary = 0b00001111
    const uint8_t SECOND_CIPHER_OP = 15;  

};
