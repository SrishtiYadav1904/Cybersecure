import os
import csv
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

# Comprehensive sample pools across all 10 classes
# Balanced across English, Hindi (Devanagari), and Hinglish (Roman Hindi)

DATA_POOLS = {
    "Age-based": {
        "English": [
            "You boomer grandma, you are too old to understand anything.",
            "Look at this little child pretending to know about the real world.",
            "Grandma please retire from the internet, your brain is melting.",
            "Stupid teenager should not have an opinion on politics.",
            "Ok boomer, go take your dementia pills and leave social media.",
            "You are an ancient relic with zero relevance in today's world.",
            "Little kid go finish your elementary school homework first.",
            "Why is a 70 year old trying to act cool on the internet, so cringe.",
            "Old people like you ruined the economy and now you lecture us.",
            "Immature toddler crying on twitter, go drink some milk.",
            "You are too decrepit to operate a smartphone properly.",
            "Old hag needs to shut her mouth and stay in a nursing home.",
            "Kids these days have no brains, just scrolling tiktok all day.",
            "You are way past your expiration date old man.",
            "Kindergarten child trying to argue with adults online.",
            "Dumb boomer technology is too advanced for your primitive brain.",
            "Go back to your rocking chair grandpa, your era is finished.",
            "Underage brats should be banned from all online forums.",
            "Look at this ancient dinosaur giving outdated advice.",
            "Grow up first kiddo before trying to debate grown men."
        ],
        "Hindi": [
            "बुड्ढे सठिया गए हो, अब तुम्हारी कोई औकात नहीं है।",
            "बच्चा है अभी, जाके स्कूल का होमवर्क कर पहले यहाँ बकवास करने से पहले।",
            "दादी अम्मा अब तो आराम करो, इंटरनेट पर क्यों दिमाग खराब कर रही हो।",
            "ये आजकल के नौसिखिए बच्चे इंटरनेट पर ज्ञान बाँट रहे हैं।",
            "बूढ़े हो गए हो लेकिन अक्ल नहीं आई अभी तक।",
            "जाओ दादाजी, भजन कीर्तन करो, सोशल मीडिया तुम्हारे बस का नहीं है।",
            "अरे छोटे बच्चे, बड़ों के मामले में टांग मत अड़ाओ।",
            "तुम्हारी उम्र अब कब्र में पैर लटकाने की है, यहाँ क्या कर रहे हो।",
            "सठियाए हुए बुड्ढे को घर वाले भी नहीं पूछते।",
            "दूध पीता बच्चा आ गया इंटरनेट पर चौधरी बनने।",
            "उम्र पचास की और अक्ल बचपन की भी नहीं है।",
            "ये नई उम्र के लड़के-लड़कियां बिल्कुल बेवकूफ हैं।"
        ],
        "Hinglish": [
            "Abey boomer uncle, tumhara time khatam ho gaya, chup baitho.",
            "Chhota bachha hai tu, school ja aur chup baith pehle.",
            "Budhaapa aa gaya hai par akal nahi aayi abhi tak saale.",
            "Grandma go to sleep, social media is not for your generation.",
            "Yeh bachhe internet pe hero ban rahe hain, do thappad padenge ro doge.",
            "Boomer mindset wale log har jagah gyaan pelte hain.",
            "Tu abhi kachha khiladi hai beta, bado ke saamne zubaan mat lada.",
            "Dada ji retirement enjoy karo, internet pe bakwaas mat karo.",
            "Chhote bachhe mobile pakad ke aukaat dikha rahe hain.",
            "Buddhe satiya gaya hai tu, dimaag kaam karna band ho gaya kya?",
            "School ki padhai kar le pehle beta, fir debate karna.",
            "Boomer uncle ko bolo whatsapp forward padhein bas."
        ]
    },
    "Gender-based": {
        "English": [
            "Women should not be allowed online, you are just an emotional bitch.",
            "Go back to the kitchen where you belong, that is your only use.",
            "Typical female with zero logic and infinite entitlement.",
            "You are just a cheap slut looking for validation online.",
            "Feminist trash like you are destroying traditional families.",
            "No man will ever respect or marry a whore like you.",
            "Cry more little girl, women cannot lead or code properly.",
            "Stupid woman should stay silent when men are speaking.",
            "Gold digging whore who only cares about men's bank accounts.",
            "Just another bimbo who thinks showing skin makes her relevant.",
            "Women have lower IQ than men, scientific fact.",
            "Shut up you toxic feminist bitch nobody cares about your feelings.",
            "You belong in the laundry room washing my clothes.",
            "Horrible manipulative female playing the victim card again.",
            "All women are disloyal gold diggers looking for free meals.",
            "You are an ugly slut that no decent guy would touch.",
            "Brainless female talking about things she has no clue about.",
            "She slept her way to the top, typical woman with zero skills.",
            "Sit down and be quiet, let the real men handle business.",
            "Dumb blonde bimbo with nothing inside her head."
        ],
        "Hindi": [
            "औरत हो, घर में बैठो, सोशल मीडिया पर बकवास मत करो।",
            "रंडी जैसी हरकतें करना बंद करो और अपनी सीमा में रहो।",
            "महिलाओं का काम सिर्फ रसोई संभालना है, दिमाग चलाना नहीं।",
            "फेमिनिस्ट बकवास करना बंद करो, तुम बस एक सस्ती औरत हो।",
            "लड़की हो तो अपनी मर्यादा में रहो, ज्यादा जुबान मत चलाओ।",
            "तेरे जैसी घटिया औरत कभी किसी का भला नहीं कर सकती।",
            "औरतों में अक्ल नाम की चीज नहीं होती, सिर्फ रोना आता है।",
            "चरित्रहीन औरत को समाज में बोलने का कोई अधिकार नहीं है।",
            "जाकर चौका-बर्तन संभालो, यहाँ पुरुषों की बराबरी मत करो।",
            "कपड़े छोटे पहनकर संस्कार भूल गई है ये बेशर्म लड़की।",
            "तू सिर्फ मर्दों के पैसे लूटने वाली औरत है।",
            "घटिया सोच वाली फेमिनिस्ट समाज के लिए कलंक हैं।"
        ],
        "Hinglish": [
            "Randi jaise behave mat kar, aurat hai toh chup chaap reh.",
            "Ladki hoke itna bolti hai, kitchen me jaake bartan dho.",
            "Typical feminist randi rona shuru ho gaya iska yahan.",
            "Slut banne ka shauq hai toh kahin aur ja, yahan mat dikha.",
            "Aurat ki aukaat sirf ghar sambhalne ki hoti hai.",
            "Attention seeker ladki, views ke liye kapde utaar rahi hai.",
            "Randi aurat, mard ke paison pe aish karna band kar.",
            "Female quota se aayi hai, kaam dhang se kuch nahi aata.",
            "Ladkiyon ko gaadi chalana aur dimag lagana kabhi nahi aayega.",
            "Victim card khelna band kar nautanki aurat.",
            "Gold digger ban ke ghoom rahi hai, sharam kar thodi.",
            "Chup chap reh ladki, jyada hoshiyari dikhayegi toh maar padegi."
        ]
    },
    "Religion-based": {
        "English": [
            "You are a terrorist because of your religion, get out.",
            "Your fake religion promotes violence and extremism everywhere.",
            "Dirty heathens worshiping false idols, you will all burn.",
            "Muslims are radical extremists who destroy every host country.",
            "Hindu fundamentalists are spreading hatred and fascism everywhere.",
            "Convert or leave the civilized world, you religious zealot.",
            "Your holy book is a manual for terrorism and murder.",
            "Religious cult fanatics have zero humanity and zero morality.",
            "Go back to your islamic caliphate, we don't want your faith here.",
            "Your religious community is a disease on modern democracy.",
            "Brainwashed religious idiots blindly following a desert cult.",
            "All terrorists belong to your disgusting faith.",
            "Cowardly religious bigots burning temples and churches.",
            "Your religious beliefs are barbaric and medieval.",
            "We will eradicate your religious cult from our nation.",
            "Radical jihadist sympathizer pretending to be peaceful.",
            "Fanatic zealots who value superstitions over human lives.",
            "Your people are religious parasites infesting our cities.",
            "Religious fascism is what your entire community stands for.",
            "Deport all religious extremists back to the stone age."
        ],
        "Hindi": [
            "तेरे धर्म के लोग आतंकी होते हैं, देश छोड़ दो।",
            "काफिरों को जीने का कोई हक नहीं है, इनका बहिष्कार करो।",
            "अपने पाखंडी धर्म का कचरा यहाँ मत फैलाओ जिहादियों।",
            "धर्म के नाम पर आतंक फैलाने वालों को गोली मार देनी चाहिए।",
            "कट्टरपंथी मानसिकता के लोग कभी सुधर नहीं सकते।",
            "तुम्हारे धर्म में सिर्फ नफरत सिखाई जाती है, ढोंगी कहीं के।",
            "जिहादी मानसिकता वाले इस देश के सबसे बड़े दुश्मन हैं।",
            "अपने मजहब का जहर घोलना बंद करो और सुधर जाओ।",
            "तुम्हारी आस्था सिर्फ दिखावा और पाखंड है।",
            "धर्मान्ध लोग देश की तरक्की में सबसे बड़ा रोड़ा हैं।",
            "धार्मिक उन्माद फैलाने वाले आतंकियों को सबक सिखाया जाएगा।",
            "नकली संतों और मौलवियों के गुलाम बनकर रह गए हो तुम लोग।"
        ],
        "Hinglish": [
            "Tere jaise dharam ke log desh ke dushman hain, nikal yahan se.",
            "Mullah terrorist nikal yahan se, Pakistan chala ja.",
            "Dharam ke naam pe dange failane wale jihadi kutte.",
            "Tumhare mandir aur masjid dono me sirf nafrat sikhate hain.",
            "Kafir bolke sabko target karte ho, tumhara religion toxic hai.",
            "Radical fundamentalists should be kicked out of society.",
            "Terrorist sleeper cell lagta hai tu dharam ke naam pe.",
            "Jihadi thinking band kar varna police utha ke le jayegi.",
            "Dharmik dange karwane wale dalle ho tum log.",
            "Mazhab ke naam pe brainwash ho chuke ho tum saale.",
            "Religious hate failana band karo toxic fundamentalists.",
            "Pakistani agent lag raha hai dharam ka card khelne wala."
        ]
    },
    "Ethnicity-based": {
        "English": [
            "Go back to where you came from, you dirty foreigner.",
            "Your race is genetically inferior and uncivilized.",
            "Dirty immigrants like you are ruining our entire country.",
            "Low-caste scum trying to act equal to noble people.",
            "Go back to your third-world shithole, you ethnic parasite.",
            "We don't need filthy illegal aliens taking our jobs and land.",
            "Look at this subhuman savage trying to speak our language.",
            "Your entire ethnic tribe is full of thieves, rapists, and beggars.",
            "Deport all these dirty foreigners immediately without mercy.",
            "You and your primitive people are a plague on our homeland.",
            "Inferior genetics showing through your backward behavior.",
            "Tribal jungle dweller trying to blend into civilized society.",
            "Racial slur targets you because your kind has no dignity.",
            "You belong in the ghetto, stop pretending to be one of us.",
            "Alien invaders destroying our culture and heritage.",
            "Filthy migrants bringing crime and diseases into our towns.",
            "Your race has contributed nothing positive to human history.",
            "Primitive savage people who belong in cages not colleges.",
            "Get out of our country before we run you out by force.",
            "Your ethnic heritage is pure shame and degradation."
        ],
        "Hindi": [
            "अपनी नीच जाति और कौम का कचरा यहाँ मत फैला।",
            "विदेशी घुसपैठियों को देश से लात मारकर बाहर निकालो।",
            "तुम्हारी जाति के लोग हमेशा नीचे ही रहेंगे, बराबरी मत करो।",
            "काले जंगली लोग हमारे समाज को गंदा कर रहे हैं।",
            "अपनी औकात मत भूल, तू एक नीच कुल का इंसान है।",
            "तुम्हारी कौम ही गद्दारों और चोरों की कौम है।",
            "घुसपैठिए रोहिंग्या और विदेशी हमारे देश को खा रहे हैं।",
            "जातिवादी मानसिकता से भरे नीच लोग कभी सम्मान के योग्य नहीं हैं।",
            "बाहरी लोग आकर हमारी संस्कृति को नष्ट कर रहे हैं।",
            "तेरी नस्ल ही धोखेबाजों की नस्ल है।",
            "जंगली कबीले के लोग शहरों में आकर गंदगी फैलाते हैं।",
            "अपनी जाति का घमंड मत दिखा, इतिहास गवाह है तेरी हैसियत का।"
        ],
        "Hinglish": [
            "Chapri log internet pe aa gaye, apni gandi aukat dikha rahe ho.",
            "Low caste wale barabari karenge hamari? Aukat me reh.",
            "Chinki Nepali jaisi shakal hai teri, go back to your border.",
            "Bihari migrant jaake majdoori kar yahan gyaan mat de.",
            "Third class race wale log internet pe aake chaudhre ban rahe.",
            "Ghatiya jaat ke log kabhi sudhar nahi sakte saale.",
            "Neech khandaan ke log aukaat bhool gaye hain aajkal.",
            "Foreign illegal migrant nikal hamare sheher se bahar.",
            "Chapri basti ke log internet connection leke hero ban rahe.",
            "Casteist slurs padenge tabhi tujhe akal aayegi neech aadmi.",
            "Aukaat majdoor ki hai aur baatein raja wali karta hai.",
            "Apni backward community me jaake gyaan pel yahan nahi."
        ]
    },
    "Appearance-based": {
        "English": [
            "Look at your face in the mirror, so ugly and pathetic.",
            "You look like a disgusting deformed pig, lose weight.",
            "Fat cow needs to stop eating and hit the gym immediately.",
            "Your teeth and nose are repulsive, who could ever love you?",
            "Absolute hideous creature, please wear a mask to save our eyes.",
            "You are so fat you probably need two seats on an airplane.",
            "Gross acne covered face, you look like a mutated monster.",
            "Skeleton anorexic freak, you look half dead and diseased.",
            "Your looks are completely repulsive and nauseating to look at.",
            "Plastic surgery couldn't even fix that horrific disastrous mug.",
            "Disgusting double chin and greasy hair, take a shower freak.",
            "You are visually offensive, nobody wants to see your ugly face.",
            "Bloated whale trying to wear fashionable clothes, hilarious.",
            "You look like you got hit in the face with a shovel.",
            "Repulsive dwarf goblin with zero aesthetic appeal.",
            "Stop posting selfies, you are giving everyone nightmares.",
            "Skinny twig with no muscles, looking like a sickly beggar.",
            "Ugly monster, your face belongs in a horror movie trailer.",
            "Gross crooked teeth and yellow smile, brush your teeth slob.",
            "Fat slob can barely walk without wheezing, pathetic pig.",
            "You are horribly overweight, stop gorging on junk food like a swine.",
            "Look at those hideous wrinkles and flabby skin, absolutely repulsive.",
            "You are the ugliest human being to ever step on this earth."
        ],
        "Hindi": [
            "तुम्हारा चेहरा इतना गंदा और बदसूरत है कि कोई देख नहीं सकता।",
            "मोटी भैंस थोड़ा कम खाया कर, जमीन भी धंस जाएगी तेरे वजन से।",
            "सड़ा हुआ चेहरा लेकर बाहर मत निकला कर, उल्टी आ जाती है।",
            "कितना घिनौना और भद्दा दिखता है तू, आईना तोड़ दे अपना।",
            "सूअर जैसी शक्ल है तेरी, तुझे देखकर इंसान डर जाए।",
            "इतनी काली और बदसूरत लड़की को कोई नहीं पूछेगा कभी।",
            "पिंपल्स से भरा सड़ा हुआ थोबड़ा लेकर फोटो डाल रहा है।",
            "हाथी जैसे शरीर को थोड़ा कम कर, शर्म आनी चाहिए तुझे।",
            "कंकाल जैसा सूखा हुआ शरीर है, कुछ खाया-पिया कर मरियल।",
            "तेरी भद्दी शक्ल देखकर दिन खराब हो जाता है सबका।",
            "इतना बदसूरत इंसान मैंने जिंदगी में नहीं देखा।",
            "मुँह पर कालिख पोत ले, तेरी शक्ल देखने लायक नहीं है।",
            "मोटा भैंसा जैसा शरीर बना रखा है, थोड़ा तो शर्म कर ले।"
        ],
        "Hinglish": [
            "Kitna mota aur badsurat hai tu, suar jaisi shakal hai.",
            "Moti bhains thoda exercise kar le, fati ja rahi hai.",
            "Moti bhaisn lag rahi hai ekdum, sharam kar le thodi.",
            "Badsurat chudail jaisa chehra hai tera, makeup se bhi nahi chupegi.",
            "Chehra dekha hai apna? Kutta bhi darr ke bhaag jaye tujhse.",
            "Itna repulsive lagta hai tu, mirror me dekh ke sharam nahi aati?",
            "Haathi jaisi body leke model banne chali hai, aukat dekh apni.",
            "Sukha papad jaisi body hai, hawa aayegi toh ud jayega.",
            "Ugly shakal ke sath reels mat banaya kar, ulti aati hai dekh ke.",
            "Double chin aur pet bahar nikla hua hai, sharam kar motey.",
            "Tere face pe itne daag hain, monster lagta hai pura.",
            "Fat pig stop eating burgers all day, disgusting lagta hai.",
            "Plastic surgery karwa le shayad thoda insaan jaisa dikhe.",
            "Mota saand jaisa ghoom raha hai, weight loss kar le thoda.",
            "Moti bhains jaisa sharir hai tera, chalna firna band kar diya kya?"
        ]
    },
    "Mockery/Defamation": {
        "English": [
            "What a clown show, look at this complete fool embarrassing himself.",
            "You are the biggest laughingstock on the entire internet.",
            "Everyone in the group is laughing at your pathetic public failure.",
            "Look at this clown dancing for five cents, absolute circus act.",
            "Nobody takes you seriously, you are literally a walking meme.",
            "Look at this certified loser pretending to be an expert in anything.",
            "Congratulations on embarrassing your entire family and bloodline publicly.",
            "This guy has negative IQ, what an absolute humiliation to watch.",
            "You are an absolute joke to everyone who knows your real story.",
            "A clown belongs in a circus, why are you on this serious platform?",
            "Pathetic fraud got exposed in front of the entire community.",
            "We made a compilation of your failures and it has gone viral.",
            "Everyone knows you cheated and lied your way through your degree.",
            "You are a public disgrace and an absolute laughingstock.",
            "Look at this clown crying on video for fake sympathy, haha.",
            "A cartoon character has more credibility and dignity than you.",
            "Stop embarrassing yourself in public, you have zero shame.",
            "Total clown behaviour, you are a complete joke to society.",
            "We all laugh behind your back at your ridiculous delusions.",
            "Your entire career is a fabricated sham that fell apart."
        ],
        "Hindi": [
            "पूरे कॉलेज का सबसे बड़ा जोकर यही है, सबको इसका मज़ाक उड़ाना चाहिए।",
            "सारे इंटरनेट पर तेरी थू-थू हो रही है, सर्कस के जोकर।",
            "तुम्हारा पूरा खानदान तुम्हारी इस बेवकूफी पर हँस रहा है।",
            "ये देखो नमूना, अपनी बेइज्जती खुद कराने आ गया यहाँ।",
            "हंसी का पात्र बन चुका है तू, अब मुँह छुपाने की जगह ढूंढ।",
            "तेरी औकात एक जोकर जितनी भी नहीं है, नाटक बंद कर।",
            "चार पैसे की औकात नहीं और राजा बनने का ढोंग कर रहा है।",
            "तेरी पोल खुल गई है सबके सामने, फर्जी इंसान कहीं के।",
            "लोग तुझ पर थूकते हैं और तू इसे अपनी शान समझता है।",
            "अपनी फजीहत कराने का इतना शौक है तो सर्कस में काम कर ले।",
            "सारे मोहल्ले में तेरी बदनामी का ढोल बज चुका है।",
            "सोशल मीडिया पर जोकरपंती करके क्या हासिल कर लिया तूने?"
        ],
        "Hinglish": [
            "Ye pura joker hai bhai, sab log milke iska meme banao.",
            "Circus ka joker lag raha hai tu, full standup comedy fail.",
            "Bhai kya clown hai tu, pure group me sab teri beizzati kar rahe.",
            "Meme material ban gaya hai tu, screenshot leke leak karo sab jagah.",
            "Bhai negative brain cells hain tere paas, hasi aa rahi hai tujhpe.",
            "Kitna bada namoona hai ye, khud ko hero samajh raha hai lol.",
            "Clown alert! Iska video viral karke roast karo sab log.",
            "Teri aukat sabko pata chal gayi hai, fraud pakda gaya tera.",
            "Bhai pura college tere upar has raha hai, sharam bachi hai?",
            "Beizzati karwane ka certified shauqeen hai ye banda.",
            "Joker ki tarah acting mat kar, sympathy nahi milegi tujhe.",
            "Sab log comment me iske clown emojis spam karo fast."
        ]
    },
    "Abusive/Insult": {
        "English": [
            "You are completely useless and nobody here wants you.",
            "You stupid piece of shit, get lost and never come back.",
            "You absolute moron, shut your filthy mouth immediately.",
            "Dumb bastard with the intelligence of a broken brick.",
            "You disgusting scum, everyone in this forum despises you.",
            "Worthless piece of human garbage, delete your account now.",
            "Shut the hell up you illiterate brainless idiot.",
            "Brainless idiot talking nonsense all day long without thinking.",
            "You are an obnoxious lowlife loser with no future or prospects.",
            "Filthy degenerate, stop wasting everyone's oxygen on earth.",
            "You are a pathetic excuse for a human being, get out.",
            "Dumbass idiot can't even understand simple English instructions.",
            "You are complete trash, nobody has ever loved or respected you.",
            "Go drown in a puddle you worthless incompetent failure.",
            "Disgusting parasite, you make me want to vomit.",
            "Shut your mouth you stupid moron, nobody asked for your opinion.",
            "Arrogant prick with nothing going for him in real life.",
            "Fucking idiot, your mother should have swallowed you.",
            "You are a useless degenerate burden on your poor parents.",
            "Ignorant fool spreading your disgusting stupidity everywhere.",
            "You are so dirty, filthy and vile, sickening person.",
            "Disgusting and dirty scumbag, stay away from normal people."
        ],
        "Hindi": [
            "तुम बहुत बेकार और मूर्ख इंसान हो।",
            "कमीने और नीच इंसान, अपना गंदा मुँह बंद रख।",
            "कुत्ते की औलाद, तुझे तमीज नहीं है बात करने की।",
            "नालायक और जाहिल गधे, यहाँ से दफा हो जा।",
            "घटिया और बकवास इंसान, तेरी कोई कद्र नहीं है।",
            "साले हरामखोर, अपनी बकवास कहीं और जाके कर।",
            "सूअर की औलाद, तेरी जुबान खींच लेंगे हम।",
            "बेवकूफ और गंवार, तुझे बात करने की समझ नहीं है।",
            "कचरे के ढेर जैसे इंसान, तू धरती पर बोझ है।",
            "अकल के अंधे, मूर्खता की सारी हदें पार कर दी तूने।",
            "नीच और पापी इंसान, तुझे तो नर्क में भी जगह नहीं मिलेगी।",
            "गटर के कीड़े, अपनी गंदी जुबान बंद रख।",
            "तू बहुत गंदी है और घटिया सोच रखती है बेशर्म।",
            "तू चूतिया है और हमेशा चूतिया ही रहेगा।"
        ],
        "Hinglish": [
            "Tu kitna bada kutta aur chutiya hai saale.",
            "Tu chutiya hai, bilkul dimaag se paidal aadmi.",
            "Tu chutiya hai aur rahega hamesha.",
            "Chutiya insaan hai tu ek number ka.",
            "Tu bahut gandi hai, sharam nahi aati tujhe?",
            "Tu bahut gandi aurat hai, cheap character tera.",
            "Tu gandi hai bilkul, dur reh sabse.",
            "Tu bahut ganda insaan hai, disgusting harkatein teri.",
            "Madarchod chup chaap baith varna muh tod denge tera.",
            "Behenchod aukaat me reh varna nanga karke marenge tujhe.",
            "Gadha hai tu ek number ka, dimaag bech ke kha gaya kya?",
            "Saale kameene, tere jaisa ghatiya insaan nahi dekha kahin.",
            "Chutiye jaise baatein band kar, akal naam ki cheez nahi hai.",
            "Harami kutte, nikal yahan se varna bohot pachtaayega.",
            "Teri aukaat do kaudi ki nahi hai aur gyaan baant raha hai.",
            "Bhak saale bsdk, chup chaap nikal le yahan se.",
            "Kutta kamina insaan hai tu, thukta hai pura mohalla tujhpe.",
            "Dumbass chutiya can't even write two proper lines.",
            "Saale ghatiya suar ki aulaad, dur reh mujhse.",
            "Chutiya saala bhonk raha hai kabse.",
            "Bohot gandi soch hai teri saale kameene."
        ]
    },
    "Threat/Intimidation": {
        "English": [
            "I will rape you.",
            "I will rape you and destroy your life.",
            "I will hunt you down and rape you.",
            "I will sexually assault and murder you.",
            "I am going to rape you if you ever post again.",
            "You deserve to be raped and killed in an alley.",
            "I will track where you live and rape you tonight.",
            "I will rape and torture you until you bleed.",
            "I will track your IP and destroy you and your entire family.",
            "I know where you live, you will not survive this week.",
            "Watch your back when you walk outside alone, I will end you.",
            "I am going to hunt you down and beat you senseless.",
            "I will slit your throat if you ever post in this channel again.",
            "Your house will be burned down to the ground with you inside.",
            "Sleep with one eye open, we are coming for you tonight.",
            "I will make sure you end up in a hospital ICU bed or morgue.",
            "You won't live to see tomorrow, consider this your death sentence.",
            "We have your home address and your little sister is not safe.",
            "I will break every bone in your body until you beg for mercy.",
            "A bullet to your head will solve this problem permanently.",
            "I am putting a bounty on your head, your days are numbered.",
            "We will find your workplace and drag you out into the street.",
            "Say your final prayers, you are a dead man walking.",
            "I will choke the life out of you with my bare hands.",
            "You will bleed to death on the pavement, mark my words.",
            "I will ruin your life and kill anyone who tries to protect you.",
            "Do not step foot outside your apartment or it will be your last.",
            "We are going to execute you like a dog for what you did.",
            "Go die, kill yourself right now.",
            "I will murder you in cold blood."
        ],
        "Hindi": [
            "घर से बाहर निकल, तुझे जान से मार दूंगा आज।",
            "तेरा बलात्कार कर दूंगा अगर दोबारा सामने आई तो।",
            "तुझे और तेरे पूरे खानदान को रेप करके खत्म कर देंगे।",
            "मर जा तू जाके, तेरी लाश भी नहीं मिलेगी किसी को।",
            "अगर दोबारा कुछ बोला तो तेरी गर्दन काट दूंगा मैं।",
            "तेरे घर में घुसकर तुझे और तेरे परिवार को खत्म कर देंगे।",
            "अपनी जान की खैर मना, तू बहुत जल्द मरने वाला है।",
            "तुझे अस्पताल पहुँचा दूंगा, याद रखेगा कि किससे पंगा लिया था।",
            "तेरी छाती पर गोली मारूँगा, हिम्मत है तो सामने आ।",
            "तेरी हड्डियाँ तोड़कर तुझे जिंदगी भर के लिए अपाहिज बना दूंगा।",
            "तेरी उल्टी गिनती शुरू हो चुकी है, यमराज के पास भेजने का वक्त आ गया।",
            "घर का पता नोट कर लिया है, रात को हमारी टोली आ रही है।",
            "तुझे जिंदा जमीन में गाड़ देंगे, कोई बचाने नहीं आएगा।",
            "तेरा खून बहाए बिना हम चैन से नहीं बैठेंगे।",
            "मैं तुझे जान से मार डालूंगा साले।",
            "जाकर मर जा कहीं, तेरी जिंदगी खत्म कर दूंगा।"
        ],
        "Hinglish": [
            "Moti bhaisn marr jaa.",
            "Moti bhains mar ja tu.",
            "Moti bhains mar ja jaake kahin pe.",
            "Moti bhaisn mar ja tu jaake sharam kar.",
            "Mar ja tu.",
            "Mar ja, duniya se chala ja.",
            "Tu mar ja jaake kahin.",
            "Marr jaa saale, zinda rehne ke laayak nahi hai tu.",
            "Main tujhe maar dunga.",
            "Main tujhe jaan se maar dunga agar samne aaya toh.",
            "Tujhe maar dunga main, zinda nahi bachega tu.",
            "Tera rape kar dunga agar bahar nikli toh.",
            "I will rape you saali, ghar me ghuske marunga.",
            "Tera gala daba ke maar dunga tujhe.",
            "Tera address mil gaya hai, marja tu nahi toh ghar aake maarenge.",
            "Raste me mil tu bas, zinda zameen me gaad dunga tujhe saale.",
            "Bahar nikal teri taange tod dunga aaj main jaan se marunga.",
            "Tujhe jaan se maar denge agar wapas yahan comment kiya toh.",
            "Teri family ka address hai mere paas, sabko khatam kar dunga.",
            "Marja tu jaake, nahi toh hum aake tera gala daba denge.",
            "Kal subah ka sooraj nahi dekhega tu, encounter karwa dunga tera.",
            "Ghar pe bande bhej diye hain, door khol aur maar kha.",
            "Goli maar dunga seene me seedha, panga mat le mujhse.",
            "Teri laash bhi nahi milegi tere gharwalon ko, samajh le.",
            "Hospital ke ICU me admit karwa ke chhodenge tujhe.",
            "Chhuri ghonp dunga pet me agar dobara zubaan ladayi toh.",
            "Maar daalunga tujhe, police bhi nahi bacha payegi."
        ]
    },
    "Personal Harassment": {
        "English": [
            "Stop posting here, we will harass you until you delete your account.",
            "I will create twenty fake accounts to stalk and spam you every hour.",
            "We have your private intimate photos and we will leak them to your school.",
            "I am calling your employer and boss right now to get you fired.",
            "I will flood your inbox and phone with endless spam calls and bots.",
            "You will never find peace online, we will tag your parents everywhere.",
            "We are doxxing your personal phone number on every public forum.",
            "I will follow every move you make on instagram and expose your life.",
            "We will make your life a living hell every single day of the year.",
            "Prepare to see all your personal secrets and passwords leaked online.",
            "I am reporting every single post you ever made until you get banned.",
            "I will message every friend on your follower list telling them lies about you.",
            "We will show up at your college campus and harass you in person.",
            "Your reputation will be utterly destroyed by tomorrow morning.",
            "We are organizing a mass reporting brigade to terminate your profile.",
            "I am monitoring your location and checking your stories 24/7.",
            "No matter how many accounts you make, I will always find you.",
            "I sent your photos to your relatives, have fun explaining that.",
            "We will systematically ruin your career and relationships.",
            "You cannot escape us, we are watching everything you do online."
        ],
        "Hindi": [
            "हम सब मिलकर तेरा जीना हराम कर देंगे, यहाँ से भाग जा।",
            "तेरी निजी तस्वीरें और चैट पूरे इंटरनेट पर वायरल कर देंगे हम।",
            "तुझे हर सोशल मीडिया पर दिन-रात परेशान करेंगे जब तक तू रोएगा नहीं।",
            "तेरा नंबर हर ग्रुप में बाँट दिया है, अब लगातार कॉल्स आएंगी तुझे।",
            "तेरे स्कूल और दफ्तर में तेरी शिकायत करेंगे और तुझे बर्बाद कर देंगे।",
            "हम तुझे कभी शांति से नहीं रहने देंगे, तेरा पीछा नहीं छोड़ेंगे।",
            "तेरी माँ-बाप को तेरी सारी करतूतें भेज दी हैं हमने।",
            "तेरा अकाउंट बैन करवा कर ही दम लेंगे, मास रिपोर्टिंग शुरू हो चुकी है।",
            "तू जहाँ भी जाएगा, हम वहाँ आकर तेरी बेइज्जती करेंगे।",
            "तेरी सारी पर्सनल जानकारियाँ इंटरनेट पर सार्वजनिक कर दी गई हैं।",
            "दिन-रात तुझे मैसेज करके पागल कर देंगे हम।",
            "तेरी जिंदगी को नर्क बनाने का पूरा इंतजाम कर लिया है हमने।"
        ],
        "Hinglish": [
            "Tu jahan bhi comment karega, hum wahan tujhe bully karenge.",
            "Tera phone number leak kar diya hai Telegram pe, ab maza aayega.",
            "Teri personal chats ka screenshot sabko bhej raha hoon main.",
            "Tera account ban karwake rahenge, mass report shuru kar di hai.",
            "Har post pe aake galiyaan denge, dekh tu kab tak tikta hai yahan.",
            "Doxx ho chuka hai tu, ab dekh tera kya haal hota hai real life me.",
            "Tere college ke principal ko mail kar diya hai tere khilaaf.",
            "Teri photos morph karke viral karne wale hain hum log.",
            "Tu block karega toh dus naye fake accounts se stalk karunga tujhe.",
            "Subah se shaam tak spam call karwayenge tere phone pe.",
            "Duniya ke kisi kone me chup ja, hum tujhe dhoond nikalenge.",
            "Teri life tabah karne me hume bohot maza aayega, watch out."
        ]
    },
    "Non-cyberbullying": {
        "English": [
            "Thank you so much for explaining the code, really helpful project!",
            "Good morning everyone, hope you all have a wonderful day ahead.",
            "Can someone recommend a good book on distributed systems architecture?",
            "Congratulations on your new job promotion, wishing you all the best!",
            "The weather today is cloudy and very pleasant for an evening walk.",
            "I really enjoyed reading your research paper on natural language processing.",
            "Could you please help me troubleshoot this Docker container configuration?",
            "Happy birthday to my best friend, have a fantastic and blessed year ahead!",
            "Let us meet tomorrow at 10 AM for the quarterly project standup call.",
            "Great performance by the entire engineering team during the demo today.",
            "What is the best way to learn machine learning algorithms and mathematics?",
            "Thank you for the thoughtful review and very constructive feedback.",
            "I love how beautifully you captured the sunset in that landscape photo.",
            "Can anyone share the link to the official documentation for FastAPI?",
            "We had a wonderful family dinner tonight, feeling so grateful.",
            "The conference keynote on artificial intelligence ethics was very inspiring.",
            "Please remember to submit your weekly progress reports before Friday afternoon.",
            "Hope you feel better soon, take plenty of rest and drink warm water.",
            "Excited to start learning web development and building new applications.",
            "That was an exceptional presentation, very clear diagrams and insights.",
            "Looking forward to collaborating on this open source repository together.",
            "Could you share your recipe for that delicious homemade pasta dish?",
            "Great initiative to plant more trees in our local community park.",
            "Wishing everyone a peaceful and productive week ahead.",
            "I will see you at the conference tomorrow morning.",
            "I will help you with the research project whenever you need.",
            "I will call you later in the evening after work.",
            "I will be attending the webinar on cybersecurity next Monday."
        ],
        "Hindi": [
            "आज का मौसम बहुत सुहावना है और शाम को हल्की बारिश हो रही है।",
            "नमस्ते भाई, मुझे आपकी सहायता की आवश्यकता थी इस विषय में।",
            "इस परीक्षा की तैयारी के लिए कौन सी पुस्तकें सबसे अच्छी मानी जाती हैं?",
            "आपके नए कार्यभार और पदोन्नति के लिए बहुत-बहुत बधाई और शुभकामनाएँ।",
            "यह शोध लेख बहुत ज्ञानवर्धक और उपयोगी साबित हुआ, बहुत धन्यवाद।",
            "कृपया क्या आप मुझे पायथन कोड के इस भाग को थोड़ा समझा सकते हैं?",
            "कल सुबह दस बजे हम सब पुस्तकालय में मिलकर अध्ययन करेंगे।",
            "दीपावली के इस पावन पर्व पर आप सभी और आपके परिवार को हार्दिक शुभकामनाएँ।",
            "स्वास्थ्य का विशेष ध्यान रखें और प्रतिदिन नियमित रूप से योग करें।",
            "भारतीय क्रिकेट टीम ने आज का मुकाबला बहुत शानदार तरीके से जीता।",
            "मित्रों के साथ समय बिताना मन को शांति और प्रसन्नता देता है।",
            "हम सब मिलकर इस सामाजिक कार्य को सफल बनाएंगे, आपका सहयोग सराहनीय है।",
            "पर्यावरण संरक्षण के लिए हम सबको अधिक से अधिक पौधे लगाने चाहिए।",
            "आपके द्वारा दी गई सलाह मेरे बहुत काम आई, हृदय से धन्यवाद।",
            "मैं कल तुमसे मिलकर इस विषय पर चर्चा करूंगा।",
            "कृपया मुझे इस समस्या का समाधान खोजने में मदद करें।"
        ],
        "Hinglish": [
            "Bhai project submit ho gaya, thanks for helping me out yaar!",
            "Chalo weekend pe movie dekhne chalte hain sab log sath me.",
            "Kal subah 9 baje meeting hai, please time pe aana sab log.",
            "Congratulations bhai for the new laptop, party kab de rahe ho?",
            "Kya koi bata sakta hai React me state management kaise karein properly?",
            "Aaj ka match bohot exciting tha, maza aa gaya pura dekh ke.",
            "Thank you dost, teri wajah se assignment time pe complete ho gaya.",
            "Good night dosto, kal subah jaldi uthna hai gym ke liye.",
            "Bhai ye error kaise solve karein, stack overflow pe solution mil gaya.",
            "Mausam bohot accha hai aaj, chai peene chalte hain shaam ko.",
            "Happy birthday mere bhai, bhagwan tujhe hamesha khush rakhe.",
            "Sir ka lecture bohot informative tha, kafi concepts clear ho gaye.",
            "Coffee peene chalein break ke time pe sab log?",
            "Bhai tune interview pass kar liya, bohot khushi hui sunke!",
            "Bhai kaisa hai tu, sab badhiya chal raha hai?",
            "Main kal subah tujhse milunga library me.",
            "Main help kar dunga teri code debug karne me chinta mat kar.",
            "Chai peene chalte hain shaam ko tapri pe sab dost.",
            "Movie dekhne chalte hain aaj raat ko mast maza aayega.",
            "Kal subah gym chalte hain bhai sath me."
        ]
    }
}

# Generate structured dataset with syntactic variations to achieve ~2,000+ robust samples
def build_dataset():
    all_rows = []
    
    # Prefix modifiers for natural linguistic variation
    prefixes = [
        "",
        "Honestly speaking, ",
        "Listen to me, ",
        "Everyone can clearly see that ",
        "I just wanted to say: ",
        "Seriously yaar, ",
        "Tell me one thing, "
    ]
    
    seen_texts = set()
    
    for cls_name, lang_dict in DATA_POOLS.items():
        cls_count = 0
        for lang, examples in lang_dict.items():
            for base_ex in examples:
                # Add base example
                clean_base = base_ex.strip()
                if clean_base not in seen_texts:
                    seen_texts.add(clean_base)
                    all_rows.append((clean_base, cls_name, lang))
                    cls_count += 1
                
                # Add natural prefix variations
                for pfx in prefixes[1:4]:
                    var_text = f"{pfx}{clean_base[0].lower() + clean_base[1:]}" if clean_base and clean_base[0].isupper() else f"{pfx}{clean_base}"
                    if var_text not in seen_texts:
                        seen_texts.add(var_text)
                        all_rows.append((var_text, cls_name, lang))
                        cls_count += 1
                        
        print(f"Class '{cls_name}': {cls_count} samples generated.")

    out_file = RAW_DIR / "cyberbullying_multilingual_raw.csv"
    with open(out_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["text", "raw_label", "language"])
        for row in all_rows:
            writer.writerow(row)

    print(f"\nSuccessfully generated {len(all_rows)} total multilingual samples in {out_file}")

    # Generate support wellbeing dataset
    support_file = RAW_DIR / "support_wellbeing_raw.csv"
    support_base = [
        ("I am terrified and having severe panic attacks from these constant threats.", "high_stress", "fear"),
        ("I cannot sleep at night, I feel completely helpless and cornered.", "high_stress", "anxiety"),
        ("They are threatening my family, I don't know who to call or where to hide.", "high_stress", "fear"),
        ("I feel totally overwhelmed, crying constantly and unable to focus.", "high_stress", "sadness"),
        ("Why do people hate me so much? I feel so broken and hopeless inside.", "moderate_stress", "sadness"),
        ("I don't know what to do, should I delete my Instagram and change my number?", "moderate_stress", "confusion"),
        ("These negative comments are really stressing me out today.", "moderate_stress", "anxiety"),
        ("Can someone explain how to report cyberbullying to the police?", "advisory", "neutral"),
        ("I want to know how to preserve chat logs and screenshots as evidence.", "advisory", "neutral"),
        ("What legal protections exist against online harassment and defamation?", "advisory", "neutral"),
        ("Thank you for being here and listening, I feel much calmer now.", "low_stress", "relief"),
        ("I talked to my counselor today and I am starting to feel better.", "low_stress", "relief"),
        ("Feeling safe and supported today with my close friends around me.", "low_stress", "joy"),
        ("Taking a break from social media has really cleared my mind.", "low_stress", "peace")
    ]
    
    supp_rows = []
    for mod in ["", "Honestly, ", "Please help, ", "I want to share: ", "Right now, "]:
        for txt, stress, emo in support_base:
            supp_rows.append((f"{mod}{txt}".strip(), stress, emo))

    with open(support_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["text", "stress_label", "emotion"])
        for row in supp_rows:
            writer.writerow(row)
            
    print(f"Generated {len(supp_rows)} support wellbeing samples in {support_file}")

if __name__ == "__main__":
    build_dataset()
