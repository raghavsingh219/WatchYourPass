import random

equipment_gear = 'Fujifilm X-T4|Canon EOS R6|Nikon Z6 II|Sony A7 III|Nikon Z50|Fujifilm X100V|Sony A6100|Nikon D3500|Sony A7S III|Sony ZV-1|Canon EOS R5|GoPro Hero 9 Black|Olympus OM-D E-M5 Mark III|Panasonic Lumix S5|Nikon Z5|Fujifilm GFX 100|Canon EOS 1DX Mark III|Rubber Lens Cap|Powerbank|TTL Flash|Memory Card Holder|Flash Transmitter / Sync Lead|Camera Strap|Tripod|Remote|Camera Rig Case|Creative Filters|Grey Card|Lens Cleaner|Sensor Cleaner|Extra Batteries|Extra Memory Cards|Memory Card Reader|External Hard Drive|Reflector|Camera Bag|Tethering Cable|Manfrotto 190XPro4|Vanguard Veo 2 Go 265HCBM|Manfrotto XPRO Magnesium Ball Head with Top Lock plate|Vanguard Alta PH-32|Manfrotto Pixi Evo|Benro Adventure MAD38C Carbon Fiber Monopod|DJI Osmo Mobile 3|Adonit Photogrip|SYOSIN Selfie Stick Tripod|Peak Design Everyday Messenger 13 V2|Lowepro ProTactic BP 350 AW II backpack|Think Tank Digital Holster 10 v2.0|Peak Design Slide Summit Edition Strap|Hahnel Modus 600RT Mk II|Rotolight NEO II|Elinchrom D-Lite RX 4/4 To Go|Lastolite ePhotomaker kit - Large|Phottix EasyHold 5-in-1 Reflector 107cm|Hoya PRO1 Digital Circular PL|LEE Filters 100mm Neutral Density Grad Set|Cokin Nuances Extreme ND Z-Pro|Marumi DHG Vari ND2-ND400|K&F Concept Natural Night Filter Light Pollution Filter|LEE Filters LEE100 Holder|Rode VideoMic Go|Olympus LS-P4|Manfrotto Lumimuse 8 LED Light|DJI Ronin-SC|Manfrotto BeFree Live Lever Kit|Atomos Ninja V|SanDisk Extreme PRO SDXC UHS-I|SanDisk Extreme PRO CFexpress Card|WD My Passport|SanDisk Extreme Pro Portable SSD|Seagate Expansion Desktop 8TB|WD My Cloud EX2 Ultra NAS drive|Apple MacBook Pro 16-inch (2019)|Acer ConceptD 7|BenQ SW271|Dell UltraSharp PremierColor U3219Q|Datacolor SpyderX Pro|Logitech MX Master 3|Wacom One (2020)|Canon PIXMA Pro-100/100S|Plustek OpticFilm 8200i SE|Adobe Photoshop CC 2020|Adobe Premiere Elements 2020|VisibleDust EZ SwabLight Kit|Zeiss Lens Cleaning Wipes'

names = 'Abdul,Addison,Adena,Adrienne,Ahmed,Aidan,Alexander,Alfonso,Alfreda,Ali,Alice,Allistair,Alvin,Amal,Amery,Amy,Anne,Ariana,Armand,Arthur,Asher,Aubrey,Audra,Audrey,Barry,Berk,Bert,Blaze,Boris,Brady,Branden,Brent,Britanni,Buckminster,Buffy,Byron,Cairo,Caleb,Calvin,Cameron,Carl,Casey,Castor,Catherine,Chadwick,Chaim,Chandler,Charles,Charlotte,Chava,Cherokee,Cheryl,Christian,Christine,Christopher,Claire,Clare,Clayton,Clementine,Cleo,Clinton,Colby,Colette,Colt,Colton,Cora,Cruz,Curran,Cyrus,Dalton,Damon,Darius,Davis,Dawn,Deanna,Delilah,Denise,Dennis,Dieter,Dillon,Dorian,Dorothy,Drake,Ebony,Elaine,Eliana,Elmo,Emmanuel,Erasmus,Ethan,Ezekiel,Farrah,Ferris,Florence,Forrest,Gabriel,Gage,Galvin,Gary,Germane,Giacomo,Gil,Grace,Graham,Graiden,Gray,Guy,Hadley,Hamilton,Harlan,Hasad,Hayden,Hedwig,Hollee,Holmes,Honorato,Howard,Hu,Hyatt,Idona,Inez,Inga,Iola,Irma,Isabelle,Isaiah,Ishmael,Ivory,Ivy,Jada,Jakeem,James,Jesse,Jessica,Joan,Joel,Joelle,Jolie,Jonah,Jordan,Joshua,Joy,Julian,Karen,Kasimir,Katelyn,Kay,Keiko,Kellie,Kennedy,Kevyn,Kibo,Kieran,Lacy,Lane,Larissa,Laurel,Lawrence,Len,Leonard,Lev,Lilah,Lionel,Louis,Lucian,Lucius,Luke,Lydia,Lyle,Lynn,Macon,Madaline,Magee,Malachi,Mannix,Marsden,Maryam,Mason,Matthew,Maxine,Maxwell,Maya,Mohammad,Moses,Murphy,Nash,Nasim,Neil,Nicholas,Nina,Noah,Nolan,Octavia,Octavius,Oprah,Ori,Oscar,Otto,Owen,Palmer,Pamela,Patricia,Peter,Porter,Quinlan,Quinn,Rae,Raja,Ralph,Rashad,Ray,Raymond,Reese,Roary,Robert,Ronan,Roth,Ruby,Rudyard,Ryder,Rylee,Sara,Sean,Sebastian,Seth,Shaeleigh,Shea,Sheila,Slade,Sonia,Stacey,Stephen,Steven,Stone,Stuart,Talon,Tamara,Tanya,Thane,Tobias,Trevor,Ulric,Uriah,Ursula,Wallace,Warren,Wayne,Wesley,Whilemina,Whoopi,Wing,Yael,Yardley,Yoko,Zachary,Zelenia,Zenaida,Zeph'

list_to_write = []
equipment_gear_list = equipment_gear.split("|")
names_list = names.split(",")

for x in range(10000):
    list_to_write.append(random.choice(names_list) + " | " + random.choice(equipment_gear_list) + " | " + random.choice(equipment_gear_list))

with open('generated_data.txt', 'a+') as filehandle:
    filehandle.writelines("%s\n" % line for line in list_to_write)
