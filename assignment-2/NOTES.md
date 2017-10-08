Papers and links to read
========================

  * https://sockpuppet.org/blog/2013/07/22/applied-practical-cryptography/
    Inneholder en god del fine linker som kan brukes i oppgaven som referanser.

  * https://www.2uo.de/myths-about-urandom/
    Explains myths about /dev/random and /dev/urandom

TODOs
=====

Try to verify that the CSPRNG is good. Perhaps there is a suite of tools for
checking for good CSPRNGs? That should be part of the report, with output
samples.

Finn ut hvilken protokoll som brukes. Ligner dette paa Schnorr?

Min miller-rabin implementasjon bruker repeats, dvs KNUT98. Jeg bruker faktisk
random numbers i koden. At alternativ ville vaert aa bruke AKS primality test,
som er deterministisk. Men den er mindre effektiv. Har ogsaa at 0.5ln2^200 = 69
trials. For vaar del er 512 bits da 177 trials minst.

Se appendix i Stallings, staar der hvordan man gjoer ting.
Feks side 688 gir oss key exchange.

SE DENNE
https://crypto.stackexchange.com/questions/1963/how-large-should-a-diffie-hellman-p-be
Viser hvor store tall man maa ha paa diffie-hellman exchange, og forklarer
hvorfor vi maa ha p=2q+1, ogsaa hvordan velge primitive root
