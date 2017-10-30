function result=recipresonse(stratlist,move)
if move==stratlist(1,1)
  result=stratlist(1,2)
elseif move==stratlist(end,1)
  result=stratlist(end,2)
else
  i=find(stratlist(:,1)>move,1)
  wt=(move-stratlist(i-1,1))/(stratlist(i,1)-stratlist(i-1,1))
  result=wt*stratlist(i,2)+(1-wt)*stratlist(i-1,2)
end
