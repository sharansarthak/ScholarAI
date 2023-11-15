import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("hhh2023-a2da1-firebase-adminsdk-h2zwt-5ae5f17a8b.json")
firebase_admin.initialize_app(cred)

db=firestore.client()

# #db.collection('users').add({'name': 'Zeeshan'})
# db.collection('users').document('zeeshan').collection('chat').add({'age': 22})
# db.collection('users').document('zeeshan').set({'age': 22})

# result = db.collection('users').document('zeeshan').get()

# #print(result.to_dict())

# docs = db.collection('users').document('zeeshan').collection('chat').get()
# for doc in docs:
#     print(doc.to_dict())



def write_chat(username, request):    
    for message in request:
        db.collection('users').document(username).collection('chat').add({'message':message})

def read_chat(username):
    docs = db.collection('users').document(username).collection('chat').get()
    result = []
    for doc in docs:
        result.append(doc.to_dict()['message'])
    return result


def add_scholarship(username, scholarships):
    for scholarship in scholarships:
        db.collection('users').document(username).collection('scholarship').document(str(scholarship['Title'])).set(scholarship)

def get_all_scholarship_brief(username):
    docs = db.collection('users').document(username).collection('scholarship').get()
    result = []
    for doc in docs:
        scholarship_data = doc.to_dict()
        # Remove "questions" and "answers" fields if they exist
        scholarship_data.pop('Questions', None)
        scholarship_data.pop('Answers', None)
        result.append(scholarship_data)
    return result

def get_all_scholarship(username):
    docs = db.collection('users').document(username).collection('scholarship').get()
    result = []
    for doc in docs:
        result.append(doc.to_dict())
    return result

# write_chat('zeeshan', [{"role": "system", "content": "You are a helpful assistant."},
#     {"role": "user", "content": "Who won the world series in 2020?"},
#     {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
#     {"role": "user", "content": "Where was it played?"}])
    
#print(read_chat('zeeshan'))


scholarships = [
    {
        "Scholarship Amount": "$5,000",
        "Deadline": "March 31, 2023",
        "Number of Recipients": 10,
        "Estimated Completion Time": "30 minutes",
        "Title": "STEM Innovation Grant",
        "Requirements": ["STEM", "Innovation", "Academic Excellence"],
        "Questions": [
            "What is your experience in STEM?",
            "How have you demonstrated innovation?",
            "Describe your academic achievements."
        ],
        "Answers": [
            "I participated in a STEM research project last year.",
            "I developed a new technology for my school project.",
            "I have consistently maintained a high GPA."
        ]
    },
    {
        "Scholarship Amount": "$7,500",
        "Deadline": "April 15, 2023",
        "Number of Recipients": 5,
        "Estimated Completion Time": "45 minutes",
        "Title": "Community Leadership Scholarship",
        "Requirements": ["Leadership", "Community Service", "High GPA"],
        "Questions": [
            "Describe your leadership experience.",
            "How have you contributed to your community?",
            "What is your GPA and why is it important to you?"
        ],
        "Answers": [
            "I led a community service project in my neighborhood.",
            "I volunteered at a local food bank.",
            "Maintaining a high GPA is important because..."
        ]
    },
    {
        "Scholarship Amount": "$3,000",
        "Deadline": "May 1, 2023",
        "Number of Recipients": 15,
        "Estimated Completion Time": "25 minutes",
        "Title": "Diversity and Inclusion Award",
        "Requirements": ["Diversity", "Inclusion", "Essay"],
        "Questions": [
            "How have you promoted diversity and inclusion?",
            "Why do you believe diversity is important?",
            "Write an essay on your experiences related to diversity and inclusion."
        ],
        "Answers": [
            "I organized a diversity awareness event at my school.",
            "Diversity is important because it enriches perspectives.",
            "In my essay, I will share personal experiences that highlight the importance of diversity."
        ]
    },
    {
        "Scholarship Amount": "$6,000",
        "Deadline": "April 10, 2023",
        "Number of Recipients": 8,
        "Estimated Completion Time": "40 minutes",
        "Title": "Future Entrepreneur Scholarship",
        "Requirements": ["Entrepreneurship", "Business Plan", "Innovation"],
        "Questions": [
            "What is your experience in entrepreneurship?",
            "Describe your business plan.",
            "How have you demonstrated innovation in your entrepreneurial pursuits?"
        ],
        "Answers": [
            "I started my own small business in high school.",
            "My business plan focuses on...",
            "I introduced innovative strategies to increase business efficiency."
        ]
    },
    {
        "Scholarship Amount": "$8,000",
        "Deadline": "May 15, 2023",
        "Number of Recipients": 3,
        "Estimated Completion Time": "50 minutes",
        "Title": "Environmental Stewardship Grant",
        "Requirements": ["Environmental Conservation", "Sustainability", "Essay"],
        "Questions": [
            "How have you contributed to environmental conservation?",
            "Why is sustainability important to you?",
            "Write an essay on your commitment to environmental stewardship."
        ],
        "Answers": [
            "I organized a community clean-up event.",
            "Sustainability is important because...",
            "In my essay, I will elaborate on my dedication to environmental stewardship."
        ]
    },
    {
        "Scholarship Amount": "$4,500",
        "Deadline": "March 20, 2023",
        "Number of Recipients": 12,
        "Estimated Completion Time": "35 minutes",
        "Title": "Merit Excellence Scholarship",
        "Requirements": ["Academic Excellence", "High GPA", "Essay"],
        "Questions": [
            "What achievements demonstrate your academic excellence?",
            "Why is maintaining a high GPA important to you?",
            "Write an essay on your academic journey and goals."
        ],
        "Answers": [
            "I achieved the highest grades in my science courses.",
            "Maintaining a high GPA is important because...",
            "In my essay, I will reflect on my academic journey and outline my future goals."
        ]
    }
]

#add_scholarship('zeeshan',scholarships)

print(get_all_scholarship_brief('zeeshan'))