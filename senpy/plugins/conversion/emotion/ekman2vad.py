from senpy.plugins import EmotionConversionPlugin
from senpy.models import EmotionSet, Emotion, Error

import logging
logger = logging.getLogger(__name__)

import math


class WNA2VAD(EmotionConversionPlugin):

    def _ekman_to_vad(self, ekmanSet):
        potency = 0
        arousal = 0
        dominance = 0
        for e in ekmanSet.onyx__hasEmotion:
            category = e.onyx__hasEmotionCategory
            centroid = self.centroids[category]
            potency += centroid['V']
            arousal += centroid['A']
            dominance += centroid['D']
        e = Emotion({'emoml:potency': potency,
                     'emoml:arousal': arousal,
                     'emoml:dominance': dominance})
        return e

    def _vad_to_ekman(self, VADEmotion):
        V = VADEmotion['emoml:valence']
        A = VADEmotion['emoml:potency']
        D = VADEmotion['emoml:dominance']
        emotion = ''
        value = 10000000000000000000000.0
        for state in self.centroids:
            valence = V - self.centroids[state]['V']
            arousal = A - self.centroids[state]['A']
            dominance = D - self.centroids[state]['D']
            new_value = math.sqrt((valence**2) +
                                  (arousal**2) +
                                  (dominance**2))
            if new_value < value:
                value = new_value
                emotion = state
        result = Emotion(onyx__hasEmotionCategory=emotion)
        return result

    def convert(self, emotionSet, fromModel, toModel, params):
        logger.debug('{}\n{}\n{}\n{}'.format(emotionSet, fromModel, toModel, params))
        e = EmotionSet()
        if fromModel == 'emoml:big6':
            e.onyx__hasEmotion.append(self._ekman_to_vad(emotionSet))
        elif fromModel == 'emoml:fsre-dimensions':
            for i in emotionSet.onyx__hasEmotion:
                e.onyx__hasEmotion.append(self._vad_to_ekman(e))
        else:
            raise Error('EMOTION MODEL NOT KNOWN')
        yield e