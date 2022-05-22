import sys
from Answer_question import *



def main():
    if len(sys.argv) == 2:
        if sys.argv[1] != "create":
            print("Wrong input!")
            return
        #create_ontology()
        # TODO: fix in the end
        dummy_create_ontology()
        return

    if len(sys.argv) == 3:
        if sys.argv[1] != "question":
            print("Wrong input!")
            return
        answer_question(sys.argv[2])
        return

    print("Wrong input!")


if __name__ == '__main__':
    main()

