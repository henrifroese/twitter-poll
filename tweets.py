#@PydevCodeAnalysisIgnore
'''
Created on Nov 7, 2019

@author: henri
'''
import json
from TwitterSearch import *
import datetime
import linecache
import math
from nltk.corpus import stopwords
import string
from string import punctuation
from os import listdir
from collections import Counter
import numpy
import matplotlib.pyplot

import keyfile


def mainsearch(usernames):

    ts = TwitterSearch(
        consumer_key = keyfile.consumer_key,
        consumer_secret = keyfile.consumer_secret,
        access_token = keyfile.access_token,
        access_token_secret = keyfile.access_token_secret
     )

    tokens_all_users = list()

    for username in usernames:

        try:

            tuo = TwitterUserOrder(username)
            tuo.set_include_rts(False)  # ?
            # tuo.set_count(20) does not seem to work -> use enumerate

            tokens_user = list()

            for index, tweet in enumerate(ts.search_tweets_iterable(tuo)):

                tweet_content = tweet['text']
                table = str.maketrans('', '', string.punctuation)
                # tokenize and remove punctuation and lowercase 
                tweet_content = [word.translate(table).lower() for word in tweet_content.split()] 

                # remove non-alphanumeric and short words and filter out stop words
                stop_words = set(stopwords.words('german'))
                tweet_content = [word for word in tweet_content if word.isalpha() and len(word) > 2 and word not in stop_words]                

                tokens_user += tweet_content

                if index == 99:  # 100 tweets per user
                    break

        except TwitterSearchException as e:  # take care of errors
            print(e, username)

        tokens_all_users.append(tokens_user)

    return tokens_all_users  # list of lists (each list containing tokens of one user)


def singlesearch(username):

    ts = TwitterSearch(
        consumer_key = keyfile.consumer_key,
        consumer_secret = keyfile.consumer_secret,
        access_token = keyfile.access_token,
        access_token_secret = keyfile.access_token_secret
     )

    try:

        tuo = TwitterUserOrder(username)
        tuo.set_include_rts(False)  
        # tuo.set_count(20) does not seem to work -> use enumerate
    
        tokens_user = list()
    
        for index, tweet in enumerate(ts.search_tweets_iterable(tuo)):
    
        	tweet_content = tweet['text']
        	table = str.maketrans('', '', string.punctuation)
        	# tokenize and remove punctuation and lowercase 
        	tweet_content = [word.translate(table).lower() for word in tweet_content.split()] 
        
        	# remove non-alphanumeric and short words and filter out stop words
        	stop_words = set(stopwords.words('german'))
        	tweet_content = [word for word in tweet_content if word.isalpha() and len(word) > 2 and word not in stop_words]                
        
        	tokens_user += tweet_content
        
        	if index == 99:  # 100 tweets per user
        	    break
    
    except TwitterSearchException as e:  # take care of errors
        print(e, username)
        
    return tokens_user  #  list containing user's tokens



def predict_party(twitter_username, model, vocab):
  user_tokens = singlesearch(twitter_username)
  user_tokens = [token for token in user_tokens if token in vocab]
  user_tokens = ' '.join(user_tokens)
  return user_tokens
print(predict_party('realdonaldtrump', None, ['But', 'the', 'Witch', 'hunt']))



'''
cdu_list = ['rbrinkhaus', 'SteinekeCDU', 'jensspahn', 'groehe', 'HHirte',
'MBiadaczMdB', 'Erwin_Rueddel', 'RKiesewetter', 'christophploss', 'DrAndreasNick',
'Dr_Roy_Kuehne', 'MGrosseBroemer', 'JM_Luczak', 'TinoSorge', 'akk', 'PaulZiemiak',
'JuliaKloeckner', 'ArminLaschet', 'vonderleyen', 'MPKretschmer', 'MikeMohring',
'caspary', 'AxelVossMdEP', '_FriedrichMerz', 'peteraltmeier', 'petertauber',
'SvenVolmering', 'tschipanski', 'DWoehrl', 'StefanKaufmann',
'PSchnieder', 'UweSchummer', 'erwin_rueddel', 'koschyk', 'peersteinbrueck',
'groehe', 'schroeder_k', 'MGrosseBroemer', 'NadineSchoen',
'berndfabritius', 'SteinekeCDU', 'mechthildheil', 'TinaSchwarzer',
'marcusweinberg', 'julia_obermeier', 'wanderwitz', 'MatthiasHauer',
'Axel_Fischer', 'plengsfeld', 'VolkerUllrich',
'BettinaHornhues', 'helmut_nowak', 
'matthiaszimmer', 'berndsiebert', 'tj_tweets', 'missfelder',
'drmfuchs', 'meister_schafft', 'christianhirte', 'fuchtel',
'juergenhardt', 'tschipanski', 'MaikBeermann', 'charlesmhuber49', 'ninawarken',
'SylviaPantel', 'XaverJung', 'PatrickSensburg',
'frankheinrich', 'Wellenreuther', 'guenterkrings',
'Manfredbehrens', 'jungfj', 'KLeikert',
'anjaweisgerber', 'HGundelach', 'GudrunZollner',
'amattfeldt', 'davidmcallister', 'Missfelder', 'GOettingerEU',
'NadineSchoen', 'schroeder_k', 'UweSchummer'] #  from CDU

greens_list = ['ABaerbock', 'GoeringEckardt', 'svenlehmann', 'AnjaSiegesmund', 
'MiKellner', 'Gesine_Agena', 'bueti', 'sven_giegold', 'L_Petersdotter', 'UNonnemacher', 
'jamila_anna', 'SkaKeller', 'Ben_Raschke', 'Ka_Meier', 'Gruen_WGuenther', 'RenateKuenast',
'sven_kindler', 'KonstantinNotz', 'cem_oezdemir', 'JTrittin', 'HajdukBundestag', 'K_SA', 
'BriHasselmann', 'GruenSprecher', 'beatewaro', 'W_SK', 'katjadoerner', 'oezcanmutlu', 'steffilemke',
'BabettesChefin', 'LisaPaus', 'TabeaRoessner', 'Volker_Beck', 'DJanecek', 'monikalazar',
'ekindeligoez', 'mdb_stroebele', 'steffilemke', 'BaerbelHoehn', 'Volker_Beck',
'tobiaslindner', 'KaiGehring', 'nouripour', 'kerstinandreae', 'ekindeligoez',
'GrueneBeate', 'WilmsVal', 'katjadoerner', 'NicoleMaisch', 'DJanecek', 'ManuelSarrazin',
'Luise_Amtsberg', 'ebner_sha', 'IreneMihalic', 'Oliver_Krischer',
'ulle_schauws', 'julia_verlinden', 'katdro', 'Uwekekeritz', 'beatewaro',
'BabettesChefin', 'BrigittePothmer', 'crueffer', 'DorisWagner_MdB', 'monikalazar',
'KoenigsGruen', 'fbrantner', 'MarieluiseBeck', 'markuskurthmdb', 'StarkeRegionen',
'peter_simone', 'JanAlbrecht', 'bueti', 'sven_giegold', 'WinneHermann',
'ToniHofreiter', 'stephankuehn', 'KathaSchulze'] #  from Greens

spd_list = ['Karl_Lauterbach', 'kahrs', 'EvaHoegl', 'KatjaMast', 'OlafScholz', 
'Achim_P', 'soerenbartol', 'baerbelbas', 'JensZimmermann1', 'HeikoMaas', 'NilsSchmid', 
'thomashitschler', 'schneidercar', 'SvenjaSchulze68', 'MarjaVoellers', 'EskenSaskia', 
'NilsSchmid', 'FrankSchwabe', 'hubertus_heil', 'sigmargabriel', 'Ralf_Stegner', 'larsklingbeil', 
'KarambaDiaby', 'Lothar_Binding', 'UlrichKelber', 
'ManuelaSchwesig', 'MiRo_SPD', 'g_reichenbach', 'thomashitschler',
'ThomasOppermann', 'florianpronold', 'FrankeEdgar', 'KerstinGriese',
'SCLemme', 'michaelaengel', 'PErnstberger', 'UlliNissen', 'Schwarz_MdB', 'Elke_Ferner',
'danielakolbe', 'swenschulz', 'achim_p', 'MetinHakverdi', 'NielsAnnen', 
'HildeMattheis', 'c_kampmann', 'ChristianFlisek', 'MartinRosemann', 'michael_thews',
'brigittezypries', 'rainerarnold', 'RebmannMdB', 'juergencosse',
'FlorianPost', 'W_Priesmeier', 'SusannRuethrich', 'BetMueller',
'michaelgrossmdb', 'marcobuelow', 'edrossmann',
'rischwasu', 'dieschmidt', 'GabiWeberSPD',
'JensZimmermann1', 'DennisRohde', 'AnnetteSawade', 'oezdemir_spd',
'GabyKatzmarek', 'ThomasHitschler', 'fritzfelgentreu', 'larscastellucci',
'zierke', 'HiltrudLotze', 'arnoklare', 'MalechaNissen', 'A_Gloeckner',
'Aschenbrennerin', 'GescheJoost', 'MartinSchulz', 'KazunguHass', 'Alex_Schweitzer',
'MartinRosemann', 'D_Stich', 'Sabine_Baetzing', 'JensZimmermann1', 'UlliNissen',
'Schwarz_MdB', 'Achim_P', 'LangeMdB', 'sebast_hartmann', 'KerstinGriese',
'KaczmarekOliver', 'KuehniKev'] # from SPD

afd_list = ['Joerg_Meuthen', 'UlrichSiegmund', 'Alice_Weidel', 'UdoHemmelgarn', 
'Joerg_UrbanAfD', 'M_Reichardt_AfD', 'Georg_Pazderski', 'PoggenburgAndre', 'GottfriedCurio', 
'GtzFrmming', 'gunnar_beck', 'BjoernHoecke', 'M_HarderKuehnel', 
'Leif_Erik_Holm', 'Frank_Pasemann', 'WMuhsal', 'torben_braga', 'StBrandner', 'Beatrix_vStorch', 
'JoanaCotar', 'AndreasBleckMdB', 'DirkSpaniel', 'Renner_AfD', 'DroeseSigbert',
'WolfgangWiehle', 'DrHollnagel', 'MdB_Mueller_AfD', 'JoernKoenigAfD', 'Jacobi_AfD',
'VerHartmannAfD', 'Frank_Magnitz', 'HuberMdB', 'HilseMdB', 'ChrWirthMdB',
'Martin_Sichert', 'JuergenBraunAfD', 'KestnerJens', 'JensMaierAfD',
'DrFriesenMdB', 'Th_Seitz_AfD', 'SteffenKotre', 'EspendillerM',
'Buettner_MdB', 'MartinHess_AfD', 'CorinnaMiazga', 'NKleinwaechter',
'S_Muenzenmaier', 'UdoHemmelgarn', 'h_weyel', 'Rene_Springer',
'ProfMaier', 'JoanaCotar', 'PetrBystronAfD', 'DirkSpaniel',
'MarcBernhardAfD', 'Dr_Rainer_Kraft', 'Tino_Chrupalla', 'StefanKeuterAfD',
'EnricoKomning', 'Gerold_Otten', 'Paul_Podolay', 'Marcus_Buehl',
'Schneider_AfD', 'Jochen_Haug', 'MdB_Lucassen', 'Witt_Uwe',
'ElsnervonGronow', 'Frohnmaier_AfD', 'Marc_Jongen', 'Jan_Nolte_AfD',
'WaldemarHerdt', 'Ulrich_Oehme', 'ThomasEhrhorn', 'Nicole_Hoechst',
'mrosek1958', 'M_Reichardt_AfD', 'TobiasMPeterka', 'MalsackWinkeman',
'axelgehrke', 'ttte94', 'Frank_Pasemann', 'AfDProtschka',
'KayGottschalk1'] #  from AfD

linke_list = ['b_riexinger', 'DietmarBartsch', 'katjakipping', 'SWagenknecht', 'GregorGysi', 
'bodoramelow', 'JoergSchindler', 'FabioDeMasi', 'ernst_klaus', 'MartinaRenner', 'CarenLay', 
'SusanneHennig', 'sebastiank', 'NordMdB', 'NiemaMovassat', 'DorisAchelwilm', 'ZaklinNastic',
'KirstenTackmann', 'SevimDagdelen', 'PetraPauMaHe', 'MichaelLeutert', 'berlinliebich',
'SusanneFerschl', 'LINKEPELLI', 'Petra_Sitte_MdB', 'Halina_Waw', 'Halina_Waw', 'voglerk',
'MichaelLeutert', 'MWBirkwald', 'MartinaRenner', 'Team_GLoetzsch', 'ernst_klaus',
'Diether_Dehm', 'AndrejHunko', 'Katrin_Werner', 'AlexanderSNeu', 'UllaJelpke',
'JuttaKrellmann', 'ch_buchholz', 'HeikeHaensel', 'katrinbinder', 'JuttaKrellmann'
, 'martina_michels', 'Andi_Wagner', 'SusanneFerschl', 'jessica_tatti',
'Amira_M_Ali', 'AkbulutGokay', 'F_Brychcy', 'FrStraetmanns', 'MdB_Schreiber',
'MdB_Freihold', 'HESommer', 'Ingrid_Remmers', 'victorperli', 'pascalmeiser',
'AchimKesslerMdB', 'SylviaGabelmann', 'joerg_cezanne', 'michael_brandt',
'lgbeutin', 'SBarrientosK', 'DorisAchelwilm', 'CanselK', 'SeeroiberJenny',
'CansuOezdemir'] #  from LINKE

fdp_list = ['G_UllrichFDP', 'rock_fdp', 'MarcoBuschmann', 'c_lindner', 'KemmerichThL',
'nicolabeerfdp', 'LindaTeuteberg', 'Lambsdorff', 'KonstantinKuhle', 'johannesvogel',
'DFoest', 'ChristophFDP', 'k_willkomm', 'starkwatzinger', 'f_schaeffler', 
'jimmyschulz', 'EUTheurer', 'MarcusFaber', 'torstenherbst', 'OlliLuksic',
'koehler_fdp', 'HoffmannForest', 'KatjaSuding', 'MAStrackZi', 'danielbahr',
'lassebecker', 'ManuelHoeferlin', 'sls_fdp', 'Andi_Glueck', 'CGrascha',
'krstdt', 'AGBuelow', 'moritzkoerner', 'tinademeeus', 'jcoetjen', 'nicole_ae_bauer',
'DanielaKluckert', 'jensbeeck', 'UllmannMdB', 'th_sattelberger', 'GydeJ',
'muellerboehm', 'c_jung77', 'BraFDP', 'HoubenReinhard', 'WSchinnenburg',
'JBrandenburgFDP', 'sandra_weeser', 'carina_konrad', 'koehler_fdp',
'olafinderbeek', 'HartmutEbbing', 'reinholdmdb', 'reuther_bernd',
'G_UllrichFDP', 'busen_mdb', 'alexmuellerfdp', 'JudithSkudelny',
'TillMansmann', 'DjirSarai', 'GeroHocker', '_MartinNeumann',
'aggelidis_fdp', 'theliberalfrank', 'ulrichlechte', 'NicoleWestig',
'MdBKlein', 'HerbrandMarkus', 'BrittaDassler', 'RenataAlt_MdB',
'realMartinHagen', 'starkwatzinger', 'rock_fdp', 'hoffmann_fdp',
'StephanThomae', 'KH_Paque', 'j_huettl', 'bstrasser', 'nicolabeerfdp'] #  from FDP


cdu_tokens    = [usertweet for usertweet in mainsearch(cdu_list) if usertweet != []]
spd_tokens    = [usertweet for usertweet in mainsearch(spd_list) if usertweet != []]
afd_tokens    = [usertweet for usertweet in mainsearch(afd_list) if usertweet != []]
fdp_tokens    = [usertweet for usertweet in mainsearch(fdp_list) if usertweet != []]
linke_tokens  = [usertweet for usertweet in mainsearch(linke_list) if usertweet != []]
greens_tokens = [usertweet for usertweet in mainsearch(greens_list) if usertweet != []]


with open('data/cdu_tokens.txt', 'w') as f:
    for usertokens in cdu_tokens:
        f.write("%s\n" % ' '.join(usertokens))

with open('data/spd_tokens.txt', 'w') as f:
    for usertokens in spd_tokens:
        f.write("%s\n" % ' '.join(usertokens))

with open('data/afd_tokens.txt', 'w') as f:
    for usertokens in afd_tokens:
        f.write("%s\n" % ' '.join(usertokens))

with open('data/fdp_tokens.txt', 'w') as f:
    for usertokens in fdp_tokens:
        f.write("%s\n" % ' '.join(usertokens))

with open('data/linke_tokens.txt', 'w') as f:
    for usertokens in linke_tokens:
        f.write("%s\n" % ' '.join(usertokens))
with open('data/greens_tokens.txt', 'w') as f:
    for usertokens in greens_tokens:
        f.write("%s\n" % ' '.join(usertokens))'''
