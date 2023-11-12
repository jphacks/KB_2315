#include "UNIT_HBRIDGE.h"

void UNIT_HBRIDGE::writeBytes(uint8_t addr, uint8_t reg, uint8_t *buffer,
                              uint8_t length) {
    _wire->beginTransmission(addr);
    _wire->write(reg);
    for (int i = 0; i < length; i++) {
        _wire->write(*(buffer + i));
    }
    _wire->endTransmission();
}

void UNIT_HBRIDGE::readBytes(uint8_t addr, uint8_t reg, uint8_t *buffer,
                             uint8_t length) {
    uint8_t index = 0;
    _wire->beginTransmission(addr);
    _wire->write(reg);
    _wire->endTransmission();
    _wire->requestFrom(addr, length);
    for (int i = 0; i < length; i++) {
        buffer[index++] = _wire->read();
    }
}

bool UNIT_HBRIDGE::begin(TwoWire *wire, uint8_t addr, uint8_t sda, uint8_t scl,
                         uint32_t speed) {
    _wire  = wire;
    _addr  = addr;
    _sda   = sda;
    _scl   = scl;
    _speed = speed;
    _wire->begin(_sda, _scl, _speed);
    delay(10);
    _wire->beginTransmission(_addr);
    uint8_t error = _wire->endTransmission();
    if (error == 0) {
        return true;
    } else {
        return false;
    }
}

uint8_t UNIT_HBRIDGE::getDriverDirection(void) {
    uint8_t data[4];
    readBytes(_addr, DRIVER_CONFIG_REG, data, 1);
    return data[0];
}

uint8_t UNIT_HBRIDGE::getDriverSpeed8Bits(void) {
    uint8_t data[4];
    readBytes(_addr, DRIVER_CONFIG_REG + 1, data, 1);
    return data[0];
}

uint16_t UNIT_HBRIDGE::getDriverSpeed16Bits(void) {
    uint8_t data[4];
    readBytes(_addr, DRIVER_CONFIG_REG + 2, data, 2);
    return (data[0] | (data[1] << 8));
}

uint16_t UNIT_HBRIDGE::getDriverPWMFreq(void) {
    uint8_t data[4];
    readBytes(_addr, DRIVER_CONFIG_REG + 4, data, 2);
    return (data[0] | (data[1] << 8));
}

void UNIT_HBRIDGE::setDriverPWMFreq(uint16_t freq) {
    uint8_t data[4];
    data[0] = (freq & 0xff);
    data[1] = ((freq >> 8) & 0xff);
    writeBytes(_addr, DRIVER_CONFIG_REG + 4, data, 2);
}

void UNIT_HBRIDGE::setDriverDirection(uint8_t dir) {
    uint8_t data[4];
    data[0] = dir;
    writeBytes(_addr, DRIVER_CONFIG_REG, data, 1);
}

void UNIT_HBRIDGE::setDriverSpeed8Bits(uint8_t speed) {
    uint8_t data[4];
    data[0] = speed;
    writeBytes(_addr, DRIVER_CONFIG_REG + 1, data, 1);
}

void UNIT_HBRIDGE::setDriverSpeed16Bits(uint16_t speed) {
    uint8_t data[4];
    data[0] = speed;
    data[1] = (speed >> 8);
    writeBytes(_addr, DRIVER_CONFIG_REG + 2, data, 2);
}

uint16_t UNIT_HBRIDGE::getAnalogInput(hbridge_anolog_read_mode_t bit) {
    if (bit == _8bit) {
        uint8_t data;
        readBytes(_addr, MOTOR_ADC_8BIT_REG, &data, 1);
        return data;
    } else {
        uint8_t data[2];
        readBytes(_addr, MOTOR_ADC_12BIT_REG, data, 2);
        return (data[0] | (data[1] << 8));
    }
}

// Only V1.1 can use this
float UNIT_HBRIDGE::getMotorCurrent(void) {
    uint8_t data[4];
    float c;
    uint8_t *p;

    readBytes(_addr, MOTOR_CURRENT_REG, data, 4);
    p = (uint8_t *)&c;
    memcpy(p, data, 4);

    return c;
}

uint8_t UNIT_HBRIDGE::getFirmwareVersion(void) {
    uint8_t data[4];
    readBytes(_addr, HBRIDGE_FW_VERSION_REG, data, 1);
    return data[0];
}

uint8_t UNIT_HBRIDGE::getI2CAddress(void) {
    uint8_t data[4];
    readBytes(_addr, HBRIDGE_I2C_ADDRESS_REG, data, 1);
    return data[0];
}

// Only V1.1 can use this
void UNIT_HBRIDGE::jumpBootloader(void) {
    uint8_t value = 1;

    writeBytes(_addr, JUMP_TO_BOOTLOADER_REG, (uint8_t *)&value, 1);
}
