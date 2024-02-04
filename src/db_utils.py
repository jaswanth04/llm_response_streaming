import pymongo
import datetime
import uuid

def remove_inst_tags(input_string):
    while '[INST]' in input_string:
        start_index = input_string.find('[INST]')
        end_index = input_string.rfind('[/INST]') + len('[/INST]')
        input_string = input_string[:start_index] + input_string[end_index:]
    return input_string

class MongoConnector:
    def __init__(self) -> None:
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["llm"]
        self.collection = db["history"]

        # x = mycol.insert_one(mydict)

    def insert_record(self, session_id: str, question: str, answer: str) -> None:
        record = {"session_id": session_id,
                  "timestamp": datetime.datetime.utcnow(),
                  "question": question,
                  "answer": answer}
        
        res = self.collection.insert_one(record)

        print(res)

    def retrieve_history(self, session_id):
        # Query MongoDB to retrieve questions and answers for a given session_id, sorted by timestamp
        cursor = self.collection.find({'session_id': session_id}).sort('timestamp', 1)  # 1 for ascending order, -1 for descending

        questions_and_answers = []  # List to store questions and answers

        for doc in cursor:
            question = doc['question']
            answer = doc['answer']
            questions_and_answers.append((question, answer))

        return questions_and_answers


def main():
    mongo_connector = MongoConnector()

    session_id = str(uuid.uuid4())
    question = "Who are you?"
    answer = "My name is Mistral"

    mongo_connector.insert_record(session_id, question, answer)

if __name__ == '__main__':
    main()