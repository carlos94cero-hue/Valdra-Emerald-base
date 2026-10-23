#include <assert.h>
#include <stdio.h>
#include "constants/abilities.h"
#include "constants/pokemon.h"
#include "../ability_rules.h"
int main(void) {
    for (int s=3;s<=6;s++) {
        assert(ValdaraRouteAbility(s,1,0)==(s<=4 ? ABILITY_VALDARA_ESPIRITU_PROTECTOR : ABILITY_VALDARA_VINCULO_GUARDIAN));
        assert(ValdaraRouteAbility(s,2,0)==(s<=4 ? ABILITY_VALDARA_AFINIDAD_OSCURA : ABILITY_VALDARA_PODER_UMBRIO));
        assert(ValdaraRouteAbility(s,3,0)==(s<=4 ? ABILITY_VALDARA_INSTINTO_EXPLORADOR : ABILITY_VALDARA_ADAPTACION_NATURAL));
        assert(ValdaraRouteAbility(s,0,70)==70);
    }
    assert(ValdaraAttackPercent(ABILITY_VALDARA_AFINIDAD_OSCURA, TYPE_DARK)==120);
    assert(ValdaraAttackPercent(ABILITY_VALDARA_AFINIDAD_OSCURA, TYPE_WATER)==100);
    assert(ValdaraAttackPercent(ABILITY_VALDARA_PODER_UMBRIO, TYPE_GHOST)==125);
    assert(ValdaraAttackPercent(ABILITY_VALDARA_DOMINIO_OSCURO, TYPE_DARK)==130);
    assert(ValdaraAttackPercent(ABILITY_VALDARA_INSTINTO_EXPLORADOR, TYPE_GROUND)==120);
    assert(ValdaraDefensePercent(ABILITY_VALDARA_ESPIRITU_PROTECTOR,49,100,0,0)==85);
    assert(ValdaraDefensePercent(ABILITY_VALDARA_ESPIRITU_PROTECTOR,50,100,0,0)==100);
    assert(ValdaraDefensePercent(ABILITY_VALDARA_VINCULO_GUARDIAN,90,100,0,1)==80);
    assert(ValdaraDefensePercent(ABILITY_VALDARA_ADAPTACION_NATURAL,90,100,0,1)==80);
    assert(ValdaraDefensePercent(ABILITY_VALDARA_ADAPTACION_TERRENAL,90,100,0,1)==75);
    assert(ValdaraDefensePercent(ABILITY_VALDARA_CORAZA_ANCESTRAL,90,100,1,0)==80);
    assert(ValdaraDefensePercent(ABILITY_VALDARA_CORAZA_ANCESTRAL,90,100,0,0)==100);
    puts("PASS: active ability routing and precise offensive/defensive multipliers");
}