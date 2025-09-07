#include "RGBLight.h"
#include "ti/driverlib/dl_gpio.h"

/**
 * @brief Construct a new RGBLight::RGBLight object
 * 
 * @param color 0 for Green, 1 for Red, 2 for Blue
 */
RGBLight::RGBLight(uint32_t color){
    // Assign ports and pins
    gpioPort = LED2_PORT;
    this->changeColor(color);
    this->color=color;
    }

/**
 * @brief Wrapper method for dl_gpio.h function that enables the pin/port combination
 * 
 */
void RGBLight::enable(void){
    DL_GPIO_setPins(gpioPort, gpioPins);
}

/**
 * @brief Wrapper method for dl_gpio.h function that toggles the pin state
 * 
 */
void RGBLight::toggle(void){
    DL_GPIO_togglePins(gpioPort, gpioPins);
}

/**
 * @brief Wrapper method for dl_gpio.h function that disables the pin/port combination
 * 
 */
void RGBLight::disable(void){
    DL_GPIO_clearPins(gpioPort, gpioPins);
}

/**
 * @brief Switches the light from one pin to another.
 * Note: Multiple pins can be enabled at the same time
 * Each pin is connected to a certain colored LED
 * If all three pins are active the resulting color is white
 * @param color 0 for Green, 1 for Red, 2 for Blue
 */
void RGBLight::changeColor(uint8_t color){
    this->disable();
    if (color == 0) {
        this->gpioPins = LED2_GREEN_PIN;
    } else if (color == 1) {
        this->gpioPins = LED2_RED_PIN;
    } else {
        this->gpioPins= LED2_BLUE_PIN;
    }
    this->enable();
}
