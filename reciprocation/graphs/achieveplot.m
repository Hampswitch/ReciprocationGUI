function achieveplot(stratlist,achievetitle)

th=0:pi/50:2*pi;
xunit=cos(th)
yunit=sin(th)

data=zeros(101,2)
for a = 1:101
    data(a,1)=cos(th(a))+sqrt(1-recipresponse(stratlist,cos(th(a)))^2)
    data(a,2)=sin(th(a))+recipresponse(stratlist,cos(th(a)))
end

hold on

plot(xunit,yunit,'k')
plot(2*xunit,2*yunit,'k')

plot([0 0],[2 -2],'k')
plot([-2 2],[0 0],'k')
fill(data(:,1),data(:,2),'g')



axis([-2 2 -2 2])
xlabel('Agent Payoff')
ylabel('Opponent Payoff')
title(achievetitle)

hold off
