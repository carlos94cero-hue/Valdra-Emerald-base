/* Real Emerald ROM test; bootstrap skips Birch dialogue only in the test harness. */
#include <mgba/core/core.h>
#include <mgba/core/config.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <sys/stat.h>
#include "port_symbols.h"
static color_t pixels[240*160];
static struct mCore *c;
static const char *outdir;
static int gender;
static void frames(unsigned keys,int count){c->setKeys(c,keys);while(count--)c->runFrame(c);}
static uint32_t sb1(void){return c->busRead32(c,S_gSaveBlock1Ptr);}
static unsigned map(void){return c->busRead8(c,sb1()+5);}
static int px(void){unsigned id=c->busRead8(c,S_gPlayerAvatar+5);return (int16_t)c->busRead16(c,S_gObjectEvents+id*36+16)-7;}
static int py(void){unsigned id=c->busRead8(c,S_gPlayerAvatar+5);return (int16_t)c->busRead16(c,S_gObjectEvents+id*36+18)-7;}
static void shot(const char *name){
 char path[512];snprintf(path,sizeof(path),"%s/%d-%s.ppm",outdir,gender,name);FILE *f=fopen(path,"wb");assert(f);fprintf(f,"P6\n240 160\n255\n");
 for(int i=0;i<240*160;i++){uint32_t v=pixels[i];fputc(v&255,f);fputc((v>>8)&255,f);fputc((v>>16)&255,f);}fclose(f);
}
static void move_to(int x,int y){
 unsigned old=map();
 for(int n=0;n<2400&&(px()!=x||py()!=y);n++){unsigned key=px()<x?16:px()>x?32:py()<y?128:64;frames(key,1);assert(map()==old);}
 frames(0,24);if(px()!=x||py()!=y){fprintf(stderr,"Stuck at %d,%d target %d,%d map %u\n",px(),py(),x,y,map());shot("failure");exit(6);}
}
static void until_map(unsigned keys,unsigned destination){for(int n=0;n<600&&map()!=destination;n++)frames(keys,1);frames(0,180);assert(map()==destination);}
int main(int argc,char **argv){
 assert(argc==3);outdir=argv[2];mkdir(outdir,0755);
 for(gender=0;gender<2;gender++){
  c=mCoreFind(argv[1]);assert(c&&c->init(c));mCoreInitConfig(c,NULL);mCoreConfigSetDefaultIntValue(&c->config,"useBios",0);mCoreConfigSetDefaultIntValue(&c->config,"skipBios",1);mCoreConfigSetDefaultIntValue(&c->config,"mute",1);mCoreLoadConfig(c);
  c->setVideoBuffer(c,pixels,240);c->setAudioBufferSize(c,1024);assert(mCoreLoadFile(c,argv[1]));c->reset(c);frames(0,1200);
  uint32_t save2=c->busRead32(c,S_gSaveBlock2Ptr);assert(save2>=0x02000000&&save2<0x03008000);
  const uint8_t name[]={0xd0,0xbb,0xc6,0xbe,0xbb,0xcc,0xbb,0xff};for(int i=0;i<8;i++)c->busWrite8(c,save2+i,name[i]);c->busWrite8(c,save2+8,gender);c->busWrite16(c,save2+0x14,2);
  c->busWrite32(c,S_gMain,0);c->busWrite8(c,S_gMain+0x438,0);c->busWrite32(c,S_gMain+4,S_CB2_NewGame|1);
  frames(0,600);assert(c->busRead8(c,sb1()+4)==VALDARA_MAP_GROUP&&map()==0);assert(px()==19&&py()==38);shot("muelle");
  move_to(19,30);shot("paseo-maritimo");move_to(19,25);move_to(24,25);move_to(24,16);shot("plaza");frames(16|2,8);shot("carrera");frames(0,24);
  move_to(34,16);move_to(34,12);shot("centro-exterior");until_map(64,2);shot("centro-interior");until_map(128,0);
  printf("PASS gender=%d: native Emerald boot, full pier, camera, plaza, running, clinic entry/exit; map %u at %d,%d\n",gender,map(),px(),py());mCoreConfigDeinit(&c->config);c->deinit(c);
 }
 return 0;
}
