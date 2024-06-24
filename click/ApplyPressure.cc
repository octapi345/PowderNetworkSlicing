#include <click/config.h>
#include <click/glue.hh>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <thread>
// #include <click/TODO.hh>
#include "ApplyPressure.hh"
//#include "DummyProto.hh"
CLICK_DECLS
void memThread(){
	int x = 2000;
    	int *mem = (int *)malloc(sizeof(int) * x);
    	int i;
	for(i=0; i<(x-30); i++){
		mem[mem[i+28]] = mem[mem[i+30]];
        	mem[mem[i+24]] = mem[mem[i+26]];
        	mem[mem[i+20]] = mem[mem[i+22]];
        	mem[mem[i+16]] = mem[mem[i+18]];
        	mem[mem[i+12]] = mem[mem[i+14]];
        	mem[mem[i+ 8]] = mem[mem[i+10]];
        	mem[mem[i+ 4]] = mem[mem[i+ 6]];
        	mem[mem[i+ 0]] = mem[mem[i+ 2]];	
	}
	free(mem);
}


ApplyPressure::ApplyPressure() { };
ApplyPressure::~ApplyPressure() { };
Packet *ApplyPressure::simple_action(Packet *p) {
	int k;
	for(k=0; k<3; k++){
		std::thread th (memThread);
		th.detach();
	}
	//click_chatter("test complete");
	return p;
};
CLICK_ENDDECLS
EXPORT_ELEMENT(ApplyPressure)
