# Android Real Device Networking Setup

## Overview
This document explains how to set up Android networking for real device communication with Spring Boot backend.

## Key Differences: Emulator vs Real Device

### Emulator (10.0.2.2)
- **IP Address**: `10.0.2.2` (special alias to host machine)
- **Use Case**: Development and testing in Android Studio
- **Network**: Uses host machine's localhost via NAT

### Real Device (192.168.x.x)
- **IP Address**: Your computer's actual local IP address
- **Use Case**: Testing on physical Android devices
- **Network**: Same WiFi network as your computer

## Setup Instructions

### 1. Spring Boot Server Configuration
Make sure your Spring Boot application binds to all network interfaces:

```properties
# application.properties
server.address=0.0.0.0
server.port=8080
```

This allows connections from any IP address on your network, not just localhost.

### 2. Find Your Computer's IP Address

**Windows:**
```cmd
ipconfig
```
Look for "IPv4 Address" under your WiFi adapter (e.g., 192.168.1.100)

**Mac/Linux:**
```bash
ifconfig
# or
ip addr
```
Look for "inet" address (e.g., 192.168.1.100)

### 3. Update Android Network Configuration

#### Network Security Config
The app includes `network_security_config.xml` that allows cleartext HTTP traffic for:
- localhost
- 10.0.2.2 (emulator)
- 192.168.x.x ranges (local network)

#### AndroidManifest.xml
- `android:usesCleartextTraffic="true"` - Allows HTTP traffic
- `android:networkSecurityConfig="@xml/network_security_config"` - Uses custom security config

### 4. Update IP Address in Code

Edit `NetworkConfig.kt` and update this line with your actual IP:

```kotlin
val computerIp = "192.168.29.53" // <-- REPLACE WITH YOUR ACTUAL IP
```

### 5. Spring Boot Backend Requirements

Ensure your Spring Boot application:
1. Runs on port 8080 (or update the port in Android code)
2. Binds to 0.0.0.0 (not just localhost)
3. Has CORS enabled for mobile app access

```java
@CrossOrigin(origins = "*")
@RestController
public class YourController {
    // your endpoints
}
```

## Troubleshooting

### "Cleartext HTTP traffic not permitted"
- Ensure `android:usesCleartextTraffic="true"` in AndroidManifest.xml
- Check network security config allows your IP range
- For production, use HTTPS instead of HTTP

### "Connection refused" / "Connection timeout"
1. Verify Spring Boot is running on your computer
2. Check firewall settings on your computer
3. Ensure both devices are on the same WiFi network
4. Verify IP address is correct
5. Check that Spring Boot binds to 0.0.0.0, not 127.0.0.1

### "Network unreachable"
- Make sure your Android device and computer are on the same WiFi network
- Check that your computer's firewall allows incoming connections on port 8080

## Testing Connectivity

You can test connectivity from your Android device using:
1. Web browser on the device: `http://YOUR_IP:8080`
2. NetworkConfig utility includes `canConnectToServer()` method

## Security Notes

- This setup uses HTTP (cleartext) for development convenience
- For production, implement HTTPS with proper SSL certificates
- Consider using a reverse proxy (nginx) for better security
- Implement proper authentication and authorization

## IP Address Ranges Covered

The network security config allows these ranges:
- 192.168.0.0/16 (all private 192.168.x.x addresses)
- 192.168.1.0/24 (common home router range)
- 192.168.43.0/24 (Android hotspot range)
- 192.168.8.0/24 (some router ranges)

This covers most common WiFi network configurations.
