@ Puerto Brisa introductory slice; separate from Hoenn events.
PuertoBrisa_Mom::
	lock
	faceplayer
	msgbox PuertoBrisa_TextMom, MSGBOX_DEFAULT
	release
	end
PuertoBrisa_Elder::
	lock
	faceplayer
	goto_if_set FLAG_SYS_POKEMON_GET, PuertoBrisa_ElderAfter
	msgbox PuertoBrisa_TextChoose, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, PuertoBrisa_GiveFemale
	givemon SPECIES_NIDORAN_M, 5
	goto PuertoBrisa_Given
PuertoBrisa_GiveFemale:
	givemon SPECIES_NIDORAN_F, 5
PuertoBrisa_Given:
	setflag FLAG_SYS_POKEMON_GET
	setflag FLAG_SYS_B_DASH
	msgbox PuertoBrisa_TextGiven, MSGBOX_DEFAULT
	giveitem ITEM_POKE_BALL, 5
	giveitem ITEM_POTION, 3
	release
	end
PuertoBrisa_ElderAfter:
	msgbox PuertoBrisa_TextElderAfter, MSGBOX_DEFAULT
	release
	end
PuertoBrisa_Gate::
	goto_if_set FLAG_SYS_POKEMON_GET, PuertoBrisa_GateOpen
	lockall
	msgbox PuertoBrisa_TextGate, MSGBOX_DEFAULT
	applymovement OBJ_EVENT_ID_PLAYER, PuertoBrisa_StepBack
	waitmovement 0
	releaseall
	end
PuertoBrisa_GateOpen:
	end
PuertoBrisa_StepBack:
	walk_down
	step_end
PuertoBrisa_Innkeeper::
	lock
	faceplayer
	msgbox PuertoBrisa_TextInnkeeper, MSGBOX_DEFAULT
	special HealPlayerParty
	playfanfare MUS_HEAL
	waitfanfare
	release
	end
PuertoBrisa_Nurse::
	lock
	faceplayer
	msgbox PuertoBrisa_TextNurse, MSGBOX_DEFAULT
	special HealPlayerParty
	playfanfare MUS_HEAL
	waitfanfare
	msgbox PuertoBrisa_TextHealed, MSGBOX_DEFAULT
	release
	end
PuertoBrisa_Clerk::
	lock
	faceplayer
	message PuertoBrisa_TextClerk
	waitmessage
	pokemart PuertoBrisa_Items
	msgbox PuertoBrisa_TextThanks, MSGBOX_DEFAULT
	release
	end
	.align 2
PuertoBrisa_Items:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_REPEL
	pokemartlistend
PuertoBrisa_Sailor::
	msgbox PuertoBrisa_TextSailor, MSGBOX_NPC
	end
PuertoBrisa_Fisherman::
	msgbox PuertoBrisa_TextFisherman, MSGBOX_NPC
	end
PuertoBrisa_Gardener::
	msgbox PuertoBrisa_TextGardener, MSGBOX_NPC
	end
PuertoBrisa_Cargo::
	msgbox PuertoBrisa_TextCargo, MSGBOX_NPC
	end
PuertoBrisa_Girl::
	msgbox PuertoBrisa_TextGirl, MSGBOX_NPC
	end
PuertoBrisa_Market::
	msgbox PuertoBrisa_TextMarket, MSGBOX_NPC
	end
PuertoBrisa_Citizen::
	msgbox PuertoBrisa_TextCitizen, MSGBOX_NPC
	end
PuertoBrisa_Ship::
	msgbox PuertoBrisa_TextShip, MSGBOX_NPC
	end
PuertoBrisa_Terminal::
	msgbox PuertoBrisa_TextTerminal, MSGBOX_NPC
	end
PuertoBrisa_Resident::
	msgbox PuertoBrisa_TextResident, MSGBOX_NPC
	end
PuertoBrisa_Upstairs::
	msgbox PuertoBrisa_TextUpstairs, MSGBOX_NPC
	end
PuertoBrisa_RouteGirl::
	msgbox PuertoBrisa_TextRouteGirl, MSGBOX_NPC
	end
PuertoBrisa_RouteEnd::
	msgbox PuertoBrisa_TextRouteEnd, MSGBOX_SIGN
	end
PuertoBrisa_InnSign::
	msgbox PuertoBrisa_TextInnSign, MSGBOX_SIGN
	end
PuertoBrisa_ClinicSign::
	msgbox PuertoBrisa_TextClinicSign, MSGBOX_SIGN
	end
PuertoBrisa_ShopSign::
	msgbox PuertoBrisa_TextShopSign, MSGBOX_SIGN
	end
PuertoBrisa_TerminalSign::
	msgbox PuertoBrisa_TextTerminalSign, MSGBOX_SIGN
	end
PuertoBrisa_RouteSign::
	msgbox PuertoBrisa_TextRouteSign, MSGBOX_SIGN
	end
PuertoBrisa_TextMom:
	.string "Por fin llegamos a Puerto Brisa.\nDescansaré mientras buscas ayuda.\pDicen que en Ciudad Salvia tienen\nla medicina que necesito.$"
PuertoBrisa_TextChoose:
	.string "Vas a salir del puerto, ¿verdad?\nLleva un compañero contigo.\pTengo dos NIDORAN.\n¿Prefieres a la hembra?\pSÍ: NIDORAN hembra.\nNO: NIDORAN macho.$"
PuertoBrisa_TextGiven:
	.string "Cuida de tu nuevo compañero.\nVuestro vínculo empieza hoy.\pEn la hierba de la Ruta 01\nencontrarás otros POKéMON.$"
PuertoBrisa_TextElderAfter:
	.string "La salida está al norte.\nMantén B pulsado para correr.\pElegir un compañero no decide\nqué camino seguirás en Valdara.$"
PuertoBrisa_TextGate:
	.string "Antes de salir, habla con el\nanciano que está junto al cartel.\pNo es seguro entrar en la hierba\nsin un POKéMON que te acompañe.$"
PuertoBrisa_TextInnkeeper:
	.string "Bienvenido a la posada.\nTu equipo puede descansar aquí.$"
PuertoBrisa_TextNurse:
	.string "Bienvenido al Centro POKéMON.\nVoy a cuidar de tu equipo.$"
PuertoBrisa_TextHealed:
	.string "Tus POKéMON están recuperados.\n¡Buen viaje por Valdara!$"
PuertoBrisa_TextClerk:
	.string "Bienvenido. Tenemos provisiones\npara tu primera expedición.$"
PuertoBrisa_TextThanks:
	.string "Gracias por tu visita.\n¡Cuida de tu compañero!$"
PuertoBrisa_TextSailor:
	.string "El barco acaba de atracar.\nLa terminal está al oeste.\pSube por el muelle para llegar\na la plaza de Puerto Brisa.$"
PuertoBrisa_TextFisherman:
	.string "La brisa trae vida a esta bahía.\nMira los barcos junto al faro.$"
PuertoBrisa_TextGardener:
	.string "Los jardines son de todos.\nLos vecinos los cuidamos juntos.$"
PuertoBrisa_TextCargo:
	.string "Este cargamento trae alimentos\npara los pueblos del interior.$"
PuertoBrisa_TextGirl:
	.string "¡Me encanta pasear por la plaza!\nDesde el faro se ve toda la bahía.$"
PuertoBrisa_TextMarket:
	.string "En el mercado hablamos de todo:\nel mar, los viajes y los POKéMON.$"
PuertoBrisa_TextCitizen:
	.string "Bienvenido a Valdara,\nla tierra de los vínculos.$"
PuertoBrisa_TextShip:
	.string "El barco permanece amarrado.\nLa tripulación prepara el regreso.$"
PuertoBrisa_TextTerminal:
	.string "Esta es la terminal de Puerto Brisa.\nEl próximo destino será Salvia.\pEn esta versión puedes explorar\nel puerto y el inicio de la ruta.$"
PuertoBrisa_TextResident:
	.string "Antes compartíamos remedios\ny conocimientos entre los pueblos.\pAlgunos todavía recordamos\nlo que significa Valdara.$"
PuertoBrisa_TextUpstairs:
	.string "La planta superior está cerrada.\nLa atención se ofrece aquí abajo.$"
PuertoBrisa_TextRouteGirl:
	.string "Puedes explorar la hierba\no continuar por el sendero.\pLos combates y las capturas\nusan las reglas de Esmeralda.$"
PuertoBrisa_TextRouteEnd:
	.string "RUTA 01 - CAMINO DE LA COSTA\nDirección: CIUDAD SALVIA.\pFin del tramo de esta versión.\nPuedes regresar a Puerto Brisa.$"
PuertoBrisa_TextInnSign:
	.string "POSADA DE PUERTO BRISA\nDescanso para viajeros y POKéMON.$"
PuertoBrisa_TextClinicSign:
	.string "CENTRO POKéMON\nCuidamos de tus compañeros.$"
PuertoBrisa_TextShopSign:
	.string "TIENDA POKéMON\nProvisiones para tu viaje.$"
PuertoBrisa_TextTerminalSign:
	.string "TERMINAL MARÍTIMA\nLlegadas y embarque.$"
PuertoBrisa_TextRouteSign:
	.string "NORTE: RUTA 01\nSUR: PLAZA Y MUELLES.$"
