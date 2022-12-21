def get_ranked_icon(mode: str) -> str:
    if mode == "Expédition risquée":
        return "<:ExpeditionRisque:1036691276017455196>"
    elif mode == "Mission Bazookarpe":
        return "<:MissionBazookarpe:1036691565688668190>"
    elif mode == "Défense de zone":
        return "<:DefenseDeZone:1036691255125606400>"
    else:
        return "<:PluieDePalourdes:1036691257629618307>"

def get_brand_icon(brand: str) -> str:
    if brand == "Amiibo":
        return "<:amiibo:1054416940673802250>"
    elif brand == "Annaki":
        return "<:aroz:1054418169625837648>"
    elif brand == "Barazushi":
        return "<:alpaj:1054418812784627775>"
    elif brand == "Cuttlegear":
        return "<:macalamar:1054419333125771395>"
    elif brand == "Emberz":
        return "<:apex:1054420011428614234>"
    elif brand == "Enperry":
        return "<:dux:1054421119546966146>"
    elif brand == "Firefin":
        return "<:friture:1054421546942353521>"
    elif brand == "Forge":
        return "<:focus:1054421784142811146>"
    elif brand == "Grizzco":
        return "<:MOursSA:1054422098656903268>"
    elif brand == "Inkline":
        return "<:abysma:1054422423686094908>"
    elif brand == "Krak-On":
        return "<:krakers:1054423077242536056>"
    elif brand == "Rockenberg":
        return "<:iormungand:1054423374836813906>"
    elif brand == "Skalop":
        return "<:jack:1054423836885516348>"
    elif brand == "Splash Mob":
        return "<:gedeon:1054424146886537286>"
    elif brand == "SquidForce":
        return "<:kalamarus_rex:1054424465632657428>"
    elif brand == "Takoroka":
        return "<:cubic:1054424706331201546>"
    elif brand == "Tentatek":
        return "<:oculr:1054425072582021232>"
    elif brand == "Toni Kensa":
        return "<:thony_k:1054425413784453252>"
    elif brand == "Zekko":
        return "<:ezko:1054425882858639410>"
    elif brand == "Zink":
        return "<:leviathus:1054426036093341839>"
    else:
        return "<:no_brand:1054426078090887228>"

def get_ability_icon(ability: str) -> str:  # sourcery skip: low-code-quality
    if ability == "Ink Saver (Main)":
        return "<:InkSaverMain:1055107474836959312>"
    elif ability == "Ink Saver (Sub)":
        return "<:InkSaverSub:1055107735974326383>"
    elif ability == "Ink Recovery Up":
        return "<:InkRecoveryUp:1055108019500879923>"
    elif ability == "Run Speed Up":
        return "<:RunSpeedUp:1055108788044173403>"
    elif ability == "Swim Speed Up":
        return "<:SwimSpeedUp:1055109232288092250>"
    elif ability == "Special Charge Up":
        return "<:SpecialChargeUp:1055109455366340662>"
    elif ability == "Special Saver":
        return "<:SpecialSaver:1055109643237589002>"
    elif ability == "Special Power Up":
        return "<:SpecialPowerUp:1055109836456603679>"
    elif ability == "Quick Respawn":
        return "<:QuickRespawn:1055110053100793966>"
    elif ability == "Quick Super Jump":
        return "<:QuickSuperJump:1055111046894993478>"
    elif ability == "Sub Power Up":
        return "<:SubPowerUp:1055111628665925724>"
    elif ability == "Ink Resistance Up":
        return "<:InkResistanceUp:1055111932002177104>"
    elif ability == "Sub Resistance Up":
        return "<:SubResistanceUp:1055112154388373625>"
    elif ability == "Intensify Action":
        return "<:IntensifyAction:1055112559214202912>"
    elif ability == "Opening Gambit":
        return "<:OpeningGambit:1055112929722241035>"
    elif ability == "Last-Ditch Effort":
        return "<:LastDitchEffort:1055113163701489734>"
    elif ability == "Tenacity":
        return "<:Tenacity:1055113369436299354>"
    elif ability == "Comeback":
        return "<:Comeback:1055113723594936412>"
    elif ability == "Ninja Squid":
        return "<:NinjaSquid:1055113913429151794>"
    elif ability == "Haunt":
        return "<:Haunt:1055114224541646908>"
    elif ability == "Thermal Ink":
        return "<:ThermalInk:1055114371845595206>"
    elif ability == "Respawn Punisher":
        return "<:RespawnPunisher:1055114509305520170>"
    elif ability == "Ability Doubler":
        return "<:AbilityDoubler:1055114687584407573>"
    elif ability == "Stealth Jump":
        return "<:StealthJump:1055114866878332979>"
    elif ability == "Object Shredder":
        return "<:ObjectShredder:1055115003683938326>"
    elif ability == "Drop Roller":
        return "<:DropRoller:1055115219719958598>"
    elif ability == "Bomb Defense Up DX":
        return "<:BombDefenseUpDX:1055115563531251782>"
    elif ability == "Main Power Up":
        return "<:MainPowerUp:1055115725188120586>"
    elif ability == "Unknown":
        return "<:Unknown:1055115944965455882>"
    else:
        return "❓"