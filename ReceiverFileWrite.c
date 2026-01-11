//testing out the receiver

#include <stdio.h>
#include <pigpio.h>

int main(void){
	
	if(gpioInitialise() < 0){
		printf("Failed the setup\n");
		return 1;
	}
	
	FILE *fptr;
	
	
	
	
	
	int receiverPin = 24;
	int currentLevel = 1;
	int s, u, counter, iU;
	gpioSetMode(receiverPin, PI_INPUT);
	
	
	char buttonName[20];
	printf("Enter the button name: ");
	
	scanf("%s", buttonName);
	
	fptr = fopen("LedCodes.txt", "a");
	fprintf(fptr, "\n%s:", buttonName);
	
	
	while(1){
		int readLevel = gpioRead(receiverPin);
		if(readLevel != currentLevel){
			gpioTime(PI_TIME_RELATIVE, &s, &u);
			
			if(counter >2 && (counter%2 == 0)){
				
				if((u-iU) < 800){
					printf("0");
					fprintf(fptr, "0");
					}
				else{
					printf("1");
					fprintf(fptr, "1");
					}
			}
			
			iU = u;
			
			currentLevel = readLevel;
			counter ++;
		}
		
		if(counter == 68){
			break;
		}
	}
	
	fclose(fptr);
	printf("\n");
	return 1;
}

