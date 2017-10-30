function mkStratPlot(stratlist,fname)

h=figure(1);
set(gcf,'PaperUnits','centimeters')
set(gcf,'PaperPosition',[0 0 10 10])
set(h,'Visible','off')

plot(stratlist(:,1),stratlist(:,2))
axis([-1 1 -1 1])
xlabel('Opponent gift to Agent')
ylabel('Agent gift to Opponent')

saveas(h,fname)
