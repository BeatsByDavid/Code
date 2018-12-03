#include <iostream>
#include <errno.h>
#include <wiringPiSPI.h>
#include <unistd.h>
#include <stdint.h>

using namespace std;

static const int CHANNEL = 1;

int main()
{
    int fd, result;
    uint8_t buffer[100];

    cout<<"Initializing SPI"<<endl;

    fd = wiringPiSPISetup(CHANNEL, 500000);
    cout<<"Init Result: "<<fd<<endl;

}