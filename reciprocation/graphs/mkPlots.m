d99e0625=[-1 -.533; -.386 -.993; .435 -.896; .905 -.289; 1 .233]
d99e1=[-1 -.849; -.484 -.984; .402 -.810; .832 .453; 1 .496]
d99e16=[-1 -.132; -.9979 .730; -.9977 .541; -.995 -.32; 1 .312]
d999e0625=[-1 -.67; -1 -.375; -.04 -.999; .844 -.397; 1 .255]
d999e1=[-1 -.005; -.997 -.979; .712 -.930; .911 .356; 1 .361]
d999e16=[-1 -.419; -.775 -.435; -.336 -.349; .603 .382; 1 .348]
d1e0625=[-1 -.904; -.971 -.993; .479 -.998; .948 -.275; 1 .145]
d1e1=[-1 -.929; -.658 -.988; .774 -.918; .923 .342; 1 .222]
d1e16=[-1 -.985; -1 -.972; -1 -.642; .999 .511; 1 -.276]

mkStratPlot(d99e0625,'d99e0625.png')
mkStratPlot(d99e1,'d99e1.png')
mkStratPlot(d99e16,'d99e16.png')
mkStratPlot(d999e0625,'d999e0625.png')
mkStratPlot(d999e1,'d999e1.png')
mkStratPlot(d999e16,'d999e16.png')
mkStratPlot(d1e0625,'d1e0625.png')
mkStratPlot(d1e1,'d1e1.png')
mkStratPlot(d1e16,'d1e16.png')

mkAchievePlot(d99e0625,'achieved99e0625.png')
mkAchievePlot(d99e1,'achieved99e1.png')
mkAchievePlot(d99e16,'achieved99e16.png')
mkAchievePlot(d999e0625,'achieved999e0625.png')
mkAchievePlot(d999e1,'achieved999e1.png')
mkAchievePlot(d999e16,'achieved999e16.png')
mkAchievePlot(d1e0625,'achieved1e0625.png')
mkAchievePlot(d1e1,'achieved1e1.png')
mkAchievePlot(d1e16,'achieved1e16.png')

generous=[-1 0; 0 0; .5 .866; 1 .705]
fair=[-1 -1;.705 .705;1 .705]
godfather=[-1 -1; 0 -1; .07 -.88; .32 -.73; .64 -.44; .92 .01; .980198 .19801; 1 .19801]

mkStratPlot(generous,'generousstrat.png')
mkAchievePlot(generous,'generousachieve.png')

mkStratPlot(fair,'fairstrat.png')
mkAchievePlot(fair,'fairachieve.png')

mkStratPlot(godfather,'godfatherstrat.png')
mkAchievePlot(godfather,'godfatherachieve.png')
