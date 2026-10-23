#include <assert.h>
#include <stdio.h>
#include "../breeding_rules.h"
int main(void) {
  unsigned r,l,s,phase;
  for (r=0; r<=4; ++r) for (l=1; l<=100; ++l) for (s=1;s<=12;++s) {
      unsigned v=ValdaraBreedingTarget(s,l,r,0,0);
      if (r==0||r==4||l<18||s>=3) assert(v==0);
      else assert(v==(s==1?3:4));
  }
  for (r=1;r<=3;++r) {
      assert(ValdaraBreedingTarget(3,18,r,1,0)==5);
      assert(ValdaraBreedingTarget(4,18,r,1,0)==6);
      assert(ValdaraBreedingTarget(5,18,r,0,1)==0);
      assert(ValdaraBreedingTarget(6,18,r,0,1)==0);
      assert(ValdaraBreedingTarget(5,18,r,1,1)==6+r);
      assert(ValdaraBreedingTarget(6,18,r,1,1)==9+r);
      for(s=7;s<=12;++s)assert(ValdaraBreedingTarget(s,100,r,1,1)==0);
  }
  for (r=1;r<=3;++r) for(s=3;s<=6;++s){
     unsigned sum=0;
     for(phase=0;phase<6;++phase){
        unsigned x=ValdaraStatForRoute(s,r,phase,0);
        assert(x>=30 && x<=150);sum+=x;
     }
     assert(sum == (s==3?390:s==4?400:s==5?530:540));
  }
  assert(ValdaraIsBreedingSpecies(1) && ValdaraIsBreedingSpecies(12));
  assert(!ValdaraIsBreedingSpecies(13));
  assert(ValdaraStatForRoute(7,1,0,123)==123);
  assert(ValdaraStatForRoute(3,0,0,75)==75);
  puts("PASS: all upbringing routes, 2 sexes, mission gates, 12 exact stat profiles and edge cases");
  return 0;
}