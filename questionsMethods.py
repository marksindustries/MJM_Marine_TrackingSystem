class QuestionsMethods:
    def ProcessQuestionsMethod(qa, questions_list, data):
        answers = {}
        for i in range(len(questions_list)):
            result = qa.invoke({"query": questions_list[i]})
            answers[data[i]] = result['result']
        return answers
