import firebase_admin
from firebase_admin import auth, credentials, firestore, initialize_app

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


def populate_user_profile(username, user_response):
    db.collection('users').document(username).set(user_response)
    

def add_scholarship(username, scholarships):
    for scholarship in scholarships:
        db.collection('users').document(username).collection('scholarship').document(str(scholarship['Title'])).set(scholarship)

def add_resource(username, resources):
    for category in resources:
        category_name = category['category']
        activities = category['activities']
        
        # Create a document with the category name as the document ID
        category_doc_ref = db.collection('users').document(username).collection('resource').document(category_name)
        
        # Set the document with all activities of the category
        category_doc_ref.set({'activities': activities})



def get_all_scholarship_brief(username):
    docs = db.collection('users').document(username).collection('scholarship').get()
    result = []
    for doc in docs:
        scholarship_data = doc.to_dict()
        # Remove "questions" and "answers" fields if they exist
        scholarship_data.pop('Questions', None)
        scholarship_data.pop('Answers', None)
        scholarship_data.pop('Description', None)
        result.append(scholarship_data)
    return result

def get_all_resources(username):
    docs = db.collection('users').document(username).collection('resource').get()
    result = []
    for doc in docs:
        resource_data = doc.to_dict()
        resource_data['category'] = doc.id  # Add the 'category' field
        result.append(resource_data)
    return result


def login(email, password):
    try:
        # Sign in the user with the provided email and password
        user = auth.get_user_by_email(email)
        user_token = auth.create_custom_token(user.uid)

        return {'success': True, 'uid': user.uid, 'token': user_token}

    except Exception as e:
        return {'error': e}, 401

def signup(email, password):
    try:

        # Create a new user account with the provided email and password
        user = auth.create_user(
            email=email,
            password=password
        )

        return {'success': True, 'uid': user.uid}

    except Exception as e:
        return {'error': str(e)}

def update_scholarship_answer(username, scholarship_title, index, updated_answer):
    try:
        # Get data from the request

        # Validate required fields
        if not username or not scholarship_title or index is None or updated_answer is None:
            return {'error': 'Invalid request. Missing required fields.'}

        # Retrieve the scholarship document
        scholarship_ref = db.collection('users').document(username).collection('scholarship').document(scholarship_title)
        scholarship_doc = scholarship_ref.get()

        # Check if the scholarship exists
        if not scholarship_doc.exists:
            return {'error': 'Scholarship not found.'}

        print("Hi")
        # Update the 'Answers' field at the specified index
        current_answers = scholarship_doc.get('Answers')

        print(current_answers)
        if 0 <= index < len(current_answers):
            current_answers[index] = updated_answer
            scholarship_ref.update({'Answers': current_answers})
            return {'success': True}

        return {'error': 'Invalid index.'}

    except Exception as e:
        return {'error': str(e)}

# def application_submitted(username, title):

#     data = request.json
#     username = data.get('username')
#     title = data.get('title')

#     db.collection('users').document(username).collection('scholarship').document(title).update({'Submitted': True})


def gpt_improve_essay():

    request_message_formatted = {'content': request_message, 'role': 'user'}
    messages_to_send = read_chat(username) + [request_message_formatted]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages_to_send
    )

    response_message_formatted = {'content': response.choices[0].message.content, 'role': 'assistant'}
    messages = [request_message_formatted]+[response_message_formatted]

    write_chat(username, messages)
    

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
        "Description": "This scholarship is for students with a passion for STEM, a history of innovation, and demonstrated academic excellence.",
        "Questions": [
            "What is your experience in STEM?",
            "How have you demonstrated innovation?",
            "Describe your academic achievements."
        ],
        "Answers": [
            "I participated in a STEM research project last year.",
            "I developed a new technology for my school project.",
            "I have consistently maintained a high GPA."
        ],
        "Submitted": False  # New field
    },
    {
        "Scholarship Amount": "$7,500",
        "Deadline": "April 15, 2023",
        "Number of Recipients": 5,
        "Estimated Completion Time": "45 minutes",
        "Title": "Community Leadership Scholarship",
        "Requirements": ["Leadership", "Community Service", "High GPA"],
        "Description": "This scholarship recognizes students who have shown exceptional leadership skills, contributed to their community, and maintained a high GPA.",
        "Questions": [
            "Describe your leadership experience.",
            "How have you contributed to your community?",
            "What is your GPA and why is it important to you?"
        ],
        "Answers": [
            "I led a community service project in my neighborhood.",
            "I volunteered at a local food bank.",
            "Maintaining a high GPA is important because..."
        ],
        "Submitted": False  # New field
    },
    {
        "Scholarship Amount": "$3,000",
        "Deadline": "May 1, 2023",
        "Number of Recipients": 15,
        "Estimated Completion Time": "25 minutes",
        "Title": "Diversity and Inclusion Award",
        "Requirements": ["Diversity", "Inclusion", "Essay"],
        "Description": "This award is for students who actively promote diversity and inclusion. Applicants must submit an essay detailing their experiences related to diversity.",
        "Questions": [
            "How have you promoted diversity and inclusion?",
            "Why do you believe diversity is important?",
            "Write an essay on your experiences related to diversity and inclusion."
        ],
        "Answers": [
            "I organized a diversity awareness event at my school.",
            "Diversity is important because it enriches perspectives.",
            "In my essay, I will share personal experiences that highlight the importance of diversity."
        ],
        "Submitted": False  # New field
    },
    {
        "Scholarship Amount": "$6,000",
        "Deadline": "April 10, 2023",
        "Number of Recipients": 8,
        "Estimated Completion Time": "40 minutes",
        "Title": "Future Entrepreneur Scholarship",
        "Requirements": ["Entrepreneurship", "Business Plan", "Innovation"],
        "Description": "This scholarship is for aspiring entrepreneurs with a strong background in entrepreneurship, a well-defined business plan, and a track record of innovation.",
        "Questions": [
            "What is your experience in entrepreneurship?",
            "Describe your business plan.",
            "How have you demonstrated innovation in your entrepreneurial pursuits?"
        ],
        "Answers": [
            "I started my own small business in high school.",
            "My business plan focuses on...",
            "I introduced innovative strategies to increase business efficiency."
        ],
        "Submitted": False  # New field
    },
    {
        "Scholarship Amount": "$8,000",
        "Deadline": "May 15, 2023",
        "Number of Recipients": 3,
        "Estimated Completion Time": "50 minutes",
        "Title": "Environmental Stewardship Grant",
        "Requirements": ["Environmental Conservation", "Sustainability", "Essay"],
        "Description": "This grant is for students dedicated to environmental conservation and sustainability. Applicants must submit an essay detailing their commitment to environmental stewardship.",
        "Questions": [
            "How have you contributed to environmental conservation?",
            "Why is sustainability important to you?",
            "Write an essay on your commitment to environmental stewardship."
        ],
        "Answers": [
            "I organized a community clean-up event.",
            "Sustainability is important because...",
            "In my essay, I will elaborate on my dedication to environmental stewardship."
        ],
        "Submitted": False  # New field
    },
    {
        "Scholarship Amount": "$4,500",
        "Deadline": "March 20, 2023",
        "Number of Recipients": 12,
        "Estimated Completion Time": "35 minutes",
        "Title": "Merit Excellence Scholarship",
        "Requirements": ["Academic Excellence", "High GPA", "Essay"],
        "Description": "This scholarship recognizes students with a history of academic excellence, a high GPA, and the ability to articulate their academic journey and goals through an essay.",
        "Questions": [
            "What achievements demonstrate your academic excellence?",
            "Why is maintaining a high GPA important to you?",
            "Write an essay on your academic journey and goals."
        ],
        "Answers": [
            "I achieved the highest grades in my science courses.",
            "Maintaining a high GPA is important because...",
            "In my essay, I will reflect on my academic journey and outline my future goals."
        ],
        "Submitted": False  # New field
    }
]

resources = [
    {
        "category": "hackathons",
        "activities": [
            {
                "activity": "Hackathon 1",
                "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer nec odio. Praesent libero. Sed cursus ante dapibus diam.",
                "link": "https://hackathon1.com",
                "image": "https://www.google.com/imgres?imgurl=https%3A%2F%2Fpbs.twimg.com%2Fprofile_images%2F625987202909085696%2FKKYbLP8y_400x400.jpg&tbnid=ky1Jb3jyAGSj1M&vet=12ahUKEwjg6OnV0ceCAxWdLDQIHc-tBOwQMygAegQIARBK..i&imgrefurl=https%3A%2F%2Ftwitter.com%2Fdevpost&docid=JrkSXIYc2ahqUM&w=400&h=400&q=devpost%20logo&ved=2ahUKEwjg6OnV0ceCAxWdLDQIHc-tBOwQMygAegQIARBK"
            },
            {
                "activity": "Hackathon 2",
                "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer nec odio. Praesent libero. Sed cursus ante dapibus diam.",
                "link": "https://hackathon2.com",
                "image": "https://www.google.com/imgres?imgurl=https%3A%2F%2Fpbs.twimg.com%2Fprofile_images%2F625987202909085696%2FKKYbLP8y_400x400.jpg&tbnid=ky1Jb3jyAGSj1M&vet=12ahUKEwjg6OnV0ceCAxWdLDQIHc-tBOwQMygAegQIARBK..i&imgrefurl=https%3A%2F%2Ftwitter.com%2Fdevpost&docid=JrkSXIYc2ahqUM&w=400&h=400&q=devpost%20logo&ved=2ahUKEwjg6OnV0ceCAxWdLDQIHc-tBOwQMygAegQIARBK"
            },
            {
                "activity": "Hackathon 3",
                "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer nec odio. Praesent libero. Sed cursus ante dapibus diam.",
                "link": "https://hackathon3.com",
                "image": "https://www.google.com/imgres?imgurl=https%3A%2F%2Fpbs.twimg.com%2Fprofile_images%2F625987202909085696%2FKKYbLP8y_400x400.jpg&tbnid=ky1Jb3jyAGSj1M&vet=12ahUKEwjg6OnV0ceCAxWdLDQIHc-tBOwQMygAegQIARBK..i&imgrefurl=https%3A%2F%2Ftwitter.com%2Fdevpost&docid=JrkSXIYc2ahqUM&w=400&h=400&q=devpost%20logo&ved=2ahUKEwjg6OnV0ceCAxWdLDQIHc-tBOwQMygAegQIARBK"
            },
            {
                "activity": "Hackathon 4",
                "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer nec odio. Praesent libero. Sed cursus ante dapibus diam.",
                "link": "https://hackathon4.com",
                "image": "https://www.google.com/imgres?imgurl=https%3A%2F%2Fpbs.twimg.com%2Fprofile_images%2F625987202909085696%2FKKYbLP8y_400x400.jpg&tbnid=ky1Jb3jyAGSj1M&vet=12ahUKEwjg6OnV0ceCAxWdLDQIHc-tBOwQMygAegQIARBK..i&imgrefurl=https%3A%2F%2Ftwitter.com%2Fdevpost&docid=JrkSXIYc2ahqUM&w=400&h=400&q=devpost%20logo&ved=2ahUKEwjg6OnV0ceCAxWdLDQIHc-tBOwQMygAegQIARBK"
            },
            {
                "activity": "Hackathon 5",
                "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer nec odio. Praesent libero. Sed cursus ante dapibus diam.",
                "link": "https://hackathon5.com",
                "image": "https://www.google.com/imgres?imgurl=https%3A%2F%2Fpbs.twimg.com%2Fprofile_images%2F625987202909085696%2FKKYbLP8y_400x400.jpg&tbnid=ky1Jb3jyAGSj1M&vet=12ahUKEwjg6OnV0ceCAxWdLDQIHc-tBOwQMygAegQIARBK..i&imgrefurl=https%3A%2F%2Ftwitter.com%2Fdevpost&docid=JrkSXIYc2ahqUM&w=400&h=400&q=devpost%20logo&ved=2ahUKEwjg6OnV0ceCAxWdLDQIHc-tBOwQMygAegQIARBK"
            },
            {
                "activity": "Hackathon 6",
                "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer nec odio. Praesent libero. Sed cursus ante dapibus diam.",
                "link": "https://hackathon6.com",
                "image": "https://www.google.com/imgres?imgurl=https%3A%2F%2Fpbs.twimg.com%2Fprofile_images%2F625987202909085696%2FKKYbLP8y_400x400.jpg&tbnid=ky1Jb3jyAGSj1M&vet=12ahUKEwjg6OnV0ceCAxWdLDQIHc-tBOwQMygAegQIARBK..i&imgrefurl=https%3A%2F%2Ftwitter.com%2Fdevpost&docid=JrkSXIYc2ahqUM&w=400&h=400&q=devpost%20logo&ved=2ahUKEwjg6OnV0ceCAxWdLDQIHc-tBOwQMygAegQIARBK"
            }
        ]
    },
    {
        "category": "certificates",
        "activities": [
            {
                "activity": "Certificate 1",
                "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer nec odio. Praesent libero. Sed cursus ante dapibus diam.",
                "link": "https://certificate1.com",
                "image": "https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.vecteezy.com%2Fpng%2F18930587-linkedin-logo-png-linkedin-icon-transparent-png&psig=AOvVaw0vHVmWPgfEAp5NSP1aQ4lu&ust=1700193963078000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCMicwJvSx4IDFQAAAAAdAAAAABAI"
            },
            {
                "activity": "Certificate 2",
                "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer nec odio. Praesent libero. Sed cursus ante dapibus diam.",
                "link": "https://certificate2.com",
                "image": "https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.vecteezy.com%2Fpng%2F18930587-linkedin-logo-png-linkedin-icon-transparent-png&psig=AOvVaw0vHVmWPgfEAp5NSP1aQ4lu&ust=1700193963078000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCMicwJvSx4IDFQAAAAAdAAAAABAI"
            },
            {
                "activity": "Certificate 3",
                "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer nec odio. Praesent libero. Sed cursus ante dapibus diam.",
                "link": "https://certificate3.com",
                "image": "https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.vecteezy.com%2Fpng%2F18930587-linkedin-logo-png-linkedin-icon-transparent-png&psig=AOvVaw0vHVmWPgfEAp5NSP1aQ4lu&ust=1700193963078000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCMicwJvSx4IDFQAAAAAdAAAAABAI"
            },
            {
                "activity": "Certificate 4",
                "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer nec odio. Praesent libero. Sed cursus ante dapibus diam.",
                "link": "https://certificate4.com",
                "image": "https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.vecteezy.com%2Fpng%2F18930587-linkedin-logo-png-linkedin-icon-transparent-png&psig=AOvVaw0vHVmWPgfEAp5NSP1aQ4lu&ust=1700193963078000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCMicwJvSx4IDFQAAAAAdAAAAABAI"
            },
            {
                "activity": "Certificate 5",
                "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer nec odio. Praesent libero. Sed cursus ante dapibus diam.",
                "link": "https://certificate5.com",
                "image": "https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.vecteezy.com%2Fpng%2F18930587-linkedin-logo-png-linkedin-icon-transparent-png&psig=AOvVaw0vHVmWPgfEAp5NSP1aQ4lu&ust=1700193963078000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCMicwJvSx4IDFQAAAAAdAAAAABAI"
            },
            {
                "activity": "Certificate 6",
                "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer nec odio. Praesent libero. Sed cursus ante dapibus diam.",
                "link": "https://certificate6.com",
                "image": "https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.vecteezy.com%2Fpng%2F18930587-linkedin-logo-png-linkedin-icon-transparent-png&psig=AOvVaw0vHVmWPgfEAp5NSP1aQ4lu&ust=1700193963078000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCMicwJvSx4IDFQAAAAAdAAAAABAI"
            }
        ]
    }
]

user_response = {
  "name": "Zeeshan",
  "age": 22,
  "race": "Asian",
  "gender": "Male",
  "GPA": 3.99,
  "institution": "University of Calgary",
  "major": "Software Engineer",
  "year_of_study": "Senior",
  "extracurricular_activities": ["Programming Club", "Debate Team"],
  "internship_experience": [
    {
      "company": "Activision",
      "position": "Software Engineering Intern",
      "duration": "Summer 2022"
    }
  ],
  "research_projects": [
    {
      "title": "Natural Language Processing in Chatbots",
      "description": "Explored advanced techniques for improving chatbot interactions using NLP."
    }
  ],
  "awards_and_honors": ["Dean's List", "Outstanding Volunteer Award"],
  "languages_spoken": ["English", "Mandarin"],
  "career_aspirations": "I aspire to become a computer scientist specializing in artificial intelligence. My goal is to contribute to advancements in machine learning and create innovative solutions.",
  "community_involvement": "I have been actively involved in my community by volunteering at a local shelter, organizing charity events, and participating in environmental conservation projects. I believe in making a positive impact and fostering community well-being.",
  "challenges_and_achievements": "One significant challenge I faced was overcoming language barriers when I moved to a new country. Despite the initial struggles, I not only learned a new language but also excelled academically. My proudest achievement is winning the 'Outstanding Volunteer' award for my contributions to a youth mentorship program."
}


add_scholarship('zeeshan',scholarships)
add_resource('zeeshan',resources)
populate_user_profile('zeeshan', user_response)

#print(get_all_scholarship_brief('zeeshan'))
#print(update_scholarship_answer('zeeshan', 'Community Leadership Scholarship', 0, 'aaadsad'))
#print(application_submitted('zeeshan', 'Community Leadership Scholarship'))

# print(login('Zeeshan.chougle@ucalgary.ca', 'Zeemaan1234@'))

print(get_all_resources('zeeshan')[1])