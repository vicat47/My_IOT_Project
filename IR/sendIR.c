#include <wiringPi.h>
#include <stdio.h>

const int PWMpin = 1;

int setup();
int sendHead();
int sendTail();
void sendData(int* input);
int myPwnSender(int* input);

int main(void) 
{
    int testData[] = {1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1};
    myPwnSender(testData);
}

int myPwnSender(int* input)
{
    setup();
    sendHead();
    sendData(input);
    sendTail();
    return 0;
}

void sendData(int* input)
{
    int i;
    for(i = 0; i < 104; i++)
    {
        switch(input[i])
        {
            case 0:
                pwmWrite(PWMpin, 1);
                delayMicroseconds(560);
                pwmWrite (PWMpin, 0);
                delayMicroseconds(560);
                break;
            case 1:
                pwmWrite(PWMpin, 1);
                delayMicroseconds(560);
                pwmWrite (PWMpin, 0);
                delayMicroseconds(1690);
                break;
        }
    }
}

int sendHead()
{
    pwmWrite(PWMpin, 1);
    delayMicroseconds(9000);
    pwmWrite (PWMpin, 0);
    delayMicroseconds(4500);
    return 0;
}

int sendTail()
{
    pwmWrite(PWMpin, 1);
    delayMicroseconds(560);
    pwmWrite (PWMpin, 0);
    return 0;
}

int setup()
{
    if (-1 == wiringPiSetup()){
        return 10001;
    }
    pinMode(PWMpin, PWM_OUTPUT);
    pwmSetMode(PWM_MODE_MS);
    pwmSetRange(3);
    pwmSetClock(168);
    return 10000;
}