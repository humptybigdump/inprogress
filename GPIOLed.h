/**
 * @file GPIOLed.h
 * @author TIVA
 * @brief This class can also be found in a different form in the TIVA materials for the MSPM0!
 * @version 0.1
 * @date 2024-12-20
 * 
 * @copyright Copyright (c) 2024
 * 
 */
#pragma once
#include "ti_msp_dl_config.h"
#include <cstdint>
#include "ti_msp_dl_config.h"
class GPIOLed
{
    public:
     /* ///////////////////////////////
     *  *****   GPIOLed Class   ******
     *  //////////////////////////////
     * This class is designed to control LEDs with a GPIO output.
     * The GPIO class can also be used as an input; for more information,
     * see dl_gpio.h
     *
     */
     GPIOLed(GPIO_Regs* gpioPort, uint32_t gpioPin);

     /**
     * @brief GPIOLed::enable activates the stored pins for the stored port.
     * Use case: turn on LED
     */
     void enable(void);

     /**
     * @brief GPIOLed::toggle toggles the stored pins for the stored port.
     * If the pins are disabled, they will be enabled, and vice versa.
     */
     void toggle(void);

     /**
     * @brief GPIOLed::disable deactivates the stored pins.
     */
     void disable(void);

    private:
     GPIO_Regs* gpioPort;
     uint32_t gpioPins; // only one pin is used in this class
};
