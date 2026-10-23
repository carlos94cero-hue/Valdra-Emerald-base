/* Headless mGBA test. Captures are actual emulator output, not mockups. */
#include <mgba/core/core.h>
#include <mgba/core/config.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <sys/stat.h>
static color_t pixels[240*160];
static void screenshot(const char *dir,int frame){
 char path[512];snprintf(path,sizeof(path),"%s/frame-%05d.ppm",dir,frame);
 FILE *f=fopen(path,"wb");if(!f){perror(path);exit(2);}fputs("P6\n240 160\n255\n",f);
 for(int i=0;i<240*160;i++){uint32_t c=pixels[i];unsigned char rgb[3]={c&255,(c>>8)&255,(c>>16)&255};fwrite(rgb,1,3,f);}fclose(f);
}
int main(int argc,char **argv){
 if(argc!=3){fprintf(stderr,"usage: smoke ROM output_dir\n");return 2;}
 mkdir(argv[2],0755);
 struct mCore *core=mCoreFind(argv[1]);if(!core||!core->init(core))return 3;
 mCoreInitConfig(core,NULL);mCoreConfigSetDefaultIntValue(&core->config,"useBios",0);mCoreConfigSetDefaultIntValue(&core->config,"skipBios",1);mCoreConfigSetDefaultIntValue(&core->config,"mute",1);mCoreLoadConfig(core);
 core->setVideoBuffer(core,pixels,240);core->setAudioBufferSize(core,1024);
 if(!mCoreLoadFile(core,argv[1]))return 4;
 core->reset(core);
 for(int f=0;f<12000;f++){
  unsigned keys=0;
  if(f>180 && f<7800){if(f%40<4)keys=1;if(f%480<4)keys=8;}
  if(f>=7800){const unsigned dirs[4]={16,128,32,64};keys=dirs[((f-7800)/120)%4];if(f%120<4)keys|=1;}
  core->setKeys(core,keys);core->runFrame(core);
  if(f%300==299)screenshot(argv[2],f+1);
 }
 printf("mGBA completed %u frames; %zu-byte ROM. Captures require visual review.\n",core->frameCounter(core),core->romSize(core));return 0;
}
