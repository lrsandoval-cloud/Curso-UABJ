from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from translate import Translator

analyzer = SentimentIntensityAnalyzer()

oraciones = [   'El uso excesivo de pantallas lleva a los niños a necesitarlas aún más',
                'Los adolescentes y su relación con la tecnología: la mayoría piensan que deben cambiar sus hábitos',
                'Los preocupantes hallazgos sobre Instagram y sus efectos en las adolescentes',
                'Ministerio TIC respalda regular el uso de redes sociales en menores de 14 años',
                'Los adolescentes utilizan chatbots como terapeutas y eso es alarmante',
                'La comida de este restaurante es riquísima, la atención es excelente y la vista es espectacular',
                'La comida de este restaurante es una porquería, atienden muy mal y está todo sucio',
                'La comida de este restaurante es riquísima, la atención es excelente, la vista es espectacular y todo lo que dije es mentira'
                ]


vader = []
traductor = Translator(to_lang="en")

for oracion in oraciones:
    oracion_eng = traductor.translate(oracion)
    scores = analyzer.polarity_scores(oracion_eng)
    '''
    print(oracion)
    print(oracion_eng)
    print(scores)
    print()
    '''
    vader.append(scores['compound'])


###########################################################################################################3


from transformers import pipeline
classifier = pipeline('sentiment-analysis', model="nlptown/bert-base-multilingual-uncased-sentiment")

for i, oracion in enumerate(oraciones):
    sentir = classifier(oracion)
    print(oracion)
    print('Vader: ', vader[i])
    print(sentir)
    print()


