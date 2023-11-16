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
        "Institution": "Harvard University",
        "Image": "data:image/png;base64,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",
        "Submitted": False
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
        "Submitted": False
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
        "Submitted": False
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
        "Submitted": False
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
        "Submitted": False
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
        "Submitted": False
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
print(update_scholarship_answer('zeeshan', 'Community Leadership Scholarship', 0, 'aaadsad'))
#print(application_submitted('zeeshan', 'Community Leadership Scholarship'))

# print(login('Zeeshan.chougle@ucalgary.ca', 'Zeemaan1234@'))

#print(get_all_resources('zeeshan')[1])