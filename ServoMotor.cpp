#include "ServoMotor.h"
#include "ti/devices/msp/peripherals/hw_gptimer.h"
#include "ti/driverlib/dl_common.h"
#include "ti/driverlib/dl_timer.h"
#include "ti/driverlib/dl_timerg.h"
#include "ti/driverlib/m0p/sysctl/dl_sysctl_mspm0g1x0x_g3x0x.h"
#include <cstdint>
#include <iostream>

/**
 * @brief Construct a new Servo Motor object
 * Stores portTimer and pwmClock.
 * Calculates pwmPeriod from the desired operating frequency.
 * NOTE: The PWM operating frequency is set in the system data.
 * It is not necessary to set it manually here.
 * @param portTimer PWMPort
 * @param pwmClock PWM clock frequency
 */
ServoMotor::ServoMotor(GPTIMER_Regs *portTimer, uint32_t pwmClock){
    this->portTimer = portTimer;
    this->pwmClock = pwmClock;
    this->pwmPeriod = uint32_t(pwmClock/FREQ);
}

/**
 * @brief Activates the servo motor and performs a rotation.
 * The motor must be correctly enabled and the angle should be stored.
 * @param angle Angle in degrees
 */
void ServoMotor::setAngle(float angle) {
    // only first channel
    disableMotor();
    uint32_t load = angleToLoad(angle);
    setLoad(load);
    enableMotor();
    DL_Common_delayCycles(10); // Minimum time to ensure correct port setting
    this->currentAngle = angle;
}

/**
 * @brief This method enables:
 * - the PWM clock
 * - the PWM output (channel output)
 * - the period counter of the PWM
 */
void ServoMotor::enableMotor(void){
    DL_TimerG_enableClock(portTimer);
    DL_TimerG_setCCPDirection(portTimer , DL_TIMER_CC0_OUTPUT ); // only use channel 0
    DL_TimerG_startCounter(portTimer);
}

/**
 * @brief This method disables:
 * - the PWM clock
 * - the period counter of the PWM
 */
void ServoMotor::disableMotor(void){
    DL_TimerG_disableClock(portTimer);
    DL_TimerG_stopCounter(portTimer);
}

/**
 * @brief Calculates the duty cycle for a given angle.
 * The conversion is derived from the extreme values for controlling the servo motor,
 * which produce a rotation between 0 and 180 degrees.
 * 
 * This duty cycle is then converted to the corresponding ticks,
 * which determine the load for the PWM counter. (hint: 100% duty = full pwmPeriod)
 * @param angle Angle between 0 and 180 degrees
 * @return uint32_t load: Number of ticks corresponding to the desired duty cycle
 */
uint32_t ServoMotor::angleToLoad(float angle){
    float duty;
    if (angle < 0.1f) {
        duty= MIN_DUTY;
    } else if (angle > 179.0f ) {
        duty = MAX_DUTY;
    } else {
        duty = MIN_DUTY + (MAX_DUTY - MIN_DUTY)  *(angle/180.0f);   
    }
    uint32_t load = this->pwmPeriod - uint32_t(this->pwmPeriod * duty/100.0f);

    return load;
}

/**
 * @brief Wrapper method to use DL_TimerG_setCaptureCompareValue.
 * 
 * @param load Number of ticks to be loaded into the PWM counter.
 */
void ServoMotor::setLoad(uint32_t load){
    // use only first channel
    DL_TimerG_setCaptureCompareValue(portTimer, load, DL_TIMER_CC_0_INDEX);

}
