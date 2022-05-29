from flask import Flask, request, session
import pandas as pd
from twilio.twiml.messaging_response import MessagingResponse
from fuzzywuzzy import fuzz,process


# The session object makes use of a secret key.
SECRET_KEY = 'a secret key'
app = Flask(__name__)
app.config.from_object(__name__)

def findSimalrties(val,mass):
   return fuzz.partial_ratio(mass,val)
def defineUrl(row):
    if row['type']=='Dashboard':
        return f'https://h-f-c.maps.arcgis.com/apps/dashboards/{row[id]}'
    if row['type']=='Web Map':
        return f'https://h-f-c.maps.arcgis.com/home/webmap/viewer.html?webmap={row[id]}'
    if row['url'].isnotna():
        return row['url']
    return f'https://h-f-c.maps.arcgis.com/home/item.html?id={row[id]}'

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
        data = pd.read_csv('allData.csv')

        data['url']=data.apply(lambda row:defineUrl[row],axis=1)
        data=data[['url','title']]
        data['grade'] =data['title'].apply(lambda val: findSimalrties(val,message_input))
        data=data[data['grade']>80]
        data=data.sort_values(by=['grade'],ascending=False).head(20)
        result = data.shape[0]
        if result == 0:
            message =f"בצער רב לא הצלחתי למצוא תוצר בשם {message_input}. אנא נסה שוב"
            session['state']=1
            resp.message(message)

        elif result == 1:
            message = 'התוצר המבוקש הינו: '
            message = message + f'{data.iloc[0].title}, כתובתו'
            message = message +f'{data.iloc[0].url}'
            session['state']=0
            resp.message(message)
        else:
            options =[]
            message = 'להלן ההתאמות המובילות: \n'
            for i,val in enumerate(data['title']):
                message = message + f'{i+1} {val} \n'
            for val in data['url']:
                options.append(val)
            session['options'] =options
            session['state']=2
            resp.message(message)
    if state == 2:
        try:
            opt =int(message_input)
            if opt <=0:
                opt =1000
            message = f"{session.get('options')[opt-1]}"
            resp.message(message)
            session['state']=0
        except Exception:
            message ='עליך לבחור במספר מתוך הרשימה בהודעה הקודמת'
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
