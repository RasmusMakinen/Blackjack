import random
import json

def getPakka():
    with open("korttipakka.txt", "r")as pakkafile:
        for rivi in pakkafile:
            pakka = rivi.split(",")
    return pakka
        
def jaaKortit():
    pakka = getPakka()
    pelaajaKortit = []
    dealerKortit = []
    for i in range(2):
        valittuKortti = random.choice(pakka)
        pelaajaKortit.append(valittuKortti)    #valitaan pelaajalle 2 korttia
        pakka.remove(valittuKortti)
        
        valittuKortti = random.choice(pakka)
        dealerKortit.append(valittuKortti)    #valitaan dealerille 2 korttia
        pakka.remove(valittuKortti)
    return pakka, pelaajaKortit, dealerKortit

def printPelaaja(pelaajaKortit): 
    print("Sinulla on kortit: ",end = "")
    for i in pelaajaKortit:
        print (i," ",end = "")
    print("")

def kortitStringiksi(kortit):
    kortitString=""
    for i in kortit:
        kortitString = kortitString+i+" "
    return kortitString

def printDealerEka(dealerKortit):
    print("Dealerilla on: ", dealerKortit[0])
    
def lisääKortti(pakka, pelaajaKortit):
    valittuKortti = random.choice(pakka)
    pelaajaKortit.append(valittuKortti)
    pakka.remove(valittuKortti)
    return pelaajaKortit, pakka
        
def mitenJatkuu(pakka,pelaajaKortit, dealerKortit): #kysyy miten pelaaja haluaa jatkaa kunnes holdaa tai luovuttaa
    tulos=1
    pelinTulos=""
    pelaajaYhteenlaskettu = evaluoiKäsi(pelaajaKortit)
    dealerYhteenlaskettu = evaluoiKäsi(dealerKortit)
    case=1
    if pelaajaYhteenlaskettu == 21:
        print ("Sait Blackjackin! Onneksi olkoon voitit! Blackjack maksaa 3 suhde 2.")
        return "blackjack"
    else:
        while case==1:
            case = input("\nKirjoita mitä haluat tehdä:\nNosta uusi kortti :1\nHold: 2\nLuovuta:3\n\n")
                 
            if case.isdigit() and case=="1" or case == "2" or case == "3":
                case=int(case)
                if case == 1: #nostat uuden kortin
                    print("nosta uusi kortti")
                    pelaajaKortit, pakka= lisääKortti(pakka, pelaajaKortit)
                    printPelaaja(pelaajaKortit)
                    if evaluoiKäsi(pelaajaKortit)>21:
                        print("Yli 21! Hävisit.")
                        return "häviö"
                        break
                elif case == 2: #hold
                    dealerNostaa(pakka, dealerKortit)
                    return kumpiVoitti(pelaajaKortit, dealerKortit)
                elif case == 3: #luovuta saa panos x 0,5
                    print("Luovutit. Saat pitää puolet panoksestasi.")
                    return "luovutus"
            else:
                case=1
                print("Syötä numero 1, 2 tai 3")
                
        
def evaluoiKäsi(kortit):   #Laskee korttien arvot yhteen. Jos on ässiä laskee ensin muut yhteen ja lisää lopussa 1 tai 11 riippuen summasta
    summa=0
    ässiä=0
    for i in kortit:
        if i.isnumeric():
            summa+=int(i)
        elif i == "J" or i == "Q" or i == "K" :
            summa+=10
        else:
            ässiä+=1
    for i in range(ässiä):
        if summa>10:
            summa+=1
        else:
            summa+=11
    return summa
        
def dealerNostaa(pakka,dealerKortit):
    print("Dealerillä on kortit",kortitStringiksi(dealerKortit))
    while evaluoiKäsi(dealerKortit)<16:
        dealerKortit, pakka =lisääKortti(pakka, dealerKortit)
        print("Dealer nosti kortin. Dealerillä on nyt",kortitStringiksi(dealerKortit))

def kumpiVoitti(pelaajaKortit, dealerKortit):
    printPelaaja(pelaajaKortit)
    if evaluoiKäsi(dealerKortit)>21:  #pelaaja voittaa
        print("Dealerin kortit ovat yli 21. Sinä voitit! Saat panoksen kaksinkertaisena takaisin.")
        return "voitto"
    elif evaluoiKäsi(dealerKortit)>evaluoiKäsi(pelaajaKortit):
        print("Dealeri oli lähempänä BlackJackia. Hävisit. Menetät panoksen")
        return "häviö"
    elif evaluoiKäsi(dealerKortit)<evaluoiKäsi(pelaajaKortit):
        print("Olit lähempänä BlackJackia. Voitit! Saat panoksen kaksinkertaisena takaisin.")
        return "voitto"
    elif evaluoiKäsi(dealerKortit)==evaluoiKäsi(pelaajaKortit):
        print("Tasapeli. Saat panoksesi takaisin")
        return "tasapeli"
    
def rahanMuutos(rahat, pelinTulos, panos): #muuttaa kokonaisrahamäärää tuloksen mukaan
    if pelinTulos=="blackjack":
        rahat+=panos*1.5
    elif pelinTulos=="voitto":
        rahat+=panos
    elif pelinTulos=="luovutus":
        rahat+= -panos/2
    elif pelinTulos=="häviö":
        rahat+= -panos
    print ("Sinulla on",rahat,"rahaa")
    print("")
    return rahat

def kysyPanos(kierros,raha):  
    print("Kierros",kierros,"alkaa:")
    print("Sinulla on",raha,"rahaa.")
    onkoValidi=1 
    while onkoValidi != 0:
        onkoValidi=0
        panos=input("Kuinka paljon haluat asettaa panokseksi? (max 50% rahoista)")
        for i in panos:
            if i=="." or i==",":
                print("Luku ei ole kokonaisluku. Syötä kokonaisluku")
                onkoValidi+=1
                       
        if onkoValidi==0:
            panos=int(panos)
            if panos>raha*0.5:
                print("Voit asettaa panokseksi max 50% rahoista")
                onkoValidi+=1
            
    print("Asetit panokseksi",panos,"€")            
    print("")
    return int(panos)

def tallennaTiedot(loppuRahat):  #kysyy pelaajalta nimen ja tallentaa pelaajan nimen ja pelaajan loppurahat JSON tiedostoon
    with open("blackjackscoreboard.json","r") as f:
        data=json.load(f)
        kaikki= data["henkilot"]
        nimi=input("Syötä nimi pelituloksesi tallentamista varten: ")
        uusiHenkilo={"nimi": nimi,
                     "tulos": loppuRahat
                     }
        kaikki.append(uusiHenkilo)
        kirjoitaJson(data)
        printtaaHighScore(data)
 
def kirjoitaJson(kaikki):
    with open("blackjackscoreboard.json","w") as f:
        json.dump(kaikki, f, indent=4)
    
def printtaaHighScore(data): #tulostaa parhaimmat pisteet saaneen pelaajan nimen ja tuloksen
    ennatys=-1.0
    voittaja=""
    for henkilo in data["henkilot"]: 
        tulos = henkilo["tulos"]
        if int(tulos) > int(ennatys):
            ennatys=tulos
            voittaja=henkilo["nimi"]
    print("Kaikkien aikojen parhaat pisteet: ",ennatys , "  ",voittaja)
    
################## SUORITUS ALKAA ##################
rahat=500.0
for kierros in range(1,6):
    panos=kysyPanos(kierros,rahat)
    pakka, pelaajaKortit, dealerKortit = jaaKortit()
    printPelaaja(pelaajaKortit)
    printDealerEka(dealerKortit)
    print("Korttiesi arvo on: ",evaluoiKäsi(pelaajaKortit))
    pelinTulos= mitenJatkuu(pakka,pelaajaKortit, dealerKortit)
    rahat=rahanMuutos(rahat, pelinTulos, panos)
print("Peli loppui! Sinun alkuperäinen 500€ on nyt",rahat,"€")
tallennaTiedot(rahat)
