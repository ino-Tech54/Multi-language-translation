import pandas as pd

# Create the dataset with corrected structure
data = [
    # Project & Technical Questions
    {
        "English Sentence": "How does this translation project work?",
        "Shona Subtitle": "Purojekiti Yekushandura",
        "Shona Translation": "Iri purojekiti yekushandura inoshanda sei?",
        "Ndebele Subtitle": "Iphrojekthi Yokuhumusha",
        "Ndebele Translation": "Lolu phrojekthi yokuhumusha lusebenza kanjani?"
    },
    {
        "English Sentence": "What was the main goal when you started developing this system?",
        "Shona Subtitle": "Chinangwa Chepurojekiti",
        "Shona Translation": "Chinangwa chikuru changa chiri chii pawakatanga kugadzira iyi system?",
        "Ndebele Subtitle": "Injongo Yephrojekthi",
        "Ndebele Translation": "Iyiphi injongo eyayiyinhloko lapho niqala ukwakha lolu hlelo?"
    },
    {
        "English Sentence": "Can you explain the technology behind this real-time translation service?",
        "Shona Subtitle": "Tekinoroji Yekushandura",
        "Shona Translation": "Ungatsanangure tekinoroji iri kushanda kweiyi real-time translation service here?",
        "Ndebele Subtitle": "Ubuchwepheshe Bokuhumusha",
        "Ndebele Translation": "Ungachaza ibuchwepheshe obusetshenziswa yilesi sevisi yokuhumusha yesikhathi sangempela?"
    },
    {
        "English Sentence": "What challenges did you face in collecting data for languages like Shona and Ndebele?",
        "Shona Subtitle": "Matambudziko Ekuunganidza Data",
        "Shona Translation": "Matambudziko makuru amiwe here pawaiunganidza data yemitauro mishoma seShona neNdebele?",
        "Ndebele Subtitle": "Izinkinga Zokuqoqa Idatha",
        "Ndebele Translation": "Yiziphi izinkinga enizibekele phezulu lapho niqoqa idatha yolimi olunamathuluzi amancane njengesiNdebele nesiShona?"
    },

    # About Midlands State University (MSU)
    {
        "English Sentence": "What are the entry requirements for an undergraduate degree in Medicine at Midlands State University?",
        "Shona Subtitle": "Zvinodiwa Kuenda KuMSU",
        "Shona Translation": "Ndezvipi zvinodiwa kuti upinde dhigirii reMedicine paMidlands State University?",
        "Ndebele Subtitle": "Izidingo Zokungena EMSU",
        "Ndebele Translation": "Yiziphi izidingo zokungena kwezifundo zezokwelapha eMidlands State University?"
    },
    {
        "English Sentence": "Can you tell me about the accommodation facilities at the MSU Gweru main campus?",
        "Shona Subtitle": "Dzimba Dzekugara PaMSU",
        "Shona Translation": "Ungandiudza here nezve dzimba dzekugara paMSU Gweru main campus?",
        "Ndebele Subtitle": "Izindawo Zokuhlala EMSU",
        "Ndebele Translation": "Ungangitshela yini ngezindawo zokuhlala eMSU Gweru main campus?"
    },
    {
        "English Sentence": "How has MSU contributed to agricultural research in the Midlands province?",
        "Shona Subtitle": "MSU Nezvekurima",
        "Shona Translation": "MSU yakabatsira sei mukutsvagurudza zvekurima mudunhu reMidlands?",
        "Ndebele Subtitle": "IMSU Nezolimo",
        "Ndebele Translation": "IMSU ibe ngalutho kanjani ekucwaningeni kwezolimo esifundazweni saseMidlands?"
    },

    # Current News & Affairs
    {
        "English Sentence": "What are the main points from the recent national budget presentation by the Minister of Finance?",
        "Shona Subtitle": "Bhajeti Yenyika",
        "Shona Translation": "Ndeapi mapoinzi makuru kubva mubhajeti yenyika ichangoburwa yakaturikwa naMinister of Finance?",
        "Ndebele Subtitle": "Isabelomali Sikazwelonke",
        "Ndebele Translation": "Yiziphi izinto eziyinhloko ezivela kusabelomali sakamuva sezwe esethulwa nguNgqongqoshe Wezezimali?"
    },
    {
        "English Sentence": "How is the government addressing the current drought situation affecting farmers across the country?",
        "Shona Subtitle": "Kusanaya Kwemvura",
        "Shona Translation": "Hurumende iri kuita sei kugadzirisa kusanaya kwemvura kwazvino kuri kukanganisa varimi munyika yose?",
        "Ndebele Subtitle": "Isomiso Samanje",
        "Ndebele Translation": "Uhulumeni wenza kanjani ukubhekana nesimo sesomiso samanje esithinta abalimi kuzwelonke?"
    },
    {
        "English Sentence": "Could you summarize the latest developments in renewable energy projects in Southern Africa?",
        "Shona Subtitle": "Magetsi Anovandudzwa",
        "Shona Translation": "Ungapfupisa here zvirikuitika zvitsva mumapurojekiti emagetsi anovandudzwa muSouthern Africa?",
        "Ndebele Subtitle": "Amandla Avuselelekayo",
        "Ndebele Translation": "Unganciphisa yini izinguquko ezintsha kumaphrojekthi wamandla avuselelekayo eSouthern Africa?"
    },

    # Social Media & Digital Life
    {
        "English Sentence": "Why do some videos go viral on TikTok while others with similar content do not get any views?",
        "Shona Subtitle": "Mavhidhiyo Anobuda Pachena",
        "Shona Translation": "Sei mamwe mavhidhiyo achibuda pachena paTikTok asi mamwe ane zvakafanana asingatariswe?",
        "Ndebele Subtitle": "Amavidiyo Adumile",
        "Ndebele Translation": "Kungani amanye amavidiyo edlula athandwa kakhulu eTikTok kanti amanye anokuqukethwe okufanayo angabukeki?"
    },
    {
        "English Sentence": "How can I protect my privacy and personal data on platforms like Facebook and Instagram?",
        "Shona Subtitle": "Kuchengetedza Zvako Pamasocial Media",
        "Shona Translation": "Ndingadzivirira sei zvangu nedata rangu paFacebook neInstagram?",
        "Ndebele Subtitle": "Ukuvikelela Emasoshal Media",
        "Ndebele Translation": "Ngingazivikela kanjani ngedatha yami eFacebook nase-Instagram?"
    },
    {
        "English Sentence": "Explain the concept of an 'echo chamber' that can form on social media platforms.",
        "Shona Subtitle": "Echo Chamber Mumasocial Media",
        "Shona Translation": "Tsanangudza pfungwa ye 'echo chamber' inogona kuumbwa pamasocial media platform.",
        "Ndebele Subtitle": "I-Echo Chamber Kumasoshal Media",
        "Ndebele Translation": "Chaza umqondo we-'echo chamber' ongakheka kumasoshal media platform."
    },

    # Daily Life & Interactions
    {
        "English Sentence": "Could you give me a simple recipe for making a traditional peanut butter stew with spinach?",
        "Shona Subtitle": "Recipe Yemuto Wepeanut Butter",
        "Shona Translation": "Ungandipa here recipe iri nyore yekugadzira muto wechinyakare wepeanut butter nespinachi?",
        "Ndebele Subtitle": "Irecipe Yesobho Yepeanut Butter",
        "Ndebele Translation": "Unganginika irecipe elula yokwenza isobho yendabuko yepeanut butter nespinashi?"
    },
    {
        "English Sentence": "What is the most effective way to remove a red wine stain from a white cotton tablecloth?",
        "Shona Subtitle": "Kubvisa Ruvara Rewaini",
        "Shona Translation": "Ndeipi nzira inoshanda kwazvo yekubvisa ruvara rwewaini tsvuku pajira retafura chena?",
        "Ndebele Subtitle": "Ukususa Ibala Lewayini",
        "Ndebele Translation": "Iyiphi indlela esebenza kahle kakhulu yokususa ibala lewayini elibomvu endwangu yetafula emhlophe?"
    },
    {
        "English Sentence": "I'm planning a road trip to Victoria Falls next month, what are some essential items I should pack?",
        "Shona Subtitle": "Rwendo KuVictoria Falls",
        "Shona Translation": "Ndiri kuronga rwendo rwemumugwagwa kuenda kuVictoria Falls mwedzi unouya, ndipfakerei zvinhu zvakakosha?",
        "Ndebele Subtitle": "Uhambo Oluya EVictoria Falls",
        "Ndebele Translation": "Ngiyahlola uhambo lwasemgwaqweni oluya eVictoria Falls ngenyanga ezayo, ngifake izinto ezisemqoka ziphi?"
    },

    # Business & Economics
    {
        "English Sentence": "What are the key differences between a sole proprietorship and a private limited company?",
        "Shona Subtitle": "Mhando Dzebhizimisi",
        "Shona Translation": "Ndeupi musiyano mukuru pakati pekuita bhizimisi wega nekambani yega?",
        "Ndebele Subtitle": "Izinhlobo Zamabhizinisi",
        "Ndebele Translation": "Uyini umehluko omkhulu phakathi kokuba ngumnikazi wedwa nenkampani yangasese?"
    },
    {
        "English Sentence": "Explain the concept of inflation in simple terms for a small business owner.",
        "Shona Subtitle": "Inflation Nemabhizimisi",
        "Shona Translation": "Tsanangudza inflation nemashoko akapfava kumuridzi webhizimisi diki.",
        "Ndebele Subtitle": "Inflation Namabhizinisi",
        "Ndebele Translation": "Chaza ukwehla kwamandla emali ngamazwi alula kumnikazi webhizinisi omncane."
    },

    # Technology & Science
    {
        "English Sentence": "How do solar panels actually convert sunlight into usable electricity for a home?",
        "Shona Subtitle": "Masolar Panel Nemagetsi",
        "Shona Translation": "Masolar panel anoshandura sei chiedza chezuva kuita magetsi anoshanda kumba?",
        "Ndebele Subtitle": "Amaphaneli Elanga Nogesi",
        "Ndebele Translation": "Amaphaneli elanga ashintsha kanjani ukukhanya kwelanga kube ugesi osebenziseka endlini?"
    },
    {
        "English Sentence": "What is artificial intelligence and how is it different from machine learning?",
        "Shona Subtitle": "Artificial Intelligence",
        "Shona Translation": "Chii chinonzi artificial intelligence uye chinosiyana sei nemachine learning?",
        "Ndebele Subtitle": "Ubuhlakani Bokwenziwa",
        "Ndebele Translation": "Yini i-artificial intelligence futhi ihluke kanjani ekufundeni komshini?"
    },

    # Health & Wellness
    {
        "English Sentence": "Can you explain the symptoms and prevention methods for high blood pressure?",
        "Shona Subtitle": "BP Yepamusoro",
        "Shona Translation": "Ungatsanangura here zviratidzo uye nzira dzekudzivirira BP yepamusoro?",
        "Ndebele Subtitle": "Igazi Elinomfutho",
        "Ndebele Translation": "Ungachaza yini izimpawu nezindlela zokuvikela igazi elinomfutho?"
    },
    {
        "English Sentence": "What are the health benefits of regular exercise and a balanced diet?",
        "Shona Subtitle": "Kurovedza Muviri Nekudya",
        "Shona Translation": "Ndezvipi zvakanakira hutano zvekurovedza muviri nguva dzose uye kudya zvakafanana?",
        "Ndebele Subtitle": "Ukuzilolongela Nokudya",
        "Ndebele Translation": "Yiziphi izinzuzo zezempilo zokuzivocavoca njalo nokudya okulinganayo?"
    },

    # Education & Learning
    {
        "English Sentence": "What are the most effective strategies for learning a new language as an adult?",
        "Shona Subtitle": "Kudzidza Mutauro Mitsva",
        "Shona Translation": "Ndeapi marongero anoshanda kwazvo ekudzidza mutauro mutsva semunhu mukuru?",
        "Ndebele Subtitle": "Ukufunda Ulimi Olusha",
        "Ndebele Translation": "Yiziphi izindlela eziphumelelayo zokufunda ulimi olusha njengomuntu omdala?"
    },
    {
        "English Sentence": "How does the education system in Zimbabwe prepare students for the digital economy?",
        "Shona Subtitle": "Dzidzo MuZimbabwe",
        "Shona Translation": "Hurongwa hwedzidzo muZimbabwe hunogadzirira sei vadzidzi kune digital economy?",
        "Ndebele Subtitle": "Imfundo EZimbabwe",
        "Ndebele Translation": "Uhlelo lwezemfundo eZimbabwe lulungiselela kanjani abafundi kwezamabhizinisi edijithali?"
    },

    # Culture & Traditions
    {
        "English Sentence": "What is the historical significance of the Great Zimbabwe ruins to the Shona people?",
        "Shona Subtitle": "Matongo EGreat Zimbabwe",
        "Shona Translation": "Chii chakakosha munhoroondo yematongo eGreat Zimbabwe kuvanhu vechiShona?",
        "Ndebele Subtitle": "Amanxiwa EGreat Zimbabwe",
        "Ndebele Translation": "Yini okubalulekile emlandweni wamanxiwa eGreat Zimbabwe kubantu baseShona?"
    },
    {
        "English Sentence": "Can you describe the traditional Ndebele ceremony of umabo and its importance?",
        "Shona Subtitle": "Umabo YeNdebele",
        "Shona Translation": "Ungatsanangura here mutambo wechinyakare weNdebele weumabo nekukosha kwawo?",
        "Ndebele Subtitle": "Umabo WamaNdebele",
        "Ndebele Translation": "Ungachaza yini umkhosi wendabuko wamaNdebele wokwendiswa nokubaluleka kwawo?"
    },

    # Environment & Sustainability
    {
        "English Sentence": "How can communities promote environmental conservation in urban areas?",
        "Shona Subtitle": "Kuchengetedza Zvakatipoteredza",
        "Shona Translation": "Nharaunda dzingasimudzira sei kuchengetedzwa kwezvakatipoteredza mumadhorobha?",
        "Ndebele Subtitle": "Ukuvikelwa Kwemvelo",
        "Ndebele Translation": "Imiphakathi ingakhuthaza kanjani ukongiwa kwemvelo emadolobheni?"
    },
    {
        "English Sentence": "What are the main causes and effects of deforestation in Southern Africa?",
        "Shona Subtitle": "Kuparadzwa Kwemasango",
        "Shona Translation": "Ndezvipi zvikonzero nemigumisiro yekuparadzwa kwemasango muSouthern Africa?",
        "Ndebele Subtitle": "Ukuqothulwa Kwamahlathi",
        "Ndebele Translation": "Yiziphi izimbangela nemiphumela yokuqothulwa kwamahlathi eSouthern Africa?"
    },

    # Travel & Tourism
    {
        "English Sentence": "What are the must-visit cultural heritage sites in Zimbabwe for international tourists?",
        "Shona Subtitle": "Nzendo DzekuZimbabwe",
        "Shona Translation": "Ndeapi nzvimbo dzenhaka dzinofanirwa kushanyirwa nevashanyi vekune dzimwe nyika muZimbabwe?",
        "Ndebele Subtitle": "Ukuvakasha EZimbabwe",
        "Ndebele Translation": "Yiziphi izindawo zamasiko okufanele zivakashwe abavakashi bakwamanye amazwe eZimbabwe?"
    },
    {
        "English Sentence": "How has tourism recovery been progressing since the pandemic restrictions were lifted?",
        "Shona Subtitle": "Kudzoka Kwevashanyi",
        "Shona Translation": "Kudzoka kwevashanyi kwave kufambira mberi sei kubva pazvirambidzo zvedenda zvabviswa?",
        "Ndebele Subtitle": "Ukuvuselelwa Kwezokuvakasha",
        "Ndebele Translation": "Ukuvuselelwa kwezokuvakasha kuhambisene kanjani kusukela izithiyo zobhadane zasuswa?"
    }
]

# Create DataFrame
df = pd.DataFrame(data)

# Save to Excel
file_path = "multilingual_translation_dataset.xlsx"
df.to_excel(file_path, index=False, engine='openpyxl')

print(f"Dataset successfully created with {len(df)} entries!")
print(f"File saved as: {file_path}")

# Display sample of the data
print("\nSample of the dataset:")
print("=" * 100)
for i, row in df.head(10).iterrows():
    print(f"\n{i+1}. ENGLISH: {row['English Sentence']}")
    print(f"   SHONA SUBTITLE: {row['Shona Subtitle']}")
    print(f"   SHONA TRANSLATION: {row['Shona Translation']}")
    print(f"   NDEBELE SUBTITLE: {row['Ndebele Subtitle']}")
    print(f"   NDEBELE TRANSLATION: {row['Ndebele Translation']}")
    print("-" * 100)

print(f"\nTotal entries in dataset: {len(df)}")
print("\nDataset structure:")
print(df.info())