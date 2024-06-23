define($IFACENAME ens3);

FromDevice($IFACENAME)
	-> mem :: ApplyPressure
	->Discard;
