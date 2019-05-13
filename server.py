import random
import datetime

from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = 'why would a ninja farm'

@app.route('/')
def index():
    if 'current_gold' not in session:
        session['current_gold'] = 0
    if 'activities' not in session:
        session['activities'] = []
    if 'counter' not in session:
        session['counter'] = 0
    return render_template('index.html', current_gold=session['current_gold'], activities=session['activities'])

def convert_time():
    time = datetime.datetime.now()
    month = str(time.month)
    day = str(time.day)
    year = str(time.year)
    hour = time.hour
    minutes = str(time.minute).zfill(2)
    ampm = ' am'
    if hour > 12:
        hour = (hour - 12)
        ampm = ' pm'
    time_stamp = ' (' + month + '/' + day + '/' + year + ',' + str(hour) + ':' + minutes + ampm + ') <br>'
    return time_stamp

def game_state():
    state = 'playing'
    if session['counter'] <= 15 and session['current_gold'] >= 200:
        state = 'won'
    elif session['counter'] > 15:
        state = 'lost'
    return state

@app.route('/process_money', methods=['POST'])
def process_money():
    session['counter'] += 1
    time_stamp = convert_time()
    state = game_state()
    if state == 'playing':
        if request.form['building'] == 'farm':
            gold = random.randint(10, 20)
            session['current_gold']=session['current_gold'] + gold
            session['activities'].insert(0, '<div class="green"> Earned ' + str(gold) + ' gold pieces from your farm!' + time_stamp + '</div>')
        elif request.form['building'] == 'cave':
            gold = random.randint(5, 10)
            session['current_gold']=session['current_gold'] + gold
            session['activities'].insert(0, '<div class="green"> Earned ' + str(gold) + ' gold pieces from your cave!' + time_stamp + '</div>')
        elif request.form['building'] == 'house':
            gold = random.randint(2, 5)
            session['current_gold']=session['current_gold'] + gold
            session['activities'].insert(0, '<div class="green"> Earned ' + str(gold) + ' gold pieces from your house!' + time_stamp + '</div>')
        elif request.form['building'] == 'casino':
            gold = random.randint(0, 50)
            give_take = random.randint(0, 1)
            if give_take == 0:
                session['current_gold']=session['current_gold'] - gold
                session['activities'].insert(0, '<div class="red"> Entered a casino and lost ' + str(gold) + ' gold pieces... Ouch.' + time_stamp + '</div>')
            elif give_take == 1:
                session['current_gold']=session['current_gold'] + gold
                session['activities'].insert(0, '<div class="green"> Earned ' + str(gold) + ' gold pieces from the casino!' + time_stamp + '</div>')
    elif state == 'won':
        session['current_gold'] = 0
        session['counter'] = 0
        session['activities'].clear()
        session['activities'].insert(0, '<div class="win"> You earned enough gold within 15 turns. YOU WIN!! </div>')
    elif state == 'lost':
        session['current_gold'] = 0
        session['counter'] = 0
        session['activities'].clear()
        session['activities'].insert(0, '<div class="lose"> You have not earned enough gold within 15 turns. Gold pieces have been reset to 0. </div>')
    return redirect('/')

@app.route('/clear', methods=['POST'])
def clear():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)