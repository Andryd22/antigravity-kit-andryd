---
name: embedded-systems
description: Embedded systems, firmware, IoT, and microcontroller programming. Arduino, ESP32, STM32, FreeRTOS, MQTT, sensors, and low-power design patterns.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Embedded Systems & IoT

> Microcontrollers, firmware, sensors, and IoT protocols. Code that runs on metal.

## Platform Selection

| Platform | RAM | Flash | Best For |
|----------|-----|-------|----------|
| **Arduino Uno (ATmega328P)** | 2KB | 32KB | Learning, simple sensors |
| **ESP32** | 520KB | 4-16MB | WiFi/BLE, IoT, MQTT |
| **STM32 (Cortex-M4)** | 128KB+ | 512KB+ | Industrial, motor control |
| **Raspberry Pi Pico (RP2040)** | 264KB | 2MB | Low-cost, PIO state machines |
| **nRF52 (Cortex-M4)** | 64-256KB | 512KB-1MB | BLE peripherals, wearables |

## Core Patterns

### Non-Blocking Code (No `delay()`)
```cpp
// ❌ Blocking: freezes everything for 1 second
void loop() {
    digitalWrite(LED, HIGH);
    delay(1000);
    digitalWrite(LED, LOW);
    delay(1000);
}

// ✅ Non-blocking: millis() based timer
unsigned long lastToggle = 0;
const unsigned long interval = 1000;

void loop() {
    unsigned long now = millis();
    if (now - lastToggle >= interval) {
        lastToggle = now;
        digitalWrite(LED, !digitalRead(LED));
    }
    // CPU free for other tasks
}
```

### State Machine
```cpp
enum SystemState { IDLE, SAMPLING, TRANSMITTING, SLEEPING, ERROR };
SystemState state = IDLE;

void loop() {
    switch (state) {
        case IDLE:
            if (sensor_ready()) state = SAMPLING;
            break;
        case SAMPLING:
            float value = read_sensor();
            if (value > THRESHOLD) state = TRANSMITTING;
            else state = SLEEPING;
            break;
        case TRANSMITTING:
            if (mqtt_publish("sensor/value", value)) state = IDLE;
            else state = ERROR;
            break;
        case ERROR:
            log_error(); state = IDLE;
            break;
    }
}
```

## IoT Protocols

| Protocol | Range | Power | Use Case |
|----------|-------|-------|----------|
| **MQTT** | Global (TCP) | Medium | Sensor data, dashboards |
| **BLE** | 10-100m | Very Low | Wearables, beacons |
| **Zigbee** | 10-100m | Low | Home automation mesh |
| **LoRaWAN** | 2-15km | Ultra Low | Agriculture, remote sensors |
| **WiFi** | 50m | High | Always-connected devices |

### MQTT Pattern (ESP32)
```cpp
#include <WiFi.h>
#include <PubSubClient.h>

WiFiClient wifiClient;
PubSubClient mqtt(wifiClient);

void setup() {
    WiFi.begin("SSID", "PASSWORD");
    mqtt.setServer("broker.hivemq.com", 1883);
    mqtt.setCallback(onMessage);
}

void reconnect() {
    while (!mqtt.connected()) {
        if (mqtt.connect("esp32_sensor_01")) {
            mqtt.subscribe("device/cmd");
        } else {
            delay(5000);  // Retry with backoff
        }
    }
}

void loop() {
    if (!mqtt.connected()) reconnect();
    mqtt.loop();

    static unsigned long lastPublish = 0;
    if (millis() - lastPublish > 10000) {
        float temp = read_temperature();
        mqtt.publish("sensor/temperature", String(temp).c_str());
        lastPublish = millis();
    }
}
```

## Power Management

| Technique | Power Saving | Complexity |
|-----------|-------------|------------|
| **Deep sleep** | ~10µA (ESP32) | Low — wake by timer/pin |
| **Duty cycling** | 50-90% | Medium — sample, sleep, repeat |
| **Clock gating** | 20-40% | Medium — disable unused peripherals |
| **Dynamic voltage scaling** | 30-50% | High — lower Vcore when idle |

## Memory Constraints

```cpp
// ❌ Heap fragmentation on MCU
String message = "Temperature: ";
message += String(temp);
message += "°C";

// ✅ Stack allocation, fixed buffer
char message[32];
snprintf(message, sizeof(message), "Temperature: %.1f°C", temp);
```

## Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| `delay()` in main loop | `millis()`-based timers |
| Dynamic allocation on MCU | Static buffers, stack allocation |
| Blocking WiFi/BLE in loop | Async callbacks, non-blocking |
| No watchdog timer | Enable watchdog, pet in loop |
| Hard-coded WiFi credentials | WiFiManager portal or BLE provisioning |
| Ignore brownout | Monitor voltage, safe shutdown |

## Checklist

- [ ] Non-blocking main loop (no `delay()`)
- [ ] Watchdog timer enabled and fed
- [ ] Static buffers, no dynamic allocation
- [ ] MQTT reconnect with exponential backoff
- [ ] OTA update support (ESP32/STM32)
- [ ] Power budget calculated (awake + sleep current)
- [ ] Serial debug output toggle (disable for production)
- [ ] Sensor calibration validated
