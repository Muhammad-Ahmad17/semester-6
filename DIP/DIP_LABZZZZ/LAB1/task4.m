%plotting sine and cosine wave

t=-10:0.001:10;
A=cos(t);
B=sin(t);
subplot(2,1,1);
plot(t,A,'b');
title('cos wave');
legend('cos')
subplot(2,1,2);
plot(t,B,'r');
title('sine wave');
legend('sine')