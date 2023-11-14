#ifndef __UNIT_HBRIDGE_H
#define __UNIT_HBRIDGE_H

#include "Arduino.h"
#include "Wire.h"

#define HBRIDGE_ADDR            0x20
#define DRIVER_CONFIG_REG       0x00
#define MOTOR_ADC_8BIT_REG      0x10
#define MOTOR_ADC_12BIT_REG     0x20
#define MOTOR_CURRENT_REG       0x30
#define JUMP_TO_BOOTLOADER_REG  0xFD
#define HBRIDGE_FW_VERSION_REG  0xFE
#define HBRIDGE_I2C_ADDRESS_REG 0xFF

#define DIR_STOP    0
#define DIR_FORWARD 1
#define DIR_REVERSE 2

typedef enum { _8bit = 0, _12bit } hbridge_anolog_read_mode_t;

class UNIT_HBRIDGE {
   private:
    uint8_t _addr;
    TwoWire* _wire;
    uint8_t _scl;
    uint8_t _sda;
    uint8_t _speed;
    void writeBytes(uint8_t addr, uint8_t reg, uint8_t* buffer, uint8_t length);
    void readBytes(uint8_t addr, uint8_t reg, uint8_t* buffer, uint8_t length);

   public:
    bool begin(TwoWire* wire = &Wire, uint8_t addr = HBRIDGE_ADDR,
               uint8_t sda = 21, uint8_t scl = 22, uint32_t speed = 100000L);
    uint8_t getDriverDirection(void);
    uint8_t getDriverSpeed8Bits(void);
    uint16_t getDriverSpeed16Bits(void);
    void setDriverDirection(uint8_t dir);
    void setDriverSpeed8Bits(uint8_t speed);
    void setDriverSpeed16Bits(uint16_t speed);
    uint16_t getDriverPWMFreq(void);
    void setDriverPWMFreq(uint16_t freq);
    float getMotorCurrent(void);
    uint16_t getAnalogInput(hbridge_anolog_read_mode_t bit);
    void jumpBootloader(void);
    uint8_t getFirmwareVersion(void);
    uint8_t getI2CAddress(void);
};

#endif
