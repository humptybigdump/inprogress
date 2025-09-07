#include "GPIOLed.h"
#include "ti/driverlib/dl_gpio.h"


/* ///////////////////////////////
* *****  GPIOLed Class******
*  //////////////////////////////
*
* Constructor 
*/
GPIOLed::GPIOLed(GPIO_Regs* gpioPort, uint32_t gpioPin){
    this->gpioPort = gpioPort; // GPIO Port of the LED
    gpioPins = gpioPin; // GPIO Pin of the LED
}

/**
 * @brief Turn LED on
 */
void GPIOLed::enable(void){
    DL_GPIO_setPins(gpioPort, gpioPins); // Set the GPIO pin to high to turn on the LED
}

/**
 * @brief  Turn LED on or off
 */
void GPIOLed::toggle(void){
    DL_GPIO_togglePins(gpioPort, gpioPins); // Toggle the GPIO pin state
}

/**
 * @brief  Turn LED off
 */
void GPIOLed::disable(void){
    DL_GPIO_clearPins(gpioPort, gpioPins); // Set the GPIO pin to low to turn off the LED
}
