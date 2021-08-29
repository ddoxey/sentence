import unittest
from sentence import Sentence

from pprint import pprint


class TestDictionaryParsers(unittest.TestCase):

    def test_format_acronyms(self):

        acronyms = [
            ' F. B. I. ',
            ' F.B.I. ',
            ' F.B.I.',
            ' _F._B._I._ ',
            ' _F.B.I._ ',
            ' _F.B.I._',
            ' _F.B.I._ Today',
            ' _F.B.I._ today',
        ]

        expectations = [
            ' FBI ',
            ' FBI ',
            ' FBI.',
            ' _FBI_ ',
            ' _FBI_ ',
            ' _FBI._',
            ' _FBI_ Today',
            ' _FBI_ today',
        ]

        got = []

        for acronym in acronyms:

            got.append(Sentence._format_acronyms_(acronym))

        self.assertEqual(got, expectations, 'acronyms')


    def test_samples(self):
        text = '''
            Hello World.
            Hello (Kind World).
            Hello Mr. World.
            Hello Dr. W.H.O., and thank you!
            Hello Dr. W. H. O., and thank you!
            Back in the U.S.S.R.!
            Back in the U.S.S.R!
            I'd like to mention two things: 3. noodles, 4. eggs.
            I need to drop a number 2.
            I need to do a number 1.
            Furthermore, I am legend.
            For an arbitrary collection of English word tokens
            the Sentence parse function will return a list of strings.
            Each string is a complete sentence.
        '''
        expect = [
            'Hello World.',
            'Hello (Kind World).',
            'Hello Mr. World.',
            'Hello Dr. WHO, and thank you!',
            'Hello Dr. WHO, and thank you!',
            'Back in the USSR!',
            'Back in the USSR!',
            "I'd like to mention two things: 3. noodles, 4. eggs.",
            'I need to drop a number 2.',
            'I need to do a number 1.',
            'Furthermore, I am legend.',
            'For an arbitrary collection of English word tokens '
            'the Sentence parse function will return a list of strings.',
            'Each string is a complete sentence.'
        ]

        got = list(Sentence.parse(text))

        self.assertEqual(got, expect, 'samples')


    def test_fbi(self):
        text = '''
            The F. B.
            I. headquarters is the J. Edgar Hoover Building, located in Washington, D.C.
            The mission of the FBI follows.
            The current FBI Director is Christopher A.
            Wray appointed by President Donald Trump.
            Other things are also located in _Washington,_D.C._
        '''
        expect = [
            'The FBI headquarters is the J. Edgar Hoover Building, located in Washington, DC '
            'The mission of the FBI follows.',
            'The current FBI Director is Christopher A. Wray appointed by President Donald Trump.',
            'Other things are also located in _Washington,_DC._'
        ]

        got = list(Sentence.parse(text))

        self.assertEqual(got, expect, 'FBI')


    def test_caninae(self):
        text = '''
Their fossils were first found in North America and dated to the Oligocene era, then spreading to Asia at the end of the Miocene era, some 7 million to 8 million years ago.
Hesperocyoninae Borophaginae Caninae "Derived characteristics that distinguish the Caninae from other canids include small, simple, well-spaced premolars, a humerus without an entepicondylar foramen, and a metatarsal 1 which is reduced to a proximal rudiment."
The genus Leptocyon (Greek: leptos slender + cyon dog) includes 11 species and was the first primitive canine.

They were small and weighed around 2 kg.
        '''
        expect = [
            'Their fossils were first found in North America and dated to the Oligocene era, then spreading to Asia at the end of the Miocene era, some 7 million to 8 million years ago.',
            'Hesperocyoninae Borophaginae Caninae "Derived characteristics that distinguish the Caninae from other canids include small, simple, well-spaced premolars, a humerus without an entepicondylar foramen, and a metatarsal 1 which is reduced to a proximal rudiment."',
            'The genus Leptocyon (Greek: leptos slender + cyon dog) includes 11 species and was the first primitive canine.',
            'They were small and weighed around 2 kg.',
        ]

        got = list(Sentence.parse(text))

        self.assertEqual(got, expect, 'Caninae')


    def test_amazon(self):
        text = '''
This pump is by far the very best one that I have ever used. It totally rocks in my 55-gallon aquarium. The only thing that you need to be concerned with is that it simply pumps a lot more air than you are used too, so you'd better have plenty of airstones on hand when it comes time to change them out because you don't want to back this thing up and damage anything.
        '''
        expect = [
            'This pump is by far the very best one that I have ever used.',
            'It totally rocks in my 55-gallon aquarium.',
            'The only thing that you need to be concerned with is that it simply pumps a '
            "lot more air than you are used too, so you'd better have plenty of airstones "
            "on hand when it comes time to change them out because you don't want to back "
            'this thing up and damage anything.'
        ]

        got = list(Sentence.parse(text))

        self.assertEqual(got, expect, 'Amazon')


    def test_park_burgess(self):
        text = '''
Men were long in learning that Man's power of modifying
phenomena can result only from his knowledge of their natural
laws; and in the infancy of each science, they believed
themselves able to exert an unbounded influence over the
phenomena of that science.... Social phenomena are, of course,
from their extreme complexity, the last to be freed from this
pretension: but it is therefore only the more necessary to
remember that the pretension existed with regard to all the
rest, in their earliest stage, and to anticipate therefore that
social science will, in its turn, be emancipated from the
delusion.... It [the existing social science] represents the
social action of Man to be indefinite and arbitrary, as was
once thought in regard to biological, chemical, physical, and
even astronomical phenomena, in the earlier stages of their
respective sciences.... The human race finds itself delivered
over, without logical protection, to the ill-regulated
experimentation of the various political schools, each one of
which strives to set up, for all future time, its own immutable
type of government. We have seen what are the chaotic results
of such a strife; and we shall find that there is no chance of
order and agreement but in subjecting social phenomena, like
all others, to invariable natural laws, which shall, as a
whole, prescribe for each period, with entire certainty, the
limits and character of political action: in other words,
introducing into the study of social phenomena the same
positive spirit which has regenerated every other branch of
human speculation.[4]
        '''
        expect = [
            "Men were long in learning that Man's power of modifying phenomena can result "
            'only from his knowledge of their natural laws; and in the infancy of each '
            'science, they believed themselves able to exert an unbounded influence over '
            'the phenomena of that science...',
            'Social phenomena are, of course, from their extreme complexity, the last to '
            'be freed from this pretension: but it is therefore only the more necessary to '
            'remember that the pretension existed with regard to all the rest, in their '
            'earliest stage, and to anticipate therefore that social science will, in its '
            'turn, be emancipated from the delusion...',
            'It [the existing social science] represents the social action of Man to be '
            'indefinite and arbitrary, as was once thought in regard to biological, chemical, '
            'physical, and even astronomical phenomena, in the earlier stages of their '
            'respective sciences...',
            'The human race finds itself delivered over, without logical protection, to the '
            'ill-regulated experimentation of the various political schools, each one '
            'of which strives to set up, for all future time, its own immutable type of '
            'government.',
            'We have seen what are the chaotic results of such a strife; and we shall '
            'find that there is no chance of order and agreement but in subjecting social '
            'phenomena, like all others, to invariable natural laws, which shall, as a '
            'whole, prescribe for each period, with entire certainty, the limits and '
            'character of political action: in other words, introducing into the study of '
            'social phenomena the same positive spirit which has regenerated every other '
            'branch of human speculation.',
        ]

        got = list(Sentence.parse(text))

        self.assertEqual(got, expect, 'Park-Burgess')


    def test_lippmann(self):
        text = '''
But the most interesting kind of portraiture is that which arises
spontaneously in people's minds. When Victoria came to the throne,
says Mr. Strachey, [Footnote: Lytton Strachey, _Queen Victoria_,
p. 72.] "among the outside public there was a great wave of
enthusiasm. Sentiment and romance were coming into fashion; and the
spectacle of the little girl-queen, innocent, modest, with fair hair
and pink cheeks, driving through her capital, filled the hearts of the
beholders with raptures of affectionate loyalty. What, above all,
struck everybody with overwhelming force was the contrast between
Queen Victoria and her uncles. The nasty old men, debauched and
selfish, pigheaded and ridiculous, with their perpetual burden of
debts, confusions, and disreputabilities--they had vanished like the
snows of winter and here at last, crowned and radiant, was the
spring."
        '''
        expect = [
            'But the most interesting kind of portraiture is that which arises '
            "spontaneously in people's minds.",
            'When Victoria came to the throne, says Mr. Strachey, [Footnote: Lytton '
            'Strachey, _Queen Victoria_, p. 72.] "among the outside public there was a '
            'great wave of enthusiasm.',
            'Sentiment and romance were coming into fashion; and the spectacle of the '
            'little girl-queen, innocent, modest, with fair hair and pink cheeks, driving '
            'through her capital, filled the hearts of the beholders with raptures of '
            'affectionate loyalty.',
            'What, above all, struck everybody with overwhelming force was the contrast '
            'between Queen Victoria and her uncles.',
            'The nasty old men, debauched and selfish, pigheaded and ridiculous, with '
            'their perpetual burden of debts, confusions, and disreputabilities--they had '
            'vanished like the snows of winter and here at last, crowned and radiant, was '
            'the spring."'
        ]

        got = list(Sentence.parse(text))

        self.assertEqual(got, expect, 'Lippmann')


    def test_mccain(self):
        text = '''
26. Ration parties and parties carrying material for repairs,
etc., need not wear their equipment or carry rifles, but should be
accompanied by a fully armed N. C. O. as an escort.

27. Not more than twenty men are to be away from the company at the
same time. 1 N. C. O. and 4 men per platoon.

28. Every soldier must remember it is of the utmost importance to keep
his rifle clean and in working order whilst in the trenches. His very
life may depend upon this, as he is liable to be rushed at any moment,
either by day or by night. The dirty rifle means probably a jammed one
after the first round.

29. The first duty of a soldier, therefore, is to clean his rifle every
morning as soon as there is sufficient light to enable him to do so; an
hour will be appointed by O. C. company for this purpose. The platoon
sergeant will be responsible that section commanders superintend this
work, and inspect the rifles of their section. Any man who is found
with a dirty rifle will be made a prisoner.
        '''
        expect = [
            '26.',
            'Ration parties and parties carrying material for repairs, etc., need not '
            'wear their equipment or carry rifles, but should be accompanied by a fully '
            'armed NCO as an escort.',
            '27.',
            'Not more than twenty men are to be away from the company at the same time.',
            '1 NCO and 4 men per platoon.',
            '28.',
            'Every soldier must remember it is of the utmost importance to keep his rifle '
            'clean and in working order whilst in the trenches.',
            'His very life may depend upon this, as he is liable to be rushed at any '
            'moment, either by day or by night.',
            'The dirty rifle means probably a jammed one after the first round.',
            '29.',
            'The first duty of a soldier, therefore, is to clean his rifle every morning '
            'as soon as there is sufficient light to enable him to do so; an hour will be '
            'appointed by OC company for this purpose.',
            'The platoon sergeant will be responsible that section commanders superintend '
            'this work, and inspect the rifles of their section.',
            'Any man who is found with a dirty rifle will be made a prisoner.',
        ]

        got = list(Sentence.parse(text))

        self.assertEqual(got, expect, 'McCain')


if __name__ == '__main__':
    unittest.main()
