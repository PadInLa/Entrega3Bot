function sol=coef()
%% Datos de Entrada
clc;clear all;syms n;
RR=[1;-1;-2]
a=[1;1]
i0=0
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
        