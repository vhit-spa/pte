# pte
Python Test Environment, what a name?!

## Scope
This package provides API for a VHIT-custom test environment.

## Layout
This platform leverages Python for executing test scripts that interact with a microcontroller via a JTAG-serial debug interface:
- Data Exchange:
    - Serial communication establishes a channel between the test machine and the microcontroller.
    - JTAG-Serial Bridge: The JTAG interface facilitates controlling the microcontroller's serial communication, enabling specific memory access.
- Test Execution:
    - Scripts send serialized data to designated memory addresses in the microcontroller.
    - Data is subsequently read from the same addresses, deserialized, and analyzed for verification.

This setup allows automated testing of the microcontroller's memory access functionalities.

```                                                                         
  ┌─────────────────┐                               ┌─────────────────┐  
  │                 │                               │                 │  
  │   Test Machine  │        ┌────────────┐         │                 │  
  │                 │        │            │         │                 │  
  │        +        │        │    JTAG    │         │   µcontroller   │  
  │                 │◄──────►│            │◄───────►│                 │  
  │      Python     │        │  Interface │         │                 │  
  │    Framework    │        │            │         │                 │  
  │                 │        └────────────┘         │                 │  
  └─────────────────┘                               └─────────────────┘  
```

## Requirements
This package requires at least python 3.10 installed.
