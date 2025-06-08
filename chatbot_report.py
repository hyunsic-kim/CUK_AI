import pandas as pd

class SimpleChatBot:
    def __init__(self, filepath):
        self.questions, self.answers = self.load_data(filepath)

    # 사전 데이터 셋을 파일에서 읽어서 로드
    def load_data(self, filepath):
        data = pd.read_csv(filepath)
        questions = data['Q'].tolist()  
        answers = data['A'].tolist()   
        return questions, answers

    # 최고의 답변을 찾긱 위한 로직
    def find_best_answer(self, input_sentence):
        min_distance = float('inf')
        best_index = -1
        
        for i, question in enumerate(self.questions):
            if question is None:
                continue
            dist = calc_distance(input_sentence, question)
            if dist is None:
                continue
            if dist < min_distance:
                min_distance = dist
                best_index = i
        
        return self.answers[best_index]
    
# 레벤슈타인으로 거리 구하기기
def calc_distance(a, b):
    if a == b: return 0
    a_len = len(a)
    b_len = len(b)
    if a == "": return b_len
    if b == "": return a_len
    
    matrix = [[] for i in range(a_len+1)] 
    for i in range(a_len+1): 
        matrix[i] = [0 for j in range(b_len+1)]  
    for i in range(a_len+1):
        matrix[i][0] = i
    for j in range(b_len+1):
        matrix[0][j] = j
    for i in range(1, a_len+1):
        ac = a[i-1]
        for j in range(1, b_len+1):
            bc = b[j-1]
            cost = 0 if (ac == bc) else 1
            matrix[i][j] = min([
                matrix[i-1][j] + 1,     
                matrix[i][j-1] + 1,        
                matrix[i-1][j-1] + cost 
            ])

# 파일 경로
filepath = 'ChatbotData.csv'

# 쳇봇 생성
chatbot = SimpleChatBot(filepath)

# 종료가 입력 될 때까지 반복복
while True:
    input_sentence = input('You: ')
    if input_sentence.lower() == '종료':
        break
    response = chatbot.find_best_answer(input_sentence)
    print('Chatbot:', response)
    
