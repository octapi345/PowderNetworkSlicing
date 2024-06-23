#include <click/config.h>
#include <click/glue.hh>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
// #include <click/TODO.hh>
#include "ApplyPressure.hh"
//#include "DummyProto.hh"
CLICK_DECLS
ApplyPressure::ApplyPressure() { };
ApplyPressure::~ApplyPressure() { };
Packet *ApplyPressure::simple_action(Packet *p) {
	int x = 2000;
    	int *mem = (int *)malloc(sizeof(int) * x);
    	int rnd=open("/dev/urandom", O_RDONLY);
    	read(rnd, mem, sizeof(int)*200);
    	close(rnd);
	free(mem);
	//click_chatter("test complete");
	return p;
};
CLICK_ENDDECLS
EXPORT_ELEMENT(ApplyPressure)
