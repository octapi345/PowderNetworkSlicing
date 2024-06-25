define($IFACENAME ens3);

FromDevice($IFACENAME)
        -> c :: Counter
        -> flow :: AggregateIPFlows(TCP_TIMEOUT 3600)
        -> ag :: AggregateCounter
        ->Discard;

Script(wait 5, print c.count, loop);
