This uses BTLE to communicate.

The service ID (whatever that means) is 9B9B.
The characteristic ID (whatever that means) is 5BF9.

You will recieve a new value every 50ms.

The values will be 16 or 17 bytes (I'm not sure exactly how this works).
If you recieve 17 bytes, discard the first byte.

There are four values. Each value can be decoded by using code equivalent to the
following:

result = arr[0+i] >> 24 | arr[1+i] >> 16 | arr[2+i] >> 8 | arr[3+i];

Here are the four values and their ranges (inclusive bottom, exclusive top):

Potentiometer; 0--1024; uint32_t
Accelerometer X; -32768--32768; int32_t
Accelerometer Y; -32768--32768; int32_t
Accelerometer Z; -32768--32768; int32_t
