from flask import Flask, request, session
from twilio.twiml.messaging_response import MessagingResponse

# The session object makes use of a secret key.
SECRET_KEY = 'a secret key'
app = Flask(__name__)
app.config.from_object(__name__)




@app.route("/sms", methods=['GET', 'POST'])
def whatsapp():
    """Respond with the number of text messages sent between two parties."""
    # Increment the counter
    print(request.get_data())
    message_input = request.form['Body']
    print(message_input)
    resp = MessagingResponse()
    state = session.get('state', 0)
    # counter += 1
    if state == 0:
        message ="שלום לך, שמי הוא בוטי בוט ארכיטקט המידע של ענף אגמים. אשמח לסייע לך במציאת תוצרי מיצוי מידע אנא הקלד מה ברצונך לחפש"
        session['state']=1
        resp.message(message)
    if state ==1:
        message =f"בצער רב לא הצלחתי למצוא תוצר בשם {message_input}. אנא נסה שוב"
        session['state']=1
        resp.message(message)
    

    # from_number = request.values.get('From')
    # if from_number in callers:
    #     name = callers[from_number]
    # else:
    #     name = "Friend"

    # # Build our reply
    # message = f"{name} has messaged {request.values.get('To')} {counter} times." 

    # # Put it in a TwiML response
    # resp = MessagingResponse()
    # resp.message(message)

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
