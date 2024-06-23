#ifndef CLICK_APPLYPRESSURE__HH
#define CLICK_APPLYPRESSURE__HH
#include <click/element.hh>
CLICK_DECLS
/*
=c
applyPressure(TODO)
=s
TODO: Summary
=d
TODO: Complete description
*/
class ApplyPressure : public Element {
	//TODO: Add private attributes
	public:
		ApplyPressure();
		~ApplyPressure();
		const char *class_name() const { return "ApplyPressure"; }
		const char *port_count() const { return "1/1"; }
		const char *processing() const { return AGNOSTIC; }
		Packet *simple_action(Packet *p);
};
CLICK_ENDDECLS
#endif
