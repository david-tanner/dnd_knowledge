from discord.ext import commands #not sure why i have all these imports but i dont want to break anything so they stay
import logging, traceback
import os, sys
import time
import aiohttp
from random import randint
import utils
from collections import Counter
import discord
import asyncio
import urllib.request, json
import requests
import praw
import twitch
from twitch import TwitchClient
import random
import urllib
import lxml
import re
import linecache


#ignore everything beyond this point, its worthless

def findLine(fileCheck, keyWord):
    datafile = open(fileCheck)
    index = 0
    for line in datafile:
        if keyWord in line:
            return index
        else:
            index =  index + 1

def check(fileCheck, keyWord):
    datafile = open(fileCheck)
    for line in datafile:
        if keyWord in line:
            return True
    return False

client = discord.Client()



#classes
classes = ['artificer', 'barbarian', 'bard', 'bloodhunter', 'caster', 'cleric', 'cook', 'druid', 'fighter', 'halfcaster', 'martial', 'monk', 'mystic', 'paladin', 'pugilist', 'ranger', 'rogue', 'sorcerer', 'spells', 'warlock', 'wizard']

#spells
spells = ['acidsplash', 'bladeward', 'boomingblade', 'chilltouch', 'controlflames', 'createbonfire', 'dancinglights', 'druidcraft', 'eldritchblast', 'firebolt', 'friends', 'frostbite', 'greenflameblade', 'guidance', 'gust',
            'infestation', 'light', 'lightninglure', 'magehand', 'magicstone', 'mending', 'message', 'minorillusion', 'moldearth', 'poisonspray', 'prestidigitation', 'primalsavagery', 'producefrost', 'rayoffrost', 'resistance',
            'sacredflame', 'shapewater', 'shillelagh', 'shockinggrasp', 'swordburst', 'thaumaturgy', 'thornwhip', 'thunderclap', 'tollthedead', 'truestrike', 'viciousmockery', 'wordofradiance', 'onoff', 'virtue', 'absorbelements',
            'alarm', 'animalfriendship', 'armorofagythys', 'armsofhadar', 'bane', 'beastbond', 'bless', 'burninghands', 'catapult', 'causefear', 'ceremony', 'chaosbolt', 'charmperson', 'chromaticorb', 'colorspray', 'command',
            'compelledduel', 'comprehendlanguages', 'createordestroywater', 'curewounds', 'detectevilandgood', 'detectmagic', 'detectpoisonanddisease', 'disguiseself', 'dissonantwhispers', 'divinefavor', 'earthtremor', 'ensnaringstrike',
            'entangle', 'expeditiousretreat', 'faeriefire', 'falselife', 'featherfall', 'findfamiliar', 'fogcloud', 'goodberry', 'grease', 'guidingbolt', 'hailofthorns', 'healingword', 'hellishrebuke', 'heroism', 'hex', 'huntersmark',
            'iceknife', 'identify', 'illusoryscript','inflictwounds','jump','longstrider','magearmor','magicmissile','protectionfromevilandgood','purifyfoodanddrink','rayofsickness','sanctuary','searingsmite','shield','shieldoffaith',
            'silentimage','sleep','snare','speakwithanimals','tashashideouslaughter','tensersfloatingdisk','thunderoussmite','thunderwave','unseenservant','witchbolt','wrathfulsmite','zephyrstrike','guidinghand','healingelixir',
            'infalliblerelay','puppet','remoteaccess','senseemotion','suddenawakening','unearthlychorus','wildcunning','aganazzarsscorcher','aid','alterself','animalmessenger','arcanelock','augury','barkskin','beastsense',
            'blindnessdeafness','blur','brandingsmite','calmemotions','cloudofdaggers','continualflame','cordonofarrows','crownofmadness','darkness','darkvision','detectthoughts','dragonsbreath','dustdevil','earthbind','enhanceability',
            'enlargereduce','enthrall','findsteed','findtraps','flameblade','flamingsphere','gentlerepose','gustofwind','healingspirit','heatmetal','holdperson','invisibility','knock','lesserrestoration','levitate',
            'locateanimalsandplants','locateobject','magicmouth','magicweapon','maximiliansearthengrasp','melfsacidarrow','mindspike','mirrorimage','mistystep','moonbeam','nystulsmagicaura','passwithouttrace',
            'phantasmalforce','prayerofhealing','protectionfrompoison','pyrotechnics','rayofenfeeblment','ropetrick','scorchingray','seeinvisibility','shadowblade','shatter','silence','skywrite','snillocssnowballswarm',
            'spiderclimb','spikegrowth','spiritualweapon','suggestion','wardingbond','wardingwind','web','zoneoftruth','arcanehacking','digitalphantom','findvehicle','animatedead','auraofvitality','beaconofhope','bestowcurse',
            'blindingsmite','blink','calllightning','catnap','clairvoyance','conjureanimals','conjurebarrage','counterspell','createfoodandwater','crusadersmantle','daylight','dispelmagic','elementalweapon','enemiesabound',
            'eruptingearth','fear','feigndeath','fireball','flamearrows','fly','gaseousform','glyphofwarding','haste','hungerofhadar','hypnoticpattern','leomundstinyhut','lifetransference','lightningarrow','lightningbolt',
            'magiccircle','majorimage','masshealingword','meldintostone','melfsminutemeteors','nondetection','phantomseed','plantgrowth','protectionfromenergy','removecurse','revivify','sending','sleetstorm','slow','speakwithdead',
            'speakwithplants','spiritguardians','stinkingcloud','summonlesserdemons','thunderstep','tidalwave','tinyservant','tongues','vampirictouch','wallofsand','wallofwater','waterbreathing','waterwalk','windwall','haywire',
            'invisibilitytocameras','protectionfromballistics','arcaneeye','auraoflife','auraofpurity','banishment','blight','charmmonster','compulsion','confusion','conjureminorelementals','conjurewoodlandbeings','controlwater',
            'deathward','dimensiondoor','divination','dominatebeast','elementalbane','evardsblacktentacles','fabricate','findgreatersteed','fireshield','freedomofmovement','giantinsect','graspingvine','greaterinvisibility',
            'guardianoffaith','guardianofnature','hallucinatoryterrain','icestorm','leomundssecretchest','locatecreature','mordekainensfaithfulhound','mordekainensprivatesanctum','otilukesresilientsphere','phantasmalkiller',
            'polymorph','shadowofmoil','sickeningradiance','staggeringsmite','stoneshape','stoneskin','stormsphere','summongreaterdemon','vitriolicsphere','walloffire','waterysphere','conjureknowbot','synchronicity','systembackdoor',
            'animateobjects','antilifeshell','awaken','banishingsmite','bigbyshand','circleofpower','cloudkill','commune','communewithnature','coneofcold','conjureelemental','conjurevolley','contactotherplane','contagion','controlwinds',
            'creation','dansemacabre','dawn','destructivewave','dispelevilandgood','dominateperson','dream','enerveration','farstep','flamestrike','geas','greaterrestoration','hallow','holdmonster','holyweapon','immolation',
            'infernalcalling','insectplague','legendlore','maelstrom','masscurewounds','mislead','modifymemory','negativeenergyflood','passwall','planarbinding','raisedead','rarystelepathicbond','reincarnate','scrying','seeming',
            'skillempowerment','steelwindstrike','swiftquiver','synapticstatic','telekinesis','teleportationcircle','transmuterock','treestride','wallofforce','walloflight','wallofstone','wrathofnature','communewithcity','conjurevrock',
            'shutdown','arcanegate','bladebarrier','bonesoftheearth','chainlightning','circleofdeath','conjurefey','createhomunculus','createundead','disintegrate','drawmijsinstantsummons','druidgrove','eyebite','findthepath',
            'fleshtostone','forbiddance','globeofinvulnerability','guardsandwands','harm','heal','heroesfeast','investitureofice','investitureofflame','investitureofstone','investitureofwind','magicjar','masssuggestion','mentalprison',
            'moveearth','otilukesfreezingsphere','ottosirresistibledance','planarally','primordialward','programmedillusion','scatter','soulcage','sunbeam','tenserstransformation','tansportviaplants','trueseeing','wallofice',
            'wallofthorns','wildwalk','wordofrecall','conjurecelestial','crownofstars','delayedblastfireball','divineword','etherealness','fingerofdeath','firestorm','forcecage','miragearcane','mordenkainensmagnificentmansion',
            'mordenkainenssword','planeshift','powerwordpain','prismaticspray','projectimage','regenerate','resurrection','reversegravity','sequester','simulacrum','symbol','teleport','templeofthegods','whirlwind','conjurehezrou',
            'abidalzimshorridwilting','animalshapes','antimagicfield','antipathysympathy','clone','controlweather','demiplane','dominatemonster','earthquake','feeblemind','glibness','holyaura','illusorydragon','incendiarycloud',
            'maddeningdarkness','maze','mightyfortress','mindblank','powerwordstun','sunburst','telepathy','tsunami','astralprojection','foresight','gate','imprisonment','invulnerability','massheal','masspolymorph','powerwordheal',
            'powerwordkill','prismaticwall','psychicscream','shapechange','stormofvengeance','timestop','truepolymorph','trueressurection','weird','wish']

#deities
faerunpantheon = ['azuth', 'bane', 'chauntea', 'cyric', 'gond', 'helm', 'ilmater', 'kelemvor', 'kossuth', 'lathander', 'lolth', 'malar', 'mask', 'mielikki', 'mystra', 'oghma', 'selune', 'shar', 'shaundakul', 'silvanus', 'sune',
            'talos', 'tempus', 'torm', 'tymora', 'tyr', 'umberlee', 'uthgar', 'waukeen', 'akadi', 'auril', 'beshaba', 'deneir', 'eldath', 'finder', 'garagos', 'gargauth', 'grumbar', 'gwaeronwindstorm', 'hoar', 'istishia', 'jergal',
            'lliira', 'loviatar', 'lurue', 'milil', 'nobanion', 'redknight', 'savras', 'sharess', 'shiallia', 'siamorphe', 'talona', 'tiamat', 'ubtao', 'ulutiu', 'valkur', 'velsharoon']
karaturanpantheon = ['aiching', 'chancheng', 'chenhsiang', 'chihshih', 'fakuan', 'hsingyong', 'kwanying', 'madmonkey', 'nungchiang', 'shuchia', 'thecelestialemperor']
matzicanpantheon = ['azul', 'eha', 'kiltzi', 'maztica', 'nula', 'plutoq', 'qotal', 'tezca', 'watil', 'zaltec']
mulhordandipantheon = ['anhur', 'geb', 'hathor', 'horusre', 'isis', 'nephthys', 'osiris', 'sebek', 'set', 'thoth']
zakharanpantheon = ['bala', 'hajama', 'hakiyah', 'haku', 'jarmik', 'jauhar', 'jisan', 'kor', 'lostone', 'najm', 'ragarra', 'selan', 'shajar', 'thasmudyan', 'vataqatal', 'zann']
drowpantheon = ['eilistraee', 'ghaunadaur', 'kiaransalee', 'lolth', 'selvetarm', 'vhaeraun']
dwarvenpantheon = ['abbathor', 'berronartruesilver', 'clangeddinsilverbeard', 'deepduerra', 'dugmarenbrightmantle', 'dumathoin', 'gormgulthyn', 'haelabrightaxe', 'laduguer', 'marthammorduin', 'moradin', 'sharindlar', 'thardharr',
            'vergadain']
elvenpantheon = ['aerdriefaenya', 'angharradh', 'corellonlarethian', 'deepsashelas', 'erevanilesere', 'fenmarelmestarine', 'hanalicelanil', 'labelasenoreth', 'rillifanerallathil', 'sehaniniemoonbow', 'shevarash', 'solonorthelandria']
gnomepantheon = ['baervanwildwanderer', 'baravarcloakshadow', 'callarduransmoothhands', 'flandalsteelskin', 'gaerdalironhand', 'garldlittergold', 'segojanearthcaller', 'urdlen']
halflingpantheon = ['arvoreen', 'brandobaris', 'cyrrollalee', 'sheelaperyroyl', 'urogalan', 'yondalla']
orcpantheon = ['bahgtru', 'gruumsh', 'ilneval', 'luthic', 'shargass', 'yurtrus']
draconicpantheon = ['asgorath', 'astilabor', 'bahamut', 'garyx', 'hlal', 'kereska', 'lendys', 'null', 'tamara', 'task', 'zorquan']
giantpantheon = ['grolanthor', 'hiatea', 'iallanis', 'memnor', 'othea', 'skoraeus', 'stronmaus']
monsterdeities = ['baphomet', 'blibdoolpoolp', 'eadro', 'facelessgod', 'karrrga', 'kurtulmak', 'merrshaulk', 'persana', 'ramenos', 'trishina', 'vaprak']
deaddeities = ['amaunator', 'auppenser', 'bhall', 'chronos', 'elikarashae', 'gilgeam', 'ibrandul', 'iyachtuxvim', 'kiputytto', 'leira', 'moander', 'murdane', 'myrkul', 'ramman', 're', 'relkathoftheinfinitebranches', 'tchazzar', 'tyche', 'zinzerena']
alldeities = faerunpantheon.append(karaturanpantheon.append(matzicanpantheon.append(mulhordandipantheon.append(zakharanpantheon.append(drowpantheon.append(dwarvenpantheon.append(elvenpantheon.append(gnomepantheon.append(halflingpantheon.append(orcpantheon.append(draconicpantheon.append(giantpantheon.append(monsterdeities.append(deaddeities))))))))))))))

spelllist = open('spellfifthedition.txt', 'r')

currentmonster = open('currentmonster.txt', 'w')
newline = '\n'
#currentchannel = client.get_channel('496743000135958540')

# server side check to see if working
@client.event
async def on_ready():
    print('Logged in as')
    print('testing stuff#0444') #outdated, need to update
    print('304225937330012160') #outdated
    print('------')
    await client.change_presence(game=discord.Game(name='you like a fiddle'))

# i dont remember what this is for
# gns id = 36619809

# discord chat conditionals
@client.event
async def on_message(message):
    if message.content.startswith('!spell'):
        spell_wanted = message.content[7:]
        spell_length = len(spell_wanted) + 1
        spell_url = 'https://www.aidedd.org/dnd/sorts.php?vo=' + spell_wanted
        await client.send_message(message.channel, 'you wanted ' + spell_wanted + ' length ' + str(spell_length))
        if spell_wanted in spells:
            await client.send_message(message.channel, 'i have that spell: ' + spell_url)
        else:
            await client.send_message(message.channel, 'i dont have that spell')
    elif message.content.startswith('!monster'):
        monster_wanted = message.content[9:]
        monster_length = len(monster_wanted) + 1
        if check('monsterlist.txt', monster_wanted):
            lineNum = findLine('monsterdata.txt', monster_wanted)
##            monster_url = 'https://raw.githubusercontent.com/chisaipete/bestiary/master/_posts/2017-09-10-' + linecache.getline('monsterlist_web.txt', lineNum+1)[:-1] + '.markdown'
##            #await client.send_message(message.channel, monster_url)
##            website = urllib.request.urlopen(monster_url)
##            html = str(website.read())
            monsterMessage = linecache.getline('monsterdata.txt', findLine('monsterdata.txt', monster_wanted)+1).replace('\\n', '\n')[monster_length+2:]
            await asyncio.sleep(3)
            await client.send_message(message.channel, 'I have that monster, let me get it...')
            await asyncio.sleep(7)
            if len(monsterMessage) + 1 <= 2000:
                await client.send_message(message.channel, linecache.getline('monsterdata.txt', findLine('monsterdata.txt', monster_wanted)+1).replace('\\n', '\n')[monster_length+2:])
            else:
                sublength = int(len(monsterMessage)/3)
                firstPart = monsterMessage[:sublength]
                secondPart = monsterMessage[sublength:int(len(monsterMessage))-sublength]
                thirdPart = monsterMessage[-sublength:]
                secondSplit = secondPart.split('\n', 1)
                thirdSplit = thirdPart.split('\n', 1)
                #print (firstPart)
                #print('break')
                #print(secondSplit)
                #print('break')
                #print(thirdSplit)
                await client.send_message(message.channel, firstPart + 'break ' + secondSplit[0] + '\nbreak')
                await client.send_message(message.channel, secondSplit[1] + 'break' + thirdSplit[0] + '\nbreak')
                await client.send_message(message.channel, thirdSplit[1])
        else:
            await asyncio.sleep(4)
            await client.send_message(message.channel, "Sorry, I don't have that monster. Please try again, or tell paincow if this was a mistake.")














    #soon to be deprecated
    elif message.content.startswith('!artificeralch'):
        await client.send_message(message.channel, 'Sending "ARTIFICER.ALCHEMIST" charachter sheet...')
        await client.send_file(message.channel, 'Class_Character_Sheet_Artificer-Alchemist_V11_Fillable.pdf')
    elif message.content.startswith('!artificerguns'):
        await client.send_message(message.channel, 'Sending "ARTIFICER.GUNSMITH charachter sheet...')
        await client.send_file(message.channel, 'Class_Character_Sheet_Artificer-Gunsmith_V11_Fillable.pdf')
    elif message.content.startswith('!barbarian'):
        await client.send_message(message.channel, 'Sending "BARBARIAN" charachter sheet...')
        await client.send_file(message.channel, 'Class_Character_Sheet_Barbarian_V13_Fillable.pdf')
    elif message.content.startswith('!bard'):
        await client.send_message(message.channel, 'Sending "BARD" charachter sheet...')
        await client.send_file(message.channel, 'Class_Character_Sheet_Bard_V12_Fillable.pdf')
    elif message.content.startswith('!bloodhunter'):
        await client.send_message(message.channel, 'Sending "BLOOD HUNTER" charachter sheet...')
        await client.send_file(message.channel, 'Class_Character_Sheet_Blood_Hunter_V10_Fillable.pdf')
    elif message.content.startswith('!caster'):
        await client.send_message(message.channel, 'Sending "CASTER.GENERAL" charachter sheet...')
        await client.send_file(message.channel, 'Caster_Sheets_General.zip')
    elif message.content.startswith('!cleric'):
        await client.send_message(message.channel, 'Sending "CLERIC" charachter sheet...')
        await client.send_file(message.channel, 'Class_Character_Sheet_Cleric_V12_Fillable.pdf')
    elif message.content.startswith('!cook'):
        await client.send_message(message.channel, 'Sending "COOK" charachter sheet...')
        await client.send_file(message.channel, 'Class_Character_Sheet_Cook_V12_Fillable.pdf')
    elif message.content.startswith('!druid'):
        await client.send_message(message.channel, 'Sending "DRUID" charachter sheet...')
        await client.send_file(message.channel, 'Class_Character_Sheet_Druid_V11_Fillable.pdf')
    elif message.content.startswith('!fighter'):
        await client.send_message(message.channel, 'Sending "FIGHTER.ALL" charachter sheet...')
        await client.send_file(message.channel, 'Fighter_Sheets_All.zip')
    elif message.content.startswith('!halfcaster'):
        await client.send_message(message.channel, 'Sending "HALFCASTER.GENERAL" charachter sheet...')
        await client.send_file(message.channel, 'Halfcaster_Sheets_All.zip')
    elif message.content.startswith('!martial'):
        await client.send_message(message.channel, 'Sending "MARTIAL.GENERAL" charachter sheet...')
        await client.send_file(message.channel, 'Martial_Sheets_All.zip')
    elif message.content.startswith('!monk'):
        await client.send_message(message.channel, 'Sending "MONK" charachter sheet...')
        await client.send_file(message.channel, 'Class_Character_Sheet_Monk_V12_Fillable.pdf')
    elif message.content.startswith('!mystic'):
        await client.send_message(message.channel, 'Sending "MYSTIC" charachter sheet...')
        await client.send_file(message.channel, 'Class_Character_Sheet_Mystic_V10_Fillable.pdf')
    elif message.content.startswith('!paladin'):
        await client.send_message(message.channel, 'Sending "PALADIN" charachter sheet...')
        await client.send_file(message.channel, 'Class_Character_Sheet_Paladin_V12_Fillable.pdf')
    elif message.content.startswith('!pugilist'):
        await client.send_message(message.channel, 'Sending "PUGILIST" charachter sheet...')
        await client.send_file(message.channel, 'Class_Character_Sheet_Pugilist_V10_Fillable.pdf')
    elif message.content.startswith('!ranger'):
        await client.send_message(message.channel, 'Sending "RANGER.ALL" charachter sheet...')
        await client.send_file(message.channel, 'Ranger_Sheets_all.zip')
    elif message.content.startswith('!rogue'):
        await client.send_message(message.channel, 'Sending "ROGUE.ALL" charachter sheet...')
        await client.send_file(message.channel, 'Rogue_Sheets_All.zip')
    elif message.content.startswith('!sorcerer'):
        await client.send_message(message.channel, 'Sending "SORCERER" charachter sheet...')
        await client.send_file(message.channel, 'Class_Character_Sheet_Sorcerer_V11_Fillable.pdf')
    elif message.content.startswith('!spells'):
        await client.send_message(message.channel, 'Sending "SPELLS" sheet...')
        await client.send_file(message.channel, 'Spell_Sheets_All.zip')
    elif message.content.startswith('!warlock'):
        await client.send_message(message.channel, 'Sending "WARLOCK" charachter sheet...')
        await client.send_file(message.channel, 'Class_Character_Sheet_Warlock_V13_Fillable.pdf')
    elif message.content.startswith('!wizard'):
        await client.send_message(message.channel, 'Sending "WIZARD" charachter sheet...')
        await client.send_file(message.channel, 'Class_Character_Sheet_Wizard_V12_Fillable.pdf')
    elif message.content.startswith('!help'):
        await client.send_message(message.channel, 'Sending help...')
        await client.send_file(message.channel, 'Bot_Commands.txt')
    elif message.content.startswith('!sourcecode'):
        await client.send_message(message.channel, 'noo, do not look...')
        await client.send_file(message.channel, 'cr bot.py')
    elif message.content.startswith('!thothammer'):
        await client.send_message(message.channel, 'nah fam')
    elif message.content.startswith('!'):
        await client.send_message(message.channel, "I'm sorry, I couldn't understand that. Please look over my commands again. If you think this was a mistake, be sure to message paincow")
        await client.send_file(message.channel, 'Bot_Commands_txt')




client.run('NDk3MjY2Mjc4NTA4MjY1NDgy.Dpcshg.Xmr6tZy8qbv05AxdbZhUWfO0iCM')
