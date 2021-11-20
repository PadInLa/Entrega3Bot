%FUNCIONES GENERADORAS ORDINARIAS
function FGO(ogf)
clc;
syms k n x
orden=12;
t=taylor(ogf,'order',orden);

[sucesion, potencias]=coeffs(t,'All');
sucesion=fliplr(sucesion);
potencias=fliplr(potencias);
n=0:orden-1
potencias
sucesion
end