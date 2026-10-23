/* Approved VALDARA logo, native Emerald title-screen integration.
 * Included by title_screen.c: existing intro, main menu and save flow stay intact.
 * BG0 is 8bpp, 30x20 tiles (38,400 bytes); screenblock 31 starts at 0xF800.
 * Palette slot 255 belongs only to PULSA START; it never recolours the emblem.
 */
static const u32 sValdaraTitleGfx[] = INCGFX_U32("graphics/title_screen/valdara/title.png", ".8bpp.lz");
static const u16 sValdaraTitlePal[] = INCGFX_U16("graphics/title_screen/valdara/title.png", ".gbapal");
static u16 sValdaraTitleFrame;
static MainCallback sValdaraTitleDestination;

static void VBlankCB_ValdaraTitle(void)
{
    TransferPlttBuffer();
}

static void CB2_ValdaraTitleExit(void)
{
    if (!UpdatePaletteFade())
    {
        SetVBlankCallback(NULL);
        SetMainCallback2(sValdaraTitleDestination);
    }
}

static void ValdaraTitleExit(MainCallback destination)
{
    sValdaraTitleDestination = destination;
    FadeOutBGM(4);
    BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
    SetMainCallback2(CB2_ValdaraTitleExit);
}

static void CB2_ValdaraTitle(void)
{
    u16 color;
    if (UpdatePaletteFade())
        return;

    // Keep Emerald's maintenance shortcuts and its confirmation screens.
    if (JOY_HELD(CLEAR_SAVE_BUTTON_COMBO) == CLEAR_SAVE_BUTTON_COMBO)
        ValdaraTitleExit(CB2_InitClearSaveDataScreen);
    else if (JOY_HELD(RESET_RTC_BUTTON_COMBO) == RESET_RTC_BUTTON_COMBO && CanResetRTC())
        ValdaraTitleExit(CB2_InitResetRtcScreen);
    else if (JOY_HELD(BERRY_UPDATE_BUTTON_COMBO) == BERRY_UPDATE_BUTTON_COMBO)
        ValdaraTitleExit(CB2_GoToBerryFixScreen);
    else if (JOY_NEW(A_BUTTON | START_BUTTON))
        ValdaraTitleExit(CB2_InitMainMenu);
    else
    {
        // Slow, readable blink: 90 frames on, 30 off. Only the prompt changes.
        if (++sValdaraTitleFrame >= 120)
            sValdaraTitleFrame = 0;
        color = sValdaraTitleFrame < 90 ? sValdaraTitlePal[255] : RGB_BLACK;
        LoadPalette(&color, 255, sizeof(color));
        // Remain on the approved title instead of returning to the stock intro.
        if ((gMPlayInfo_BGM.status & 0xFFFF) == 0)
            m4aSongNumStart(MUS_TITLE);
    }
}

static void CB2_InitValdaraTitleScreen(void)
{
    u16 x, y;
    volatile u16 *map;
    SetVBlankCallback(NULL);
    SetHBlankCallback(NULL);
    ScanlineEffect_Stop();
    SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_FORCED_BLANK);
    SetGpuReg(REG_OFFSET_BLDCNT, 0);
    SetGpuReg(REG_OFFSET_BLDALPHA, 0);
    SetGpuReg(REG_OFFSET_BLDY, 0);
    SetGpuReg(REG_OFFSET_WIN0H, 0);
    SetGpuReg(REG_OFFSET_WIN0V, 0);
    SetGpuReg(REG_OFFSET_WIN1H, 0);
    SetGpuReg(REG_OFFSET_WIN1V, 0);
    SetGpuReg(REG_OFFSET_WININ, 0);
    SetGpuReg(REG_OFFSET_WINOUT, 0);
    SetGpuReg(REG_OFFSET_BG0HOFS, 0);
    SetGpuReg(REG_OFFSET_BG0VOFS, 0);
    DmaFill16(3, 0, (void *)VRAM, VRAM_SIZE);
    DmaFill32(3, 0, (void *)OAM, OAM_SIZE);
    ResetTasks();
    ResetSpriteData();
    FreeAllSpritePalettes();
    gReservedSpritePaletteCount = 0;
    ResetPaletteFade();
    LZ77UnCompVram(sValdaraTitleGfx, (void *)BG_CHAR_ADDR(0));
    map = (volatile u16 *)BG_SCREEN_ADDR(31);
    for (y = 0; y < 20; y++)
        for (x = 0; x < 30; x++)
            map[y * 32 + x] = y * 30 + x;
    LoadPalette(sValdaraTitlePal, BG_PLTT_ID(0), PLTT_SIZE_8BPP);
    SetGpuReg(REG_OFFSET_BG0CNT, BGCNT_PRIORITY(0) | BGCNT_CHARBASE(0)
             | BGCNT_SCREENBASE(31) | BGCNT_256COLOR | BGCNT_TXT256x256);
    BeginNormalPaletteFade(PALETTES_ALL, 0, 16, 0, RGB_BLACK);
    TransferPlttBuffer();
    SetVBlankCallback(VBlankCB_ValdaraTitle);
    EnableInterrupts(INTR_FLAG_VBLANK);
    SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_MODE_0 | DISPCNT_BG0_ON);
    sValdaraTitleFrame = 0;
    sValdaraTitleDestination = NULL;
    m4aSongNumStart(MUS_TITLE);
    SetMainCallback2(CB2_ValdaraTitle);
}
