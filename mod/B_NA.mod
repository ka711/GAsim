TITLE HH sodium channel
: Hodgkin - Huxley squid sodium channel

: The model used in Melnick et al. 2004 Adapt 5 and 11 mV

NEURON {
	SUFFIX B_Na
	USEION na READ ena WRITE ina
	RANGE gnabar, ina, g, m, h             : added m and h
	GLOBAL inf, alpha_shift, beta_shift
}

UNITS {
	(mA) = (milliamp)
	(mV) = (millivolt)
}

INDEPENDENT {t FROM 0 TO 1 WITH 1 (ms)}
PARAMETER {
	v (mV)
	celsius = 37	(degC)
	dt (ms)
	gnabar=0.1 (mho/cm2) <0,1e9>
	ena = 53 (mV)
	alpha_shift = 0 (mV)
	beta_shift = 0 (mV)
}
STATE {
	m h
}
ASSIGNED {
	ina (mA/cm2)
	inf[2]
	g
}
LOCAL	fac[2]

INITIAL {
	rate(v*1(/mV))
	m = inf[0]
	h = inf[1]
}

BREAKPOINT {
	SOLVE states
	g = gnabar*m*m*m*h
	ina = gnabar*m*m*m*h*(v - ena)
}

PROCEDURE states() {	: exact when v held constant
	rate(v*1(/mV))
	m = m + fac[0]*(inf[0] - m)
	h = h + fac[1]*(inf[1] - h)
	VERBATIM
	return 0;
	ENDVERBATIM
}

UNITSOFF
FUNCTION alp(v(mV),i) { LOCAL a,b,c,q10 :rest = -70  order m,h
	v = v :convert to hh convention
	q10 = 3^((celsius - 23)/10)
	if (i==0) {
		alp = q10*.182*expM1(-v + 7 - 35 + alpha_shift, 9)
	}else if (i==1){
		alp = q10 * 1 *(0.061*expM1(-v + 13 - 48 + alpha_shift, 3) + 0.0166)


	}
}

FUNCTION bet(v,i) { LOCAL a,b,c,q10 :rest = -70  order m,h
	v = v 
	q10 = 3^((celsius - 23)/10)
	if (i==0) {
		bet = q10*.124*expM1(v - 7 + 35 + beta_shift, 9)
	}else if (i==1){
		bet = q10 * 1 *.0018*expM1(v - 13 + 84 + beta_shift, 18)
	}
}

FUNCTION expM1(x,y) {
	if (fabs(x/y) < 1e-6) {
		expM1 = y*(1 - x/y/2)
	}else{
		expM1 = x/(exp(x/y) - 1)
	}
}

PROCEDURE rate(v) {LOCAL a, b, tau :rest = -70
:	TABLE inf, fac DEPEND dt, celsius FROM -150 TO 100 WITH 200
	FROM i=0 TO 1 {
		a = alp(v,i)  b=bet(v,i)
		tau = 1/(a + b)
		if (i==0) {		
		inf[i] = a/(a+b)
	}else if (i==1) {
		inf[i] = 1/(1+exp((v+75-11)/9))
	} 
		fac[i] = (1 - exp(-dt/tau))
	}
}
UNITSON
