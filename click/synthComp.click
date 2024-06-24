define($IFACENAME ens3);

FromDevice($IFACENAME)
	-> c :: Counter
	-> mem :: ApplyPressure
	->Discard;

Script(wait 5, print c.count, loop);
