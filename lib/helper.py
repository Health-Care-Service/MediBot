#!usr/bin/python
# Owner :Jaideep Kekre
# _author_ = Jaideep Kekre / Sameer Deshmukh
# _info_   = This file contains classes and functions for various helper routines.

class bcolors:
    """Pretty colours for the terminal"""

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class question_interface_helper():
    """
    This class loads questions from data/ into legit question_interface objects.
    """
  
    def __init__(self):
        pass

    """
    @private
    assign attributes
    """
    @classmethod
    def _assign_attributes(self, q_interface, value, tag):
        q_interface.tag             = value.get('tag') or tag
        q_interface.question        = value['question']
        q_interface.response        = value.get('response')
        q_interface.response_type   = value['response_type']
        q_interface.response_re     = value.get('response_re')
        q_interface.ranged          = value.get('ranged')
        q_interface.range           = value.get('range')
        q_interface.ret             = value.get('ret')
        q_interface.is_top_level    = value.get('is_top_level')
        q_interface.loop            = value.get('loop')
        q_interface.custom_keyboard = value.get('custom_keyboard')
        q_interface.serial          = value.get('serial')

        return q_interface

    # @private
    @classmethod
    def _build_linked_list(self, value, tag):
        from question_interface import question_interface
        q    = question_interface()
        temp = q

        while True:
            temp = self._assign_attributes(temp, value, tag)

            if value.has_key('linked_questions'):
                temp.linked_questions = question_interface()
                temp = temp.linked_questions
                value = value['linked_questions']
            else:
                break

        return q

    @classmethod
    def load_top_questions(self):
        from top_questions import data
        from question_interface import question_interface

        top_questions_list = []
        data = data()

        for tag, value in data.iteritems():
            top = question_interface()
            top_questions_list.append(self._assign_attributes(top,value, tag))

        return top_questions_list

    @classmethod
    def load_linked_questions(self,symptom_tag,linked_question_tag=None,serial=None):
        from question_interface import question_interface

        linked_questions_list = []
        data = __import__(symptom_tag).data()

        if serial == None and linked_question_tag == None:
            for tag, value in data.iteritems():
                linked_questions_list.append(self._build_linked_list(value, tag))

            linked_questions_list.sort(key=lambda x: x.serial)
        elif serial == None and linked_question_tag: # search and load linked question by tag
            for tag, value in data.iteritems():
                if tag == linked_question_tag:
                    linked_questions_list.append(self._build_linked_list(value, tag))

        elif linked_question_tag == None and serial: # search by serial
            for tag, value in data.iteritems():
                if value['serial'] == serial:
                    linked_questions_list.append(self._build_linked_list(value, tag))

        return linked_questions_list

def test():
    tq_list = question_interface_helper.load_top_questions()
    f = None

    for q in tq_list:
        if q.question == "Do you have a fever?":
            f = q

    if f.tag == 'fever' and f.response == ['Yes','No']:
        print "PASS"

    lq_list = question_interface_helper.load_linked_questions('fever')
    f = lq_list[0]

    if f.tag == 'fever_measure' and f.ranged == True and f.response_type == ['int', 'float']:
        print "PASS"

    lq_list = question_interface_helper.load_linked_questions('joint_pain', 'joint_pain_area')
    f = lq_list[0]

    if f.linked_questions.question == "Are any other joins hurting?" and f.tag == 'joint_pain_area' and f.linked_questions.tag == 'joint_pain_area_more_pain':
       print "PASS"

    lq_list = question_interface_helper.load_linked_questions('fever',None,1)

    if len(lq_list) == 1:
        print "PASS"
    f = lq_list[0]

    if f.tag == "fever_periodic" and f.question == "Are you having intermittent fever over time?" and f.response == ['Yes', 'No']:
        print "PASS"


if __name__ == '__main__':
    test()

