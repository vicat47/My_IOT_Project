#include <wiringPi.h>

const int PWMpin = 1;
const int dutyRatio1 = 180;
const int dutyRatio0 = 600;

int setup();
int sendHead();
int sendTail();
void sendData();


int myPwnSender(input)
{
    setup();
    sendHead();
    sendData(input);
    sendTail();
    return 0;
}

void sendData(int[] input)
{
    int i;
    for(i = 0; i < 104; i++)
    {
        switch(input[i])
        {
            case 0:
                pwmWrite(PWMpin, dutyRatio1);
                delayMicroseconds(560);
                pwmWrite(PWMpin, dutyRatio0);
                delayMicroseconds(560);
                break;
            case 1:
                pwmWrite(PWMpin, dutyRatio1);
                delayMicroseconds(560);
                pwmWrite(PWMpin, dutyRatio0);
                delayMicroseconds(1690);
                break;
        }
    }
}

int sendHead()
{
    pwmWrite(PWMpin, dutyRatio1);
    delayMicroseconds(9000);
    pwmWrite(PWMpin, dutyRatio0);
    delayMicroseconds(4500);
    return 0;
}

int sendTail()
{
    pwmWrite(PWMpin, dutyRatio1);
    delayMicroseconds(560);
    return 0;
}

int setup()
{
    if (-1 == wiringPiSetup()){
        return 10001;
    }
    pinMode(PWMpin, PWM_OUTPUT);
    pwmSetRange(15);
    return 10000
}