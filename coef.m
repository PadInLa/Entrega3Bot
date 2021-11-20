function coef(RR,a,i0)
%% Datos de Entrada
clc;clear all;syms n;
%% Proceso
R=roots(RR);
k=length(a);
MR=zeros(k);
for cont=1:k
    MR(cont,:)=R.^(i0+cont-1);
end
b=MR\a;
info_R=tabulate(R);
t=size(info_R,1);
m=info_R(:,2);
%for i=1:t

sol=dot(b,R.^n);
%% Información de Salida
sol
end