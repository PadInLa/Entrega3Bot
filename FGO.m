function [potencias,sucesion,n]=FGO()
clc;
syms k n x
orden=12;
ogf = 1/(1-3*x)^2
t=taylor(ogf,'order',orden);

[sucesion, potencias]=coeffs(t,'All');
sucesion=fliplr(sucesion);
potencias=fliplr(potencias);
n=0:orden-1
potencias
sucesion
end
        