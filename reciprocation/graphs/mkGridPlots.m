d99e0625=[-1 -.533; -.386 -.993; .435 -.896; .905 -.289; 1 .233]
d99e1=[-1 -.849; -.484 -.984; .402 -.810; .832 .453; 1 .496]
d99e16=[-1 -.132; -.9979 .730; -.9977 .541; -.995 -.32; 1 .312]
d999e0625=[-1 -.67; -1 -.375; -.04 -.999; .844 -.397; 1 .255]
d999e1=[-1 -.005; -.997 -.979; .712 -.930; .911 .356; 1 .361]
d999e16=[-1 -.419; -.775 -.435; -.336 -.349; .603 .382; 1 .348]
d1e0625=[-1 -.904; -.971 -.993; .479 -.998; .948 -.275; 1 .145]
d1e1=[-1 -.929; -.658 -.988; .774 -.918; .923 .342; 1 .222]
d1e16=[-1 -.985; -1 -.972; -1 -.642; .999 .511; 1 -.276]

generous=[-1 0; 0 0; .5 .866; 1 .705]
fair=[-1 -1;.705 .705;1 .705]
godfather=[-1 -1; 0 -1; .07 -.88; .32 -.73; .64 -.44; .92 .01; .980198 .19801; 1 .19801]

h=figure(1);
set(gcf,'PaperUnits','centimeters')
set(gcf,'PaperPosition',[0 0 30 30])
set(h,'Visible','off')

subplot(3,3,1)
stratplot(d99e0625,'Discount .01 Explore .0625')
subplot(3,3,2)
stratplot(d99e1,'Discount .01 Explore 1')
subplot(3,3,3)
stratplot(d99e16,'Discount .01 Explore 16')
subplot(3,3,4)
stratplot(d999e0625,'Discount .001 Explore .0625')
subplot(3,3,5)
stratplot(d999e1,'Discount .001 Explore 1')
subplot(3,3,6)
stratplot(d999e16,'Discount .001 Explore 16')
subplot(3,3,7)
stratplot(d1e0625,'Discount 0 Explore .0625')
subplot(3,3,8)
stratplot(d1e1,'Discount 0 Explore 1')
subplot(3,3,9)
stratplot(d1e16,'Discount 0 Explore 16')

saveas(h,'stratgrid.png')

h=figure(2);
set(gcf,'PaperUnits','centimeters')
set(gcf,'PaperPosition',[0 0 30 30])
set(h,'Visible','off')

subplot(3,3,1)
achieveplot(d99e0625,'Discount .01 Explore .0625')
subplot(3,3,2)
achieveplot(d99e1,'Discount .01 Explore 1')
subplot(3,3,3)
achieveplot(d99e16,'Discount .01 Explore 16')
subplot(3,3,4)
achieveplot(d999e0625,'Discount .001 Explore .0625')
subplot(3,3,5)
achieveplot(d999e1,'Discount .001 Explore 1')
subplot(3,3,6)
achieveplot(d999e16,'Discount .001 Explore 16')
subplot(3,3,7)
achieveplot(d1e0625,'Discount 0 Explore .0625')
subplot(3,3,8)
achieveplot(d1e1,'Discount 0 Explore 1')
subplot(3,3,9)
achieveplot(d1e16,'Discount 0 Explore 16')

saveas(h,'achievegrid.png')

h=figure(3);
set(gcf,'PaperUnits','centimeters')
set(gcf,'PaperPosition',[0 0 25 10])
set(h,'Visible','off')

subplot(1,2,1)
stratplot(fair,'Fair Reciprocator Strategy')
subplot(1,2,2)
achieveplot(fair,'Fair Reciprocator Achievable Set')

saveas(h,'fairgrid.png')

h=figure(4);
set(gcf,'PaperUnits','centimeters')
set(gcf,'PaperPosition',[0 0 25 10])
set(h,'Visible','off')

subplot(1,2,1)
stratplot(generous,'Generous Reciprocator Strategy')
subplot(1,2,2)
achieveplot(generous,'Generous Reciprocator Achievable Set')

saveas(h,'generousgrid.png')

h=figure(5);
set(gcf,'PaperUnits','centimeters')
set(gcf,'PaperPosition',[0 0 25 10])
set(h,'Visible','off')

subplot(1,2,1)
stratplot(godfather,'Greedy Reciprocator Strategy')
subplot(1,2,2)
achieveplot(godfather,'Greedy Reciprocator Achievable Set')

saveas(h,'greedygrid.png')
