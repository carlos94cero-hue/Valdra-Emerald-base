@ Import these entry points into approved story quests. Do NOT expose route switches after the first choice.
Valdara_CaminoHeroe::
    setvar VAR_VALDARA_CAMINO, 1
    return
Valdara_CaminoVillano::
    setvar VAR_VALDARA_CAMINO, 2
    return
Valdara_CaminoInvestigador::
    setvar VAR_VALDARA_CAMINO, 3
    return
Valdara_PrimeraPruebaCompletada::
    setflag FLAG_VALDARA_PRIMERA_PRUEBA
    return
Valdara_SegundaPruebaCompletada::
    setflag FLAG_VALDARA_SEGUNDA_PRUEBA
    return