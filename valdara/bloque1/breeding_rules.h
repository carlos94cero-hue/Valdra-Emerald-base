/* Valdara breeding and route-adjusted stats. Strictly source-based, no ROM needed. */
#ifndef VALDARA_BLOQUE1_BREEDING_RULES_H
#define VALDARA_BLOQUE1_BREEDING_RULES_H

#define VALDARA_RUTA_SIN_ELEGIR 0
#define VALDARA_RUTA_HEROE 1
#define VALDARA_RUTA_VILLANO 2
#define VALDARA_RUTA_INVESTIGADOR 3
#define VALDARA_STAT_HP 0
#define VALDARA_STAT_ATK 1
#define VALDARA_STAT_DEF 2
#define VALDARA_STAT_SPEED 3
#define VALDARA_STAT_SPATK 4
#define VALDARA_STAT_SPDEF 5

struct ValdaraPathStats {unsigned short species;unsigned char route;unsigned char stats[6];};
static const struct ValdaraPathStats sValdaraPathStats[] = {
    {3, 1, {65, 75, 70, 55, 55, 70}}, // Escualito: Héroe, BST 390
    {3, 2, {60, 85, 55, 65, 75, 50}}, // Escualito: Villano, BST 390
    {3, 3, {65, 80, 65, 65, 55, 60}}, // Escualito: Investigador, BST 390
    {4, 1, {80, 55, 80, 50, 55, 80}}, // Escualita: Héroe, BST 400
    {4, 2, {70, 60, 65, 55, 90, 60}}, // Escualita: Villano, BST 400
    {4, 3, {80, 65, 80, 45, 55, 75}}, // Escualita: Investigador, BST 400
    {5, 1, {90, 100, 95, 75, 75, 95}}, // Escuarón: Héroe, BST 530
    {5, 2, {80, 120, 70, 90, 105, 65}}, // Escuarón: Villano, BST 530
    {5, 3, {95, 115, 90, 85, 65, 80}}, // Escuarón: Investigador, BST 530
    {6, 1, {110, 70, 115, 65, 70, 110}}, // Escuarina: Héroe, BST 540
    {6, 2, {100, 80, 85, 70, 120, 85}}, // Escuarina: Villano, BST 540
    {6, 3, {115, 85, 110, 60, 65, 105}}, // Escuarina: Investigador, BST 540
};

static unsigned char ValdaraStatForRoute(unsigned short species, unsigned short route, unsigned char stat, unsigned char fallback)
{
    unsigned i;
    if (stat >= 6 || route < 1 || route > 3) return fallback;
    for (i = 0; i < sizeof(sValdaraPathStats)/sizeof(sValdaraPathStats[0]); ++i)
        if (sValdaraPathStats[i].species == species && sValdaraPathStats[i].route == route)
            return sValdaraPathStats[i].stats[stat];
    return fallback;
}

static unsigned short ValdaraBreedingTarget(unsigned short species, unsigned char level, unsigned short route, unsigned char firstTrial, unsigned char secondTrial)
{
    /* First stage needs the selected path and level 18; later stages need story flags.
       Existing evolution scenes still play; the checks happen on the next level-up.
       Female species 2/4/6 evolve ONLY into female final variants. */
    if (route < VALDARA_RUTA_HEROE || route > VALDARA_RUTA_INVESTIGADOR || level < 18)
        return 0;
    switch (species)
    {
    case 1: return 3;
    case 2: return 4;
    case 3: return firstTrial ? 5 : 0;
    case 4: return firstTrial ? 6 : 0;
    case 5:
        if (!firstTrial || !secondTrial) return 0;
        return route == 1 ? 7 : route == 2 ? 8 : 9;
    case 6:
        if (!firstTrial || !secondTrial) return 0;
        return route == 1 ? 10 : route == 2 ? 11 : 12;
    default: return 0;
    }
}

static unsigned char ValdaraIsBreedingSpecies(unsigned short species) {return species >= 1 && species <= 12;}
#endif