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
    

def get_scholarships_status():
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




# write_chat('zeeshan', [{"role": "system", "content": "You are a helpful assistant."},
#     {"role": "user", "content": "Who won the world series in 2020?"},
#     {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
#     {"role": "user", "content": "Where was it played?"}])
    
#print(read_chat('zeeshan'))


scholarships = [
    {
        "Scholarship Amount": "$10,000",
        "Deadline": "January 15, 2024",
        "Number of Recipients": 10,
        "Estimated Completion Time": "30 minutes",
        "Title": "CONTINUING UNDERGRADUATE AWARDS",
        "Requirements": ["STEM", "Innovation", "Academic Excellence"],
        "Description": "This scholarship is for students with a passion for STEM, a history of innovation, and demonstrated academic excellence.",
        "Questions": [
            "Describe your leadership activities (Minimum 3)",
            "How have you given back to your community?",
            "How have you demonstrated entrepreneurial skills?"
        ],
        "Answers": [
            "Leadership is a cornerstone of my academic and extracurricular pursuits. As the president of the student council, I orchestrated initiatives that fostered collaboration, inclusivity, and innovation within the student body. Leading a team of dedicated individuals, I organized events that not only enhanced the campus experience but also addressed pressing issues. Through my role, I developed strategic plans, delegated responsibilities, and implemented effective communication channels, cultivating a vibrant and engaged community.",
            "Giving back to my community is integral to my values. I initiated and led a local environmental cleanup campaign, mobilizing volunteers to restore natural spaces. Additionally, my involvement in a mentorship program for underprivileged youth allowed me to share knowledge, provide guidance, and inspire future leaders. Through these experiences, I witnessed the transformative power of community engagement and the positive impact it has on individuals and the collective well-being.",
            "Entrepreneurial spirit is evident in my initiatives to address real-world challenges. Founding a student-led startup, I developed and implemented innovative solutions to enhance campus sustainability. Through strategic planning, effective resource allocation, and collaboration with local businesses, I successfully launched eco-friendly initiatives that reduced our ecological footprint. This entrepreneurial journey sharpened my problem-solving skills, honed my ability to navigate uncertainties, and reinforced my commitment to creating positive change through innovative endeavors."
        ],
        "Institution": "University of Calgary",
        "Image": "data:image/png;base64,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",
        "Submitted": False,
        "Status": "accepted",
        "id": "1",
        "my_university": True
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
        "Institution": "Stanford University",
        "Image": "data:image/jpeg;base64,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",
        "Submitted": False,
        "Status": "applied",
        "id": "2",
        "my_university": False
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
        "Institution": "MIT",
        "Image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAARMAAAC3CAMAAAAGjUrGAAAAaVBMVEX///+jHzSKi4z89/icABSeAB/ixci+dH2hESvr2NqdAByhFi6zV2L37/CcABakITbIjJO+v7+EhYbMzMzv3uDr6+vLk5mfACTWrLCWAACaAAeuRlS5aHLz5+jTpaqbAA3Gh4/lzM98fX4g7gTHAAABz0lEQVR4nO3dwU5TQQCGURAoUBWxolgEW3n/h3R9+43JjYXGyjnrP7P4dm0md05OAAAAAAAAAAAA4Aicjf3F6CWP+tNsln2TXK/PBx5+TFePw9V6MRl9HI42y+lRt+Ojfk5Xi+FqnvX1vk2WpwPvP0xXl1ej1cVOk5vR6PTT9Khv96PR/fedJhfDs2ZZahKalCalSWlSmpQmpUlpUpqUJqVJaVKalCalSWlSmtTxNbm9uRo4322yGa3meTi6Jovt7cD213R1N1zNs306tiZHQJPSpDQpTUqT0qQ0KU1Kk9KkNKmDNzn7OrR7w+tuaN9fd/McvMnn59XA85fparFeDmweX6FAHb7J6t3AarfJ8D+lq8tXKFCalCalSWlSmpQmpUlpUpqUJqVJaVKalCalSWlSmpQmpUlpUpqUJqVJaVKalCalSWlSmpQmpUlpUpqUJqVJaVLzmjxuRtcQd79Z97aaPI2vq04vtb6xJrNoUpqUJqVJaVKalCalSWlSmpQmpUlpUpqUJqVJaVKalCalSWlSmpQmpUlpUpqUJqVJaVKalCalSf0/TWa9NzrLvPdG536zbviS6GG+WTf3ndgDH/WiZwEAAAAAAAAAAMC/6DcAbJjOtbltGAAAAABJRU5ErkJggg==",
        "Submitted": False,
        "Status": "in_progress",
        "id": "3",
        "my_university": False
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
        "Institution": "Columbia University",
        "Image": "data:image/png;base64,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",
        "Submitted": False,
        "Status": "in_progress",
        "id": "4",
        "my_university": False
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
        "Institution": "University of California, Berkeley",
        "Image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Seal_of_University_of_California%2C_Berkeley.svg/1200px-Seal_of_University_of_California%2C_Berkeley.svg.png",
        "Submitted": False,
        "Status": "interview",
        "id": "5",
        "my_university": False
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
        "Institution": "Yale University",
        "Image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAMAAAAJbSJIAAAA21BMVEUAKlz///8AKFvj5+wAFlTBydIAFFTBydQGL2Hb4ecAJl0AJloAIVcAElGzvMmrsLwAGFMADE8tQ25lcYsAHlcAJl6YpLfIzdwAGlTw8vYAEFEfOmj///0AAEymsMCMmK1sfZg3UHdldZUACE8AAE+DjJ8AAEb3+P5cbI4AIVMlPGfS1uOSoLIJNWcALGHx9fU9VXuyu8xGXYJZaYW3wtKbqL8cNl9+i6U0TntnfJRseZpRZolbboxEW4OXoLaBk6oAAEArRWk8UXDd3+1dbJNdaoQjRHN9kK6fqLLsSHuKAAAQyElEQVR4nO2djXeiuBbASUABE3xgUwuIiNqp0/rVWjt2R6e+6byd3f//L3pJ+BRBrW2n0sM9Z08ZCDE/ktzc3NxkBYFIn1mIIJBR5TPLCAtSBXxmqVRLwqJLSOiIn1GShOJYUD6djMUkoYDgZxM02SBUoPDZBColYdGlJCy+lITFl5Kw+FISFl9KwuJLSVh8KQmLLyVh8aUkLL6UhMWXkrD4UhIWX0rC4ktJWHwpCYsvJWHxpSQsvpSExZeSsPhSEn6QYF3Db5TVCRIiYktf3bn3RoinRojMNvLqU1qWpv42OZ4SIUR6u9UZBjGvDfRGuZ4MIamSmStGQb2u8Ub5ngohVLy5lYhadsy3KsmpEOIepUoQ1t+qCg8ihDhfUp0FHZQqQ/DSmoIkofY2fAcRwpuzfJltFB7dZqe63Y+Iao37jvoxhKwB5YpsJ5NKbnaquwM0P0RYN9YfQ/jV7/sbZQ7/Nd8oif7gP3RS6R4OHduuwrHijxIKwrefq4QeD2XY7P1spV5QvjV6D2rya1h1r/tNObQ4uvsRhFBAiOjVnrVRj3KjKl3XIEy9gGhbq858Rvbf2tQIOlxB6//5mDrkCXF7nqjAxdWOcuP2yE+ljvWXDT/SBxLSpFd3ce+SjV1F1zo+IH6p9fyxhILQvogrsUfy06EGH9us1vVLi/PRhDUlNqzU/FYKtTnvgyvzxcX5aEKBREOjAzpSXiq89At5+fLifDihoMuBPnXANHd6Q7hpMhCOmP58PCHqxtZjXcpOTBa+ts2t4x3y8YSC1ImVzTJT2cAx76zqEW30JAgRiY0bNdMW03yz5PGoedgJEArkPrZsFhnjOe7y5+5xJTwFQqEfmTbOoLalTKDEbWdrcpyX5SQIa61Y2dxtzcSD8cR7+VDI5SQIBSmaxNHelrZabK5mKsd6WU6DUDDiqbja33xkP/Hbt8d6c0+EEM/ieZS3MWKgG9Y9QTOveIhIRrttaHreF9hPOGHTHFOyDUOTTHxAcY8hhP1okgEslFQpbZndE3PUDOnffHGHlji866yk7GnVfkJILpWzjjuX5bnb6U2MvZDHEFKAQYToJhw1gb/jr0w1IxmLIYi/zBPJqse9hBJJ5gLA0LP39Ijj/KX6IvwFB3TjCrN5B5WzXJ1E6wzAhoi3GSbRHkKsN1O50Hxm2s5CH0fIRr2wJ15EP6D7Ft3v7Y+KbC8sWcIRkqGPdhJCezXg78vN717CcdSxt9O+mhDfxgX9HtQFHSjZzz/ZW3mQFp+SPN2c/2haEaJjbfehXYTI9O3BkW3omFTb0UcDo10O8mO9+gnPaKhYtDvmRhSNtHNKMJd8kFwaSLiWzkMtRUmbW9OPHYSQ+GqsG9aYfhPNx+939MVjCdE4biUjXlA2htBiL7d+TDrjqdY+Duw/RS8OtuYf+YSwesE+ijiOey++mQbfytrh8Dp6ZSZWNmD6k1Ui4TpObqcTmiu/pkmY9WU81vxIt9N8wn6ds8yS6smMXA7rfCvx+LUnPdbacpX+mscvW+mhEDX8jreOplqwaoV+gqf0/CuXsOqbiilbohoejKRufdg3IMS3sfN+iZHAO8U6PQIgW/VTJQYVM6r+u3RN5RHiR37XGm+WL/AI0f7/mDuXOZ4Q2rGyUW2tyXqJutVY9MBMT+YMcagFhymzNo8Q+sbS1qwTTkJtsMhtpq9YIYUk9i0ulKAus9M4QE06daJTt4ZpNZ9DiFcgO387zMnNXft5zRpw5Ft0nCnvlNsLt4FXCqidZPONhpr01CSHEBp+n7fs8JAnFIgduo0yDalXE274wNkIvqVmBLNJDZDFY9/YaERRRzywDsPuJtsTKsqYyrcbJo2bMKetb/U2hKiVJKTqcvttRevrJD0mvJQwcG45U4vJgAvYlGmuMn1dpEJ1FNcgGGY7FzPumWHbOoww1if5Yr0TIUz4FjOsmTzRQ7Nmq/dkEl4HjRSIKpfwpDkrIe/USqMZIS9T7m/sIEzPCjIJwyp3fldN09TPA1FagfAumb9O9Mp4GjuybF4Qh2a+rA5tObg53tBkVKMynerr1XewSwMxKkcQ5q/WZxHCSeD5GkyO8eD9ecIaMq/qwTsHWW0wmEKAwY5F2Xz504SI6OM4MKh+SD9E0Wz71AmhgojU2nAkuekpcBYhn3gymZ44IcT22PN1xkVYiVvWZCZhYJSCwfnp9kMIsaas5n78gvvjv2E/PKwOo3nu72OWe/4EIcUj94FvTF2MbWRHhNVU0ixC4gX3nNkxiwXvT4hMY9YMTJ/5kpgQCjHhQa00sioWx3TEdyc0GqNglm81G5Jvg7+QMNQ0xy27vjdhtJ4qrgUp7EYRYTMd7JA5WjyHPyHudP3myDsThjM7AH5KCe//iwhhK/IlZMdG7JZ3JoxYxKTFpdXz3sm0S0lsIRwR/f2+hJCEK+LDZAN7IWGUHEzzXWq58r6EsZKobMzZ/SI728oxkzARhr1l5u2Xdyb0oqdJR80LCRMdEfRyvIb5I+X7EpIv4dNOBmHGAJdNGPVmOuR0s5QN1JfneSV8X0KpGT4dvYKQudeD2w5QxxnV1e/kh9G9L2E01QWVDE3jJN6BuwgFOxGALXbTP4RYXEFuqOTbEd61t9/VozoUY6cbQu1hQDhs+3RIa+0kRL+jKCVam147WfXIaLDRxM3Tsq8lvIwInYxFaxIvwa2DIkNkPMYOuiW7iyTpIrDf8tYtpDgjyvhr2dYxgsxTQwz8wON5+3klf6U3UVvGv2u1tpQAnZ474eOZgTHCunRDm1SkG52ebuqwQ9u4P8uwI8JNzx1s321sabHcr61rgifdhexXa76j7zUrM1g3EwFgLLrCTnu3+5E54gB31r3tNVkDXX+PX5qqKnt4xhoAJNFij3OTcqC3ZZCWyO9tbXXN1xLCa6JrVeX5SUxtFqrPBFsyE3sQImduQqa99s3Gaw5wVraATY3MfsUtoqfQrOKwOdhPbvdg7zvBXyCf7wobOoqwcbbo3A23Xe0sUKHSXPeWsVrROulEw4aZ0LFc1EcdNrx1XU3co1kN3fUysepodDa3XoUV6PV3mnLHEJqLrF9K1lIrzsbYRBQXbI4BlUTrBU18ndRJG8VPGuzSj+F2gqayJ9DzGMKc0iQwkovR9jIul7pW/LjM61bYrZx6lymZyFWxKeqGExibKzm5D9NR16298fJHtdJxY49spMZ45qqiZanurGaGDQqRlUzvDUeNYN6Yk+dmeSCWbnpuRRVFdVhxvzdMc/9c4zhNg3ZLej/btWQKikL4GBaDSzVFMaWEIbA/Jw6ps3xqpFrFB22K+1M7nbe28eXcOzS3F6Q9kb3c7yclYfGlJCy+lITFl5Kw+FISFl9KwuJLSVh8KQmLLyVh8aUk/Dg52k2VzmcPIdJ94Y7c4JpeSuxvsNSEgxR8mYxdSToK7uk6Ym5DfkUg1qXwtmTz1TNdkiTNpqLpJPnLENtkPCYavxnmZbJVNk1PiGSbQpgpWysxo6vDCdGs7jabTddtjiFEd/z6boYUfuUfnHDdo0+bD25TwUueuOnWu15wdddF2POfP+n/uH5e9I9brxMB6m79zp3P5Qt5/rSqxSUj0LsQrakoe2Mo4EX4mg4bwzovjP/vpivX+17wdIEF4roP9DJ1tOseQtjw2Iq09XRPn8Azd8p2T98g4YwvraxYLcIujxp1VxA2euz2tNlr3bJ1PXr1VwvWnlnQrNNcYn4B+IaCKVBpU0CrNVu/aK5ZZJ94Hy4/kpkK5r1Vk/7Y6pp+ZJ6XuD7D/PwptiXBz8aihWl3FwxA9W6RgO6bDrDWqSMM97VSiK8uAPjS5utX2H4E6iVrOv55ZQO+DQji9r9g0cb8iiJ2aGJEruYAzK/Ya8i8HIKljemFYgFrUjUlsyWLJm+AN/TzKbSxumwl3v9xfDsAiz7GkiLzb4iwRMvYkGgGDaB2a9hsUCSJYNQDwz4yayJw5lesJPhqak30lKN/v6Yx6Bf8EnxeOA63bpgLQL+k6G9zJR7o+U2j6oaBJXgGHMvPDrWcIT/8DLUoIV+XIrcqz5KWmd+BNSuKSNFkINb4B51MVyxbhGgZ2T5V1LC6BCLcpb98jqBgrH8ZPHYu2JwrPWVEvu0ntDMJKdTKCjfF4l54uJkUEQo6fdzjK5zmGvzFH8OIELZc3ioiQvbz/v4SlkgMojRlv0+di/6hu6irsiSIEdbYxY3KAt3Y2il7ACe0PFsALyRUxJjwnq3v8o3i+GsGIatO/9w6olp+hHZMKGB/3T4kZEdsBdGmkMVdzPiKDf7q96mQUGjxqvIJWQLlf+wTQsTCq0y2EE6216JeQbhqs8VPj5Ylk5BtIuCFp+11FOzj5oRsD6He+RttElIl9NVv6Yxn4ElsfAqOdo0Iof9SRBgEe7FtQ5ZgLhObjd+GELepnh3c4mxCyMrFume17gTRPJxwolHFMhZ5aEJICJEyAPVgsdPf5qQuxlUYrJZHhL4kCINiMVXUvFLFrBjiVxHygzDEMcok5CFfssbakBzEgvAQvGC0SBAqpn7ZBPXolJQgVsxqhnvv9xEKZMWGpuzdc68jZMoRVAjJJMS3wJm2IFmAFU4Q3jFRE4TTzmItAzfWEbC6vOAL/OIqbrc7CaHEjqW4yzwC5HWEkMxoQdx2JqGAVdZM26oYnpPJW6lgVKuGEbdSx2FDuGMljzrB0oyfyz7obmqaXEI2gOREtu0n7FcShBNrg5AfreAAb5lJqI+YNv0NOmH/j3Wp2fk70Uqrl/RbqOHBYVwfYrvBjCl/y8lewqSWfjkhiwscBWVEP8OAs5AQaS5F/CeTkGnTKXZBtJknMR4iaEaELYTpH1D3D0UxR/4QgS5pXpU/QAhZfGFwKAPUvTAklBJ+x/49HjcSmLsbhNCkVfN1EIefJ8uBHrAQjxb8YIIF/3hS3fVbNYvz/yOE6DetpJ7Bmw4Rp41aSBicEFHjOSwy6pAdyeMMQBx9nhzxb4d6gtA/OoB3RbPjPPLMyDIMvM0gVDdjgl/VSgWDnUXioWqVNFTw5A9aqO9xC5sX9nFKTQpeI5HlHRclPpQDIZOWY9pq0xlhdSKzUxeRznTpjYkEzM6TtLoagtgD4k/tGuHLOrDYvliIq7SMrdBcgVhidagkQmkgNhWqmBppo/tQQv8EEVGuqGxfjm9+Pa+nwHGX/v5iveeAfxl5a9axWGDXLDzdmp2F4EU2bbfHpz0VJhY7VxJ1z9gd0XtGkPAYv9FzC9/Tvw+3jR9zILKgbvRzyT5xZfUcWEGzYL40CwsLldkZO/tA7D0fSQglb8iiIi156fcQKAyHFxcXw19BQzWepqw54ZXKbl8Mh+FZ9GQ9FUNAshAtUeWP+dsuNRgueHp6h9rN5n2FbUC/04ReXZwCa6quIWsY5GEY5Mq7KXkaBi/9akRNRQ2S/Bpvl/8gPw3ExrjbfUQGDswoqBlcojmrH36G/buGHbWWye94/zXpty/7RiQ6+z92BNea/3bfNliEKtGkVrfbMoKjCUmQaRApbkY5RDmj8E7WkH+oJwru3BGeeXKC/+AofxI72uOtfGKn62t7KykJiy8lYfGlJCy+lITFl5Kw+FISFl9KwuJLSVh8KQmLLyVh8aUkLL6UhMWXkrD4UhIWX0rC4ktJWHwpCYsvJWHxpSQsvpSExZeSsPhSEhZfSsLiS0lYfEkThv/7vc8jaJNwgmufTc4nSUJ/69xnE5Ak/LRSEhZfKCEZyZ9ZRoTtH//MQuD/AZkgzzE2J7JCAAAAAElFTkSuQmCC",
        "Submitted": False,
        "Status": "rejected",
        "id": "6",
        "my_university": False
    },
    {
        "Scholarship Amount": "$9,000",
        "Deadline": "June 5, 2023",
        "Number of Recipients": 7,
        "Estimated Completion Time": "40 minutes",
        "Title": "Amazon Future Innovators Scholarship",
        "Requirements": ["Innovation", "Technology", "Community Involvement"],
        "Description": "For students who have demonstrated innovation in technology and active involvement in their community.",
        "Questions": [
            "Describe a technology project where you showcased innovation.",
            "How do you envision using technology to benefit your community?",
            "Share your experience in a community involvement initiative."
        ],
        "Answers": [
            "I developed a groundbreaking app for community engagement.",
            "Using technology, I aim to enhance community communication.",
            "I led a successful community outreach program."
        ],
        "Institution": "Amazon",
        "Submitted": False,
        "Status": "rejected",
        "id": "7",
        "my_university": False,
        "Image": "data:image/png;base64,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"
    },
    {
        "Scholarship Amount": "$12,000",
        "Deadline": "May 25, 2023",
        "Number of Recipients": 5,
        "Estimated Completion Time": "35 minutes",
        "Title": "McKinsey Global Leadership Award",
        "Requirements": ["Leadership", "Global Perspective", "Problem Solving"],
        "Description": "For students with exceptional leadership, a global perspective, and a proven track record in creative problem-solving.",
        "Questions": [
            "Share an instance where you demonstrated effective leadership.",
            "How do you approach global challenges with a unique perspective?",
            "Provide an example of a complex problem you solved."
        ],
        "Answers": [
            "I led a diverse team to success in a challenging project.",
            "I believe in addressing global issues through collaboration and understanding.",
            "I tackled a complex problem by..."
        ],
        "Institution": "McKinsey and Co.",
        "Submitted": False,
        "Status": "rejected",
        "id": "8",
        "my_university": False,
        "Image": "data:image/png;base64,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"
    },
    {
        "Scholarship Amount": "$15,000",
        "Deadline": "June 10, 2023",
        "Number of Recipients": 3,
        "Estimated Completion Time": "50 minutes",
        "Title": "Google Impactful Technology Scholarship",
        "Requirements": ["Technology", "Impactful Projects", "Innovation"],
        "Description": "For students who have made a significant impact through innovative technology projects.",
        "Questions": [
            "Describe a technology project that had a meaningful impact.",
            "How do you approach innovation in your tech projects?",
            "Share your vision for the future of technology and its impact on society."
        ],
        "Answers": [
            "I developed a technology solution that positively impacted healthcare.",
            "Innovation is at the heart of all my tech endeavors.",
            "I envision a future where technology transforms lives by..."
        ],
        "Institution": "Google",
        "Submitted": False,
        "Status": "applied",
        "id": "9",
        "my_university": False,
        "Image": "https://blog.hubspot.com/hs-fs/hubfs/image8-2.jpg?width=600&name=image8-2.jpg"
    },
    {
        "Scholarship Amount": "$6,500",
        "Deadline": "June 15, 2023",
        "Number of Recipients": 8,
        "Estimated Completion Time": "45 minutes",
        "Title": "Microsoft Innovation Scholarship",
        "Requirements": ["Innovation", "Technology", "Future Vision"],
        "Description": "For students showcasing innovation in technology and presenting a compelling vision for the future.",
        "Questions": [
            "Highlight a technology project where innovation was a key factor.",
            "What role do you see technology playing in the future?",
            "How do you plan to contribute to the future of technology?"
        ],
        "Answers": [
            "I developed a cutting-edge software solution.",
            "Technology will be a driving force in solving future challenges.",
            "I aim to contribute by..."
        ],
        "Institution": "Microsoft",
        "Submitted": False,
        "Status": "applied",
        "id": "10",
        "my_university": False,
        "Image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Microsoft_logo.svg/2048px-Microsoft_logo.svg.png"
    },
    {
        "Scholarship Amount": "$10,000",
        "Deadline": "June 20, 2023",
        "Number of Recipients": 5,
        "Estimated Completion Time": "40 minutes",
        "Title": "Facebook Social Impact Scholarship",
        "Requirements": ["Social Impact", "Innovation", "Community Engagement"],
        "Description": "For students using innovation to make a positive social impact through community engagement.",
        "Questions": [
            "Describe a project where you used innovation for social impact.",
            "How do you engage with your community to drive positive change?",
            "What role do you think social innovation plays in community development?"
        ],
        "Answers": [
            "I initiated a project that positively impacted the local community.",
            "Community engagement is central to my approach in driving positive change.",
            "Social innovation is crucial for sustainable community development."
        ],
        "Institution": "Facebook",
        "Submitted": False,
        "Status": "accepted",
        "id": "11",
        "my_university": False,
        "Image": "https://1000logos.net/wp-content/uploads/2021/10/logo-Meta.png"
    },
    {
        "Scholarship Amount": "$8,500",
        "Deadline": "June 25, 2023",
        "Number of Recipients": 6,
        "Estimated Completion Time": "35 minutes",
        "Title": "Apple Future Innovators Award",
        "Requirements": ["Innovation", "Technology", "Creativity"],
        "Description": "For students showcasing creativity and innovation in technology projects.",
        "Questions": [
            "Highlight a technology project where creativity played a key role.",
            "How do you foster creativity in your tech endeavors?",
            "What do you see as the future trends in technological creativity?"
        ],
        "Answers": [
            "I developed a unique and creative solution in my latest tech project.",
            "Creativity is at the core of my approach to technology.",
            "I envision the future of technology being shaped by..."
        ],
        "Institution": "Apple",
        "Submitted": False,
        "Status": "accepted",
        "id": "12",
        "my_university": False,
        "Image": "https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg"
    },
    {
        "Scholarship Amount": "$7,000",
        "Deadline": "July 1, 2023",
        "Number of Recipients": 5,
        "Estimated Completion Time": "30 minutes",
        "Title": "IBM Future Technology Leaders Scholarship",
        "Requirements": ["Technology", "Leadership", "Innovation"],
        "Description": "For students with a passion for technology, strong leadership skills, and a history of innovation.",
        "Questions": [
            "How do you envision the future of technology?",
            "Describe a leadership role you've undertaken in a technology-related project.",
            "Share an innovative idea or project you've worked on."
        ],
        "Answers": [
            "I believe the future of technology will involve...",
            "I led a technology team in implementing...",
            "One of my innovative projects involved..."
        ],
        "Institution": "IBM",
        "Submitted": False,
        "Status": "accepted",
        "id": "13",
        "my_university": False,
        "Image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAMAAAAJbSJIAAAAb1BMVEX///8AAAB9fX1JSUnS0tKSkpKvr696enqqqqo+Pj7i4uL09PTPz8+ysrLg4OC2trbZ2dnq6urGxsajo6NtbW2JiYlycnLw8PDAwMAiIiKDg4MtLS1BQUFMTEw5OTliYmIMDAyenp4VFRVkZGQcHBw8JRT8AAAC6ElEQVR4nO3a63qiMBCA4aBYFFFBRO16aGv3/q9xBTGBJMjuihH7fO+vQsLEKTohgBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA4Eg6tkoTITbjtwazrT+tBvHNLuNQG8gSZuwkQ6/BUoi4qa3wsVBBflnaV/VxrMH6naHn7ZbXIJml9bN2lq1dep+h5wVlkIGtcdY+jpMMgf57n1jtIiHmx2G7Q15Qvva2pkCN4k9sHXZOMryr0uTySc1aKD1vI0dZ2zu8Roafwj4fnqVtozjJcBVYrWMhkvXgL6zPX9NFYGsJRtdBYnuktZMM8WOE0lRvmqo2W/8wkTuTUHfZv9F3zx+ej2Gqfv0zvS1SbfKTJZVyMZA9V0YpuRwwNPZv9EEerpLhQm/zWzJUFTMwMhlpwa+ML8rD3XMO5QrDcg6L+SA1d7s/hyLyS5Ex+FS1qX+971t2zn1d0Ribu53khJ9mJMV6U5iNbqj+bBdmcxYLc+coe2qlMWppZBaKiqTSU11fD0/XvwaqKB16UktvzRamZbWnmi0+5Gpjp9Ydi75meOsc1jurDA+WdUmwfWaGQP91/jsU4qh1jURvK83NWrqt9lQZDoX4qnc8if5m+D/z4b5+cX6WPTnDrq9p8hVVWruKOS+GY7XpLjH8IB2vD4uvehipTvn2JqptutX1Gn+Sb85Un6O23a9a2nafRj2rrs2HtaDFvZy+zBad3GsrzqH4ltvFnPLUc9j1/dJEO7I5ENCum2dPa+3w8qIlLCIE5T3jSO+1av5YHfIa/NPzQ+MJ6bCMfrldU5bnhXHsa2SY3sowqybypAy7eY5/rB99/C6j5yH2Wbmx3WmDvDvJEOi/uyrN9VUD412Mo4z/25MLibfnVJo7MjzJmzRGLT3I+KlK49Vmi2Hl/Vcjw71sSjL558yI4STDTt4RjvTDK0uwygJZHysVAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAODIH2HOMdUHfE1pAAAAAElFTkSuQmCC"
    },
    {
        "Scholarship Amount": "$9,500",
        "Deadline": "July 10, 2023",
        "Number of Recipients": 3,
        "Estimated Completion Time": "40 minutes",
        "Title": "Uber Global Impact Scholarship",
        "Requirements": ["Global Impact", "Innovation", "Community Involvement"],
        "Description": "For students making a global impact through innovative projects and active community involvement.",
        "Questions": [
            "Describe a project where you made a global impact.",
            "How do you incorporate innovation into your projects?",
            "Share your experiences in community involvement and its impact."
        ],
        "Answers": [
            "I initiated a project that had a positive global impact by...",
            "Innovation is a key element in all my projects, including...",
            "I actively engage with my community by..."
        ],
        "Institution": "Uber",
        "Submitted": False,
        "Status": "interview",
        "id": "14",
        "my_university": False,
        "Image": "https://helios-i.mashable.com/imagery/articles/03y6VwlrZqnsuvnwR8CtGAL/hero-image.fill.size_1248x702.v1623372852.jpg"
    },
    {
        "Scholarship Amount": "$8,000",
        "Deadline": "July 15, 2023",
        "Number of Recipients": 4,
        "Estimated Completion Time": "35 minutes",
        "Title": "NASA Space Exploration Grant",
        "Requirements": ["Space Exploration", "STEM", "Research"],
        "Description": "For students with a passion for space exploration, a background in STEM, and a history of research.",
        "Questions": [
            "Why are you interested in space exploration?",
            "Describe your involvement in STEM activities.",
            "Share details about a research project you've worked on."
        ],
        "Answers": [
            "Space exploration fascinates me because...",
            "I actively participate in STEM activities such as...",
            "I conducted research on..."
        ],
        "Institution": "NASA",
        "Submitted": False,
        "Status": "interview",
        "id": "15",
        "my_university": False,
        "Image": "https://1000logos.net/wp-content/uploads/2017/03/NASA-Logo.png"
    },
    {
        "Scholarship Amount": "$10,000",
        "Deadline": "July 20, 2023",
        "Number of Recipients": 6,
        "Estimated Completion Time": "45 minutes",
        "Title": "Tesla Innovation Scholarship",
        "Requirements": ["Innovation", "Electric Vehicles", "Engineering"],
        "Description": "For students with a focus on innovation, a passion for electric vehicles, and a background in engineering.",
        "Questions": [
            "How do you see innovation in the field of electric vehicles?",
            "Describe your experience in engineering projects.",
            "Share an innovative idea related to electric vehicles."
        ],
        "Answers": [
            "Innovation in electric vehicles involves...",
            "I've been involved in engineering projects such as...",
            "One of my innovative ideas for electric vehicles is..."
        ],
        "Institution": "Tesla",
        "Submitted": False,
        "Status": "in_progress",
        "id": "16",
        "my_university": False,
        "Image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Tesla_logo.png/1200px-Tesla_logo.png"
    },
    {
        "Scholarship Amount": "$6,500",
        "Deadline": "July 25, 2023",
        "Number of Recipients": 8,
        "Estimated Completion Time": "40 minutes",
        "Title": "Goldman Sachs Finance Excellence Scholarship",
        "Requirements": ["Finance", "Leadership", "Academic Excellence"],
        "Description": "For students with a strong interest in finance, exceptional leadership skills, and a history of academic excellence.",
        "Questions": [
            "Why are you interested in a career in finance?",
            "Describe a leadership role you've taken in a finance-related context.",
            "Share your academic achievements in the field of finance."
        ],
        "Answers": [
            "I'm interested in finance because...",
            "In a leadership role in finance, I...",
            "My academic achievements in finance include..."
        ],
        "Institution": "Goldman Sachs",
        "Submitted": False,
        "Status": "in_progress",
        "id": "17",
        "my_university": False,
        "Image": "data:image/png;base64,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"
    },
    {
        "Scholarship Amount": "$9,000",
        "Deadline": "July 30, 2023",
        "Number of Recipients": 5,
        "Estimated Completion Time": "35 minutes",
        "Title": "Johnson & Johnson Healthcare Innovation Grant",
        "Requirements": ["Healthcare Innovation", "Research", "Community Impact"],
        "Description": "For students focused on innovative solutions in healthcare, with a background in research and community impact.",
        "Questions": [
            "How do you envision bringing innovation to healthcare?",
            "Share details about your involvement in healthcare-related research.",
            "Describe a project where you had a positive impact on the community's health."
        ],
        "Answers": [
            "I believe healthcare innovation involves...",
            "In my research in healthcare, I...",
            "I positively impacted the community's health by..."
        ],
        "Institution": "Johnson & Johnson",
        "Submitted": False,
        "Status": "in_progress",
        "id": "18",
        "my_university": False,
        "Image": "data:image/png;base64,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"
    }
]

resources = [
    {
        "category": "Certifications",
        "activities": [
            {
                "activity": "Embedded Certificate in Entrepreneurial Thinking",
                "description": "This certificate program equips participants with a holistic understanding of entrepreneurial principles and fosters a mindset that embraces innovation and creative problem-solving. Participants gain valuable insights into the entrepreneurial ecosystem, enhancing their ability to identify opportunities, navigate challenges, and contribute effectively to the dynamic world of startups and innovation.",
                "link": "https://www.google.com/imgres?imgurl=https%3A%2F%2Finnovationsoftheworld.com%2Fwp-content%2Fuploads%2F2023%2F07%2Fuc-hunter-hub-full-colour1.png&tbnid=o2wY6WFh14QMYM&vet=12ahUKEwjDiMCd9MqCAxVeFzQIHYexCdEQMygAegQIARBL..i&imgrefurl=https%3A%2F%2Finnovationsoftheworld.com%2Fhunter-hub-for-entrepreneurial-thinking-the-hunter-family-the-creation-of-the-hunter-hub%2F&docid=zORbe1iXa2ClaM&w=1390&h=198&q=hunter%20hub%20ucalgary%20logo&hl=fr&ved=2ahUKEwjDiMCd9MqCAxVeFzQIHYexCdEQMygAegQIARBL",
                "image": "https://research.ucalgary.ca/sites/default/files/styles/ucws_image_desktop/public/2022-03/Hunter%20banner_0.png?itok=A3hllxdn"
            },
            {
                "activity": "Schulich Leadership Program",
                "description": "The Schulich Leadership Program is designed to cultivate leadership skills in individuals aspiring to make a positive impact in their respective fields. Participants engage in a dynamic curriculum that focuses on strategic leadership, ethical decision-making, and effective communication, preparing them for leadership roles in diverse professional environments.",
                "link": "https://www.google.com/imgres?imgurl=https%3A%2F%2Fstatic.wixstatic.com%2Fmedia%2Fa7fdd6_c2e83f8b4f0a401f80f61219d7d29864~mv2.png%2Fv1%2Ffill%2Fw_560%2Ch_272%2Cal_c%2Cq_85%2Cusm_0.66_1.00_0.01%2Cenc_auto%2Fa7fdd6_c2e83f8b4f0a401f80f61219d7d29864~mv2.png&tbnid=ZAqU7ypebr21BM&vet=12ahUKEwjc1avd8cqCAxVKIDQIHYlvATgQMygCegQIARBO..i&imgrefurl=https%3A%2F%2Fwww.pesucalgary.ca%2Fschulich-school-of-engineering&docid=OU8ocVuNRCwPnM&w=560&h=272&q=schulich%20school%20of%20engineeering%20logo&hl=fr&ved=2ahUKEwjc1avd8cqCAxVKIDQIHYlvATgQMygCegQIARBO",
                "image": "https://www.ucalgary.ca/sites/default/files/styles/ucws_image_desktop/public/2020-11/24-Schulich%20school%20of%20Engineering.jpg?itok=vOkMh76h"
            },
            {
                "activity": "IBM Certified Data Engineer - Big Data",
                "description": "The IBM Certified Data Engineer for Big Data certification confirms proficiency in designing and building big data solutions. It encompasses skills in data architecture, integration, and analytics, ensuring professionals can effectively manage and analyze large-scale datasets.",
                "link": "https://www.google.com/imgres?imgurl=https%3A%2F%2Fstatic.wixstatic.com%2Fmedia%2Fa7fdd6_c2e83f8b4f0a401f80f61219d7d29864~mv2.png%2Fv1%2Ffill%2Fw_560%2Ch_272%2Cal_c%2Cq_85%2Cusm_0.66_1.00_0.01%2Cenc_auto%2Fa7fdd6_c2e83f8b4f0a401f80f61219d7d29864~mv2.png&tbnid=ZAqU7ypebr21BM&vet=12ahUKEwjc1avd8cqCAxVKIDQIHYlvATgQMygCegQIARBO..i&imgrefurl=https%3A%2F%2Fwww.pesucalgary.ca%2Fschulich-school-of-engineering&docid=OU8ocVuNRCwPnM&w=560&h=272&q=schulich%20school%20of%20engineeering%20logo&hl=fr&ved=2ahUKEwjc1avd8cqCAxVKIDQIHYlvATgQMygCegQIARBO",
                "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcROITIvBYgaTG9g0l4kLpqx-Mc6pNH5iwHrKw&usqp=CAU"
            },
            {
                "activity": "AWS Certified Solutions Architect – Associate",
                "description": "The AWS Certified Solutions Architect – Associate certification validates expertise in designing distributed systems on the Amazon Web Services (AWS) platform. Holders of this certification demonstrate proficiency in architecting scalable and cost-effective solutions, making them valuable contributors to cloud-based infrastructure projects.",
                "link": "https://www.google.com/imgres?imgurl=https%3A%2F%2Fblog.adobe.com%2Fen%2Fpublish%2F2021%2F08%2F31%2Fmedia_1649ebc3fbbce0df508081913819d491fc3f7c7a9.png%3Fwidth%3D750%26format%3Dpng%26optimize%3Dmedium&tbnid=Mqqu7GA7Pb3AwM&vet=12ahUKEwiFm8_58cqCAxX2ADQIHSvPD6IQMygJegQIARBb..i&imgrefurl=https%3A%2F%2Fblog.adobe.com%2Fen%2Fpublish%2F2021%2F08%2F31%2Famazon-web-services-works-with-adobe-experience-cloud-as-it-reimagines-b2b-marketing&docid=1jyf6kaXYeNvoM&w=750&h=422&q=amazon%20cloud%20logo&hl=fr&ved=2ahUKEwiFm8_58cqCAxX2ADQIHSvPD6IQMygJegQIARBb",
                "image": "data:image/jpeg;base64,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"
            },
            {
                "activity": "IBM Certified Solution Architect - Cloud Pak",
                "description": "This certification validates expertise in designing, building, and deploying scalable and resilient solutions using IBM Cloud Pak for Applications. It covers various aspects of application modernization, containerization, and cloud-native development.",
                "link": "https://www.google.com/imgres?imgurl=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Fthumb%2F5%2F51%2FIBM_logo.svg%2F2560px-IBM_logo.svg.png&tbnid=1OyQOXfLcZdDiM&vet=12ahUKEwjbtrCM8cqCAxVaJDQIHWeTCTcQMygBegQIARBD..i&imgrefurl=https%3A%2F%2Fen.m.wikipedia.org%2Fwiki%2FFile%3AIBM_logo.svg&docid=91fXQvrmR7ucSM&w=2560&h=1027&q=ibm%20logo&ved=2ahUKEwjbtrCM8cqCAxVaJDQIHWeTCTcQMygBegQIARBD",
                "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcROITIvBYgaTG9g0l4kLpqx-Mc6pNH5iwHrKw&usqp=CAU"
            },
            {
                "activity": "AWS Certified Developer – Associate",
                "description": "The AWS Certified Developer – Associate certification attests to a professional's ability to design, deploy, and maintain applications on AWS. Certified individuals showcase their proficiency in coding, deploying, and debugging cloud-based applications, making them adept in leveraging AWS services to create scalable and secure applications.",
                "link": "https://www.google.com/imgres?imgurl=https%3A%2F%2Fblog.adobe.com%2Fen%2Fpublish%2F2021%2F08%2F31%2Fmedia_1649ebc3fbbce0df508081913819d491fc3f7c7a9.png%3Fwidth%3D750%26format%3Dpng%26optimize%3Dmedium&tbnid=Mqqu7GA7Pb3AwM&vet=12ahUKEwiFm8_58cqCAxX2ADQIHSvPD6IQMygJegQIARBb..i&imgrefurl=https%3A%2F%2Fblog.adobe.com%2Fen%2Fpublish%2F2021%2F08%2F31%2Famazon-web-services-works-with-adobe-experience-cloud-as-it-reimagines-b2b-marketing&docid=1jyf6kaXYeNvoM&w=750&h=422&q=amazon%20cloud%20logo&hl=fr&ved=2ahUKEwiFm8_58cqCAxX2ADQIHSvPD6IQMygJegQIARBb",
                "image": "data:image/jpeg;base64,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"
            },
        ]
    },
    {
        "category": "Hackathons",
        "activities": [
            {
                "activity": "Hunter Hub Sustainability Challenge 2023",
                "description": "The Hunter Hub Sustainability Challenge 2023 is an exciting competition hosted by Hunter Hub for Entrepreneurial Thinking, inviting participants to devise inventive and sustainable solutions for contemporary environmental challenges. This event provides a platform for creative minds to collaboratively explore entrepreneurial approaches that contribute to a more sustainable and environmentally conscious future.",
                "link": "https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.ucalgary.ca%2Fhunter-hub%2Flearn-entrepreneurial-thinking%2Fchallenges-hackathons%2Fsustainable-campus&psig=AOvVaw163FzC0iFk2k7pJojBp6-q&ust=1700304152606000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCIiq-dnsyoIDFQAAAAAdAAAAABAE",
                "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAbwAAABxCAMAAACZb+YzAAAA/FBMVEX///8AAAD/nwD8/Pz/oADsAGu/v7/sAGn5+fng4OD/nQCSkpLsAGw6OjotLS1BQUHW1tadnZ3n5+empqaGhoZnZ2fx8fHt7e0kJCRwcHA0NDRNTU3Ly8uvr69QUFD/pADtAHJ7e3vHx8dZWVlFRUW5ubkcHByYmJhra2uFhYX/+/T/8t/+8/leXl4TExP/9+n/7NHzean3ocL+7/b4qsj5vNP95e/71OT6xtv/58b/05j/xXfwOIjwRo/uG3rrAGHyYpz2k7r/1p//zon/vmT/4bf/sDv/qyH/4bn/x3z/uFH1k7bvK4P6v9jxUpH1ibLzb6P83On/wWb/sjPu3Nu5AAAT+klEQVR4nO1diVbiOhhuS2uhVGURBAUBFXEBtxFUVEQUUK6jo/P+73LTJXtKi4LinH7nzGibNEnzNcm/JUqSP+qti7PT/04snJ41z+uRAM+EmAO0mic3ZV3XMHS90707//XdDQvhg7e7a1M3Lb5uy8/XN93r60751mZS77ychfzNL+pnz7pmambn5fT3G74dOW/+d1PWQIrWvfi+1oUYg1+v1pgzX07fRKn187sbwJ/+fFb/6oaF8EP9tWxRc9oak+ftrqObeufsyxoVIhDOLOpu/CfF5jUYnc/h5DlHaN0ASm7OA+W9AHlvu6HoMi84M02t0wycvfmsmeVw7pwP/AFD6WQSNbz+emvq3Vk1J0Rw/ALjqDPpIvb2rGnP42SbEF+Bt46pv0wu/UdOdLMcbJEMMStY3J186MmzW9MMvk6GmD7eyqb+3wefvTDN21Bn+D60AHenH376vNydXlNCTIj6s6nfjUmP1AHGpLdCT9H34cXUXz2SWs3Xm07ZQue6exbOjnOHO93sChPe7p5vdceR57j1QMZmaI+eJ5zrZkc07/1+sfxCeqd7cnfabJ6+nryUwQ29/BrqdfMDoCQInD8XluX59uWMXM+iF/91LG/RSTj65gQnmkDQrHdvTb3zn4Ck8z9l09Q+IJpuba3iX7Pg//xWzL1ObO2B/1cbmSjMUWzEJSmD0ShIsQb8PSFJSfuikkzh8qNbeVhBdiVuVRCPowriafB/LG4juSr9K3gzzRvu5u+OaZZPPWTI1olu6i8Tz52ynMK/Wv23Iyfc6wV5G/wfk+UMzBGXG1Y2jKqUQL8vSNIu/D2Jys/KMuRq1alLlgvujaJdQYF/6Ieja2rcpHkHlrY/Y5w952BKLU8qeXLk5Qjy1iWbPLnm3qlZPBYtLMl71o+YRR74mazVrPGUl7er4GJRljdhodGx5G1IFnk76WIxvWHT/y/gQjc5qxgYWX4GL4veCZ1BgciDXNTQIFyGtwB5uLC8m74h78JbQchbsieTXbu6fwBAxWOHGOCuIwxfIfG7PKlNLAh5GSeFIC+yDIeJkDyHFRuByLMXVTACo9I/gHN+4IFBdR3AP/5WntCOHYS81W150b4TlLzkR8hbkHP/BHl/TI0hqgmWs0CawKQBEEHIy6ZkuWLdCUgeeGQF3iLIA7JLVPKcNqPLTh0/Hb9M8w99p6WZ5dko4daKdrhmw5s8SyK0pHoxedazSxsWAXm7qJws57KwfEDeklP82pLDM0/eYaPR2JLl5X/CFnumaczC9WJqv2dTFyn4e5MHaLNui8mzYU95efdiFyt6UaoCp0aWPBdLxdm84tfixXymb5zp2sdcsv4AAnrCQWwceVLDmvPE5DmPWxd5eSu2i8mxAMiruhVsepGXK4DUQsVSG388WmWN9ibUO2Iz5zQgWPOgjoaUdIu86Bq4CrTmrRNF2uTBX7Ne5DmqghQni/qpAOOMDj851XWRgvd20Ww23z4ZosmRt0io5MTIs37Gk0HIyy7Ja1hsJMhbheTB6TEu5yUsbUqpf4G8E7NM3+iw0yhA6/XZ1C2fUOdzu0s48laQrrwoxyVMnlSV5e1A0iZ4Ygvd4snLWzY2Gzv2d4LIi/0D5EWeGT/eb37gRV510zTdf/r1J+LEOPLA979nX644Qj4iT9qT5WCqQkHGUj9P3iYcentO3YA8J32L4Pynoq5rtImra3YY7bX1rJX1zsnF+dt586SjfSbShSPPEiwX4+n4omspxuSB3hWSV7GRT5AWFjT38uRZMmmmuJDedtQPy7KSBFhZwxrhz8WFrlMTYb3MmltalncB7eWqn+qfiBMjegwawZKu6G53LUle9hCOjcgSqyq4XgV3RlxBkmOWJ0+qUBVswgJ2SCn1h+JMu6VsKecaTaYVmESbyt46XrEu/kins/hXd4Bn05WtSjELL4po3MfSUBKtplMo2UI6nQQfwUISpheTbmHRJPL04F9j8Y31Lej1SyXTNpAj4ifjP61DXb9qHVqiPNHMG1pzYAxn+zNpV4gA+KO9UNddxi3b0srlsfpBr3Q0/VaFCIQbjTJs1q8Z68qrj3xybKilcOx9E55p+8qvDsNVuVweX0BPUf+G7H0PnjUqTLpVprW8t1vTTzxpG8rD1JsVIgjKDHk67WIQqOwc3g3jftrNChEEPuQ1Nd3fszdQjcspNytEEHR8yfO3RR8NQ6HlW8AILC2T1tGbuiiSmsWjoVxNt1khguCGkTZZgYU1fYpxpYQT5zegq3XJyzozEiWNDXARo6QOp9emEAHxql1T1y+MxeWPaYoWPdaq0jeM3nQbFsIfZ5pJXZ9odAzE+S0fTQ00c+OAuTNQS9NuWgg//NZvKV3gQjdpCaXLiDAWDgxVZcbepWK0Z9A8GtHVrI3VT8fYRBLFhW/YKBSFCP7AuNQWo4W32K1brbIgALevqANGORipw5mrC1XojPusH3UhZ5VS+fLQzdphzsLORtCaM0vrFpbjwtQIo6VLN+xur4tbQRBnm1MOHg2jH7BFH8bClMiD5Xx5IETcrThwxO+G+0BenNw1aYnljNPshFr6g2I80neG6ihgiz6MKZGHQ3PTU2pYUExM3tZ48u40WpysB1YOGAmlZ3BSzLQxJfLQ7GuHin4lpk3em6bRpucTM4A5E0gorDl631BmLbJMibw4Ik/+4lVv2uRxsX+tgEPvgZU4RzNX1KdEXg1xd/jDyQOaXZmNWmF3nghxoCr00APz5owjIj5AHnz7BnEPbTbBW2q/CFMn71xjNif/KpvXQQpnlYMjZdby5gfIy7hPZMiby7CchNdjM8LUyZM6Jm0R89wmxMgjl4xysD+YtUt9WuSt5pybX34ixMTkrfmRB5QDJoK9Kzwp4N44pm+UVJqsK2XGi960yJMiK2u53MZXj7sPkLfkR17EZI8dq3cENrEjLk7sXqFv9I3SbJWFqZEn+RmeZoTpkye9aqxe/mYKnAl9Q3mnboB5k/LiHSvs2Jwypknet2AG5NXL7KonXZiCvUDvqkKPLJXW7I5Kwf1CEds+6/kOEaH5dvbkRcY1CufxyhIBGPeoN3kez/mTJ93xyoHoMAigHDxRNwYKbREbMuleSKUzjsiwk0kLbPvZ9K7d6MOtOM0SQ16hlrSRRi9edG7UrH0pq3bqIuyutJOSoB6k603EG1a9a7tJutpo1UVKkmIrIM/hWoY/vCy7uZcBK2luvZJOsWkQYvJiyfxybq2xYrUt5sLdu0GQFymsNDY2GpWFLF0mWOOegykHdHztEyOhBBM3sxWZxEpkXPIGuZmHIQ8q2/hEFfiu1oa9hCxCmnxwiRzb1UUiG1VtCt6tRjM4yx7V7mzlkHi84TE1iMiLbaHH1mPoyIUk/UJ5aRMKnvIh02NNXQuy9aen0EaVtmJQ6aMg5BXIt7SwQ71plUklZwyGPLg7DO9rhv1vHcwSgLxF3AvZdbZaTCwiL71D5sgRQ2CTeRrtGKQhIC9JPVaEb+BOCuhrrJG5DuntaS8mqy6IACQUSiLpGQY1Et+VgW8ZMUGPEuzF+dRF1I2zI6/A51xCE2OKT3Ry8A3D2BO9PE/enkfZDHnsB0+dZPGrHOQIiGNGvOwzBrEg5C2xzbQ6EaWuiF5kGX7iMyNPwB3oMMieF3loUhBmEJ3zwpEnfF/UTnFv2aDGXtPrjGkSrG5wyZB3b/iSJ/hGZfwhFcUtXWcfnjJ5HuzAtdSTPGheq4jSREZvljxujaDbOYY8mRKYTjTP090R+owix468K/+Rh1b8jepmEdkYXb+aaEq14UYBzIi8yJowKxpZ3uQ5GaI59B7xWgMlCg7pYchb9SzYnzw6CuDG//TMd8YL1FMmXvOgX9/ZML5NXeFEsJ7s5reJpjrf2UTkxZat6A8oYuTWnWAQu0cZ8tJERYvrJJPO5ESRt1XJEz0apdJtZRKNJsHJdAx55KS5ld8irkTk7TQyZNuojdlAVdfHHzm2X1Jpcu4Vhbp+V3wjIWjyFnLOKW87Njl4rOwUrLdLoYOI3Y6YiDwHcKRTWi5NXgR3SG01IkViFdyjdnaCvG27ZixVFah0Z4KAH90O//Y0ecRJaUn73Cdi1eDI2ymAt4zEcJc0qJKFcWIk2qyvnLVEB1AV0Oe1XeDWBNRpiA0kRx+6h2TOgjy88OCTriBsdRuTBxdfeGad08c4fcFH6KPJw9VAE3nqkCqYIG+dLYJZ9aTz8YfbHqis73zIGDsHzLUAiCCA3XSM1JKjaFLAChTi2u7X2ZCHmMDyIZrPbF0ZkwNNJ2iOsMcaXvPkw7y3eUViyUPrP64Y6YsseZgp9BSzpo4dd/tDlY9a6dE5GN+6AIw2u7RbRT2Plm9isUC9ZPfibMiDX/sazoCaYq9iiLxlmJ7NUcViIcUuddcznpcmDz6wRoxXOOcy5BFxm0iqE8dyuuj9JcfZ0VBlY1T6TLzYgRrAlc7LTxX3VRFR5FJMEToT8tCSt0LkgCM+Z10g8rDzdp0qlrOvyA2xr1BMHlkxFJ4Y8sjiIL/jok4vDbXUg8Lkfg/MmUMmROWBif67NBR/l5BIgmcOJyK/W8qVPBPy0Cgjz+qvuPcOrQtEHp7eaPIkSlB0kGHsxzYo8lDF5PwHO4Ehj1xLocyyLI1B21CN4dPl8cHx49UQ/D5guNtXVTpq+l4JciaLSBGPk+2WydeGdNihQr7kQcVgEvKysFBywEPybKEYG6ZROkNeVKAp5gRzp5g80lriQR5ZCCQvN66XpWNAmWKAIQf+KfyhAT3W9/oQLPYvRipwLhJEu6k5Ai5IwUYeTP/QyCPtWVCIoUeeJ3lSpMK/06LEQUweWbEHeaRgB1/JL2L4cVQyLKiDe25MAQGG1vr2SwHdeVJhj3S/WFgnX4aIC0LDwh6bHuQhI6Rg+QogsMCHSH8ttP3YBAQgD2Ra4VZz/m+miNc8Upunz9ETrXkR2He0oifC0cFjv38sCk3psTtLWMvnWKSqFWqqSdnH/Dkg5gOk1dhzmgd5yCuBxi5PHvWmNHmwHYd4nkOGats3EIg8gFgxj5UGYe/S5KH3JcaVh0uIkGloNeVj2Od2Mt+rhjgrgax7fHcCdFQklcb8WfM+krhRU7Gx09aeGPLQ6gmH6hZXANaKyImHJg99IHjooYnBpisoeQDRVBo7BvlFiSavAjNi5x96JVbPw14zZKP6xAHn79wZAmqAbUKo+/fot7HJw6aOitPVWATfoJ92wyBQsqMYY78mJg9p4GQ30+ThL8RlL4sXZTuDH3moDmdyi0Gx6ZATOGnysIcFFoxfmCVvCZaFKpNF4mww9A0maDPYBr0YUzWaAyzyCEtFbqW6UCPs1I5AxpCHbYM71VQqgV+LIA97oDeKsVjCOaKTMUzjenK1Qqywx5bjRx76At3FC9pn/MiLYBdrJZGNRmNEzZxt87C4GpGyBdzWj8fDHavcuTmjQCfpoAkpZ5lWUmimtD9aD3cesuyx0WNs6ALT6RZYN6vIJSR0xdpwVkE/8vDzcftP3cB35C3TjFeBDIHILVHrpcgltLZNhmF8+KTeg5KqMJPmgRJI1vTgx/2TWg1xKlTbWfI8ycbkRXJ0itAZ6+XPdmV43zVvGT+yvIHnXD+BRYp6u+t8/XmiYMDeMEDQM+COi9B8V9VA4dLi0eJKThFWhXAAPzKWvGhOmJ0SzhiCxWEQG1wJZCm+5HkMXX5ssJ50scMYtXMMeaI/IHdpqENfE9dxiTVR2y6HYLuas2ODWLLLglRk+uCCbr3CCEhrYYZK8QhAEn1SSP3ylzaTgsdFY4OLYfGcO/zIE9pO24aq+oQ991SVP7bjXQ0a6i7gZ5n4myS8mRC3k4+Ypie8Hd62KTGGR6/Qv7zMAsvvAVQFAXsiuzEfPcY+CGUYhrwdJpvHHplHQM1gzAS4/2CoCkfvJSd8jgHbYDrGsUg3tELMD4JwdzJUMIe+CzrujqzPizypSle7SHRPED2vwE74wu1jgrjNTbLeXAJqvmzcJjVElz19hgcDMPiePCzM+20gqpT4MTZUlQl2xWbTeDRscIHj0SpagtZWqGZuyjnnHBMi0DOBpsV4VFrfsdMPGeNDNonqs01WSfc4lHXSWB8l1OsGZdkSkAelEjw1RqpkBE5c7NGD5JFfTXQFaQyVKDLwudzDy4yUQK+wNPYMCzB1KuqVYPQd3ZcU1XjnNYL2xIfdRmPVdLJYjQnWXSs1UUwm05vcSUfCA4Sym2mQOREl0vlohGjK+rtvWefJiMdBRNmFZDxeS29y913gYqPuHSpndjMZ39ut1Yopr2gI4WNSdLNWyezGq1miKvhHJ4jLWLqSyeRrCZ9Qi6MHVVGMUvuYoGn/qDcyAHUDwdJ2qaj+0bYhvgoHVyXLHVQaXN23Hx977aeHIWBOMUaPgsyWk322G/NCTIb9/sgwDAWMQAP+HN6LBZmRQPoM8d247L3/LdkYDu77XhLJe3g2/7dinFFyH2Dcs08GdwJgiC9E+xMHAQDu2MCkEF8I6+8BfVTgeOLPTQ3xpegDQfJjhxc9AN5nfdZfiPG4VFUjYPAQiaOREs6Z34+DkqKMs2gK0S8BnT2UVeYAYAKczMS1fwWeCP+QyXzA8vQMg8fu9UuKWpr5qdIhAuJgZKjKKJjYeTkAw24ULndzhMeStSXBf/Q9AuqUcNjNG9rWjpJhe5zocmDlUUrtUFKZO+z3LGrUUVs8fR63RyDVKPFbF0LMBR5HhqEYSmnQ7pMOvYPH3gjoBqpi/A0nzDnGUX9UMhxnUGn49+/D4O+w5PqF1MHYOTXEPODo8t7e3qVYJCqK7c8rDZ48/UIh5gz7+8f9Xu/pCqDd618ehSLKfOF/bQPbPbNMWfkAAAAASUVORK5CYII="
            },
            {
                "activity": "Hack the Change 2022",
                "description": "Hack the Change 2022 is an engaging hackathon that encourages participants to collaboratively develop innovative solutions for meaningful social impact. It serves as a platform for diverse talents to come together, hack, and contribute to positive change in addressing real-world challenges.",
                "link": "https://hack-the-change-2022.devpost.com/?ref_feature=challenge&ref_medium=discover",
                "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSQLnNCz0N7zdcro8DrYU1saU8r0EW4SgwRrA&usqp=CAU"
            },
            {
                "activity": "Calgary Hacks 2023",
                "description": "Calgary Hacks 2023 is a dynamic hackathon event that invites participants to showcase their creativity and problem-solving skills. It provides a vibrant space for individuals to collaborate, innovate, and bring new ideas to life in the realm of technology and beyond.",
                "link": "https://www.google.com/url?sa=i&url=https%3A%2F%2Fcalgaryhacks-2023.devpost.com%2F&psig=AOvVaw3Q876feZGY0UnFoPFEGCD2&ust=1700304444084000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCLD19-TtyoIDFQAAAAAdAAAAABAE",
                "image": "https://d112y698adiu2z.cloudfront.net/photos/production/challenge_photos/002/341/125/datas/full_width.png"
            },
            {
                "activity": "MIT Policy Hackathon",
                "description": "MIT Policy Hackathon is a stimulating event that challenges participants to address complex policy issues using innovative and interdisciplinary approaches. It offers a unique platform for individuals to merge policy expertise with technological solutions, fostering a collaborative environment for impactful problem-solving.",
                "link": "https://www.mitpolicyhackathon.org/",
                "image": "data:image/png;base64,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"
            },
            {
                "activity": "Innovation Amazon Hackathon",
                "description": "The Innovation Amazon Hackathon offers participants a unique opportunity to demonstrate their problem-solving skills and innovation within the framework of Amazon. It encourages creativity and collaboration, fostering an environment for participants to showcase their entrepreneurial spirit and technical expertise.",
                "link": "https://www.google.com/url?sa=i&url=https%3A%2F%2Fchallengerocket.com%2Famazon-challenge&psig=AOvVaw1I-lG6DSBRKygjfHNeoMhc&ust=1700304308036000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCNDa_aPtyoIDFQAAAAAdAAAAABAE",
                "image": "https://challengerocket.com/photo_main_big/files/company/195/2020/11/37f54fc831699d97.svg"
            },
            {
                "activity": "VTHacks IX",
                "description": "VTHacks IX provides a platform for participants to unleash their creativity and coding prowess in a competitive and collaborative environment. This hackathon fosters innovation and problem-solving, offering a space for participants to bring their project ideas to life",
                "link": "https://www.google.com/url?sa=i&url=https%3A%2F%2Fm.facebook.com%2Fvthacks%2F&psig=AOvVaw36DiIfooAv73PCpqpyk_T2&ust=1700304540890000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCKiP_5LuyoIDFQAAAAAdAAAAABAE",
                "image": "data:image/png;base64,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"
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

#print(get_all_resources('zeeshan')[1])