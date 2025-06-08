import pandas as pd

class SimpleChatBot:
    def __init__(self, filepath):
        self.questions, self.answers = self.load_data(filepath)

    # 사전 데이터 셋을 파일에서 읽어서 로드
    def load_data(self, filepath):
        data = pd.read_csv(filepath) # CSV 파일 읽기
        questions = data['Q'].tolist() # 질문 리스트
        answers = data['A'].tolist() # 답변 리스트
        return questions, answers

    # 최고의 답변을 찾긱 위한 로직
    def find_best_answer(self, input_sentence):
        min_distance = float('inf') # 무한대 초기화
        best_index = -1 # 초기 인덱스 설정
        
        for i, question in enumerate(self.questions): # enumerate를 사용하여 인덱스와 질문을 동시에 가져옴
            if question is None: # 질문이 None인 경우 건너뛰기
                continue 
            dist = calc_distance(input_sentence, question) # 레벤슈타인 거리 계산
            if dist is None: # 거리 계산이 None인 경우 건너뛰기
                continue
            if dist < min_distance: # 최소 거리를 찾기 위한 조건
                min_distance = dist # 최소 거리 업데이트
                best_index = i # 인덱스 업데이트
        
        return self.answers[best_index] # 답변 반환
    
# 레벤슈타인으로 거리 구하기기
def calc_distance(a, b):
    if a == b: return 0 # 두 문자열이 같으면 거리 0
    a_len = len(a) # 문자열 a의 길이
    b_len = len(b) # 문자열 b의 길이
    if a == "": return b_len # 빈 문자열 a의 경우 b의 길이 반환
    if b == "": return a_len # 빈 문자열 b의 경우 a의 길이 반환
    
    matrix = [[] for i in range(a_len+1)]  #  레벤슈타인 거리 계산을 위한 행렬 초기화
    for i in range(a_len+1):  # 행렬의 각 행을 초기화
        matrix[i] = [0 for j in range(b_len+1)]  # 각 열을 초기화
    for i in range(a_len+1): # 행렬의 첫 번째 열 초기화
        matrix[i][0] = i # 문자열 a의 길이
    for j in range(b_len+1): # 행렬의 첫 번째 행 초기화
        matrix[0][j] = j # 문자열 b의 길이
    for i in range(1, a_len+1): # 행렬의 나머지 부분을 채우기
        ac = a[i-1] # 문자열 a의 현재 문자
        for j in range(1, b_len+1): # 문자열 b의 현재 문자
            bc = b[j-1] # 문자열 b의 현재 문자
            cost = 0 if (ac == bc) else 1 # 현재 문자가 같으면 비용 0, 다르면 비용 1
            matrix[i][j] = min([ # 현재 위치의 최소 거리 계산
                matrix[i-1][j] + 1, # 위쪽에서 오는 경우
                matrix[i][j-1] + 1, # 왼쪽에서 오는 경우
                matrix[i-1][j-1] + cost # 대각선에서 오는 경우
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
    
