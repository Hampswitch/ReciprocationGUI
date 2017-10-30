function stratplot(stratlist,strattitle)

plot(stratlist(:,1),stratlist(:,2))
axis([-1 1 -1 1])
xlabel('Opponent gift to Agent')
ylabel('Agent gift to Opponent')
title(strattitle)

