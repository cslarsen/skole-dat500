rm(list=ls())

col1 <- data.frame(
  A=0.0286, B=0.0714, C=0.0000, D=0.0000, E=0.0429, F=0.0000, G=0.0286,
  H=0.0857, I=0.0143, J=0.0143, K=0.0714, L=0.1000, M=0.1143, N=0.0143,
  O=0.0000, P=0.0286, Q=0.0143, R=0.0143, S=0.0000, T=0.0429, U=0.0571,
  V=0.0714, W=0.0143, X=0.0857, Y=0.0429, Z=0.0429
)

col2 <- data.frame(
  A=0.0429, B=0.0571, C=0.0714, D=0.0143, E=0.0857, F=0.0429, G=0.0429,
  H=0.0286, I=0.0714, J=0.0000, K=0.0000, L=0.0429, M=0.0000, N=0.0286,
  O=0.0857, P=0.0143, Q=0.0143, R=0.0714, S=0.1000, T=0.1143, U=0.0143,
  V=0.0000, W=0.0286, X=0.0143, Y=0.0143, Z=0
)

eng <- data.frame(
  A=0.0812, B=0.0149, C=0.0271, D=0.0432, E=0.1202, F=0.0230, G=0.0203,
  H=0.0592, I=0.0731, J=0.0010, K=0.0069, L=0.0398, M=0.0261, N=0.0695,
  O=0.0768, P=0.0182, Q=0.0011, R=0.0602, S=0.0628, T=0.0910, U=0.0288,
  V=0.0111, W=0.0209, X=0.0017, Y=0.0211, Z=0.0007
)

par(mfrow=c(3,1))
barplot(as.matrix(col1), ylab="relative frequency", xlab="Unshifted column, low correlation", las=3)
barplot(as.matrix(eng), ylab="relative frequency", xlab="English", las=3)
barplot(as.matrix(col2), ylab="relative frequency", xlab="Shifted Column, high correlation", las=3)
