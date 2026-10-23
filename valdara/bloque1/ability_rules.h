#ifndef VALDARA_BLOQUE1_ABILITY_RULES_H
#define VALDARA_BLOQUE1_ABILITY_RULES_H
/* Attack/defense percentages are applied at the end of base damage calculation.
   Hidden traits and unapproved mythic effects are data-only, never faked. */
static unsigned short ValdaraRouteAbility(unsigned short species, unsigned short route, unsigned short fallback)
{
    if (route < 1 || route > 3) return fallback;
    if (species == 3 || species == 4)
        return route == 1 ? ABILITY_VALDARA_ESPIRITU_PROTECTOR :
               route == 2 ? ABILITY_VALDARA_AFINIDAD_OSCURA : ABILITY_VALDARA_INSTINTO_EXPLORADOR;
    if (species == 5 || species == 6)
        return route == 1 ? ABILITY_VALDARA_VINCULO_GUARDIAN :
               route == 2 ? ABILITY_VALDARA_PODER_UMBRIO : ABILITY_VALDARA_ADAPTACION_NATURAL;
    return fallback;
}
static unsigned short ValdaraAttackPercent(unsigned short ability, unsigned short type)
{
    if (ability == ABILITY_VALDARA_AFINIDAD_OSCURA && type == TYPE_DARK) return 120;
    if (ability == ABILITY_VALDARA_INSTINTO_EXPLORADOR && type == TYPE_GROUND) return 120;
    if (ability == ABILITY_VALDARA_PODER_UMBRIO && (type == TYPE_DARK || type == TYPE_GHOST)) return 125;
    if (ability == ABILITY_VALDARA_DOMINIO_OSCURO && type == TYPE_DARK) return 130;
    return 100;
}
static unsigned short ValdaraDefensePercent(unsigned short ability, unsigned short hp,
    unsigned short maxHp, unsigned char physical, unsigned char superEffective)
{
    if (ability == ABILITY_VALDARA_ESPIRITU_PROTECTOR && maxHp && (unsigned long)hp*2 < maxHp) return 85;
    if ((ability == ABILITY_VALDARA_VINCULO_GUARDIAN || ability == ABILITY_VALDARA_ADAPTACION_NATURAL) && superEffective) return 80;
    if (ability == ABILITY_VALDARA_ADAPTACION_TERRENAL && superEffective) return 75;
    if (ability == ABILITY_VALDARA_CORAZA_ANCESTRAL && physical) return 80;
    return 100;
}
#endif