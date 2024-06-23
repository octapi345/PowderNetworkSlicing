define($IFACENAME br-flat-lan-1);

FromDevice($IFACENAME)
	-> mem :: ApplyPressure
	->Discard;
