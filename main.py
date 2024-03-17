import os
import discord
from discord import message

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("I'm in")
    print(client.user)
    global cur_topic
    global q_index
    global current_a
    global score
    score = 0
    ques_index = 0
    cur_topic = ""
    current_ans = ""

questions = {
  "science": [
    ["What is the chemical symbol for water?", "H2O"],
    ["How many bones are in the human body?", "206"],
    ["What is the hardest natural substance on Earth?", "Diamonds"],
    ["What does DNA stand for?", "Deoxyribonucleic acid"],
    ["Roughly how long does it take for the sun's light to reach Earth?", "8 minutes"],
    ["What is the most abundant gas in the earth's atmosphere?", "Nitrogen"],
  ],
  "math": [
    ["There is a group of 10 people who are ordering pizza. If each person gets 2 slices and each pizza has 4 slices, how many pizzas should they order?", "5"],
    ["Chloe has 3 bags with the same amount of marbles in them, totaling 12 marbles. Jack has 3 bags with the same amount of marbles in them, totaling 18 marbles. How many more marbles does Jack have in each bag?", "2"],
    ["Alex drank ⅚ of a carton of milk this week. Max drank 7 times more milk than Alex. How many cartons of milk did Max drink? Write your answer as an improper fraction.", "35/6"],
    ["During PE on Monday, the students ran for ¼ of a mile. On Wednesday, they ran ½ as many miles as on Monday. How many miles did the students run in total? Write your answer as a fraction.", "3/8"],
    ["4 days a week, Katie practices martial arts for 1.5 hours. Considering a week is 7 days, what is her average practice time per day each week? Round your answer to the nearest hundredth", "0.86"],
    ["Amy walks a total of 0.9 miles to and from school each day. After 4 days, how many miles will she have walked?", "3.6"],
  ]

}

@client.event
async def on_message(message):
  global cur_topic
  global ques_index
  global current_ans
  global total
  global score

  if message.author == client.user:
    return

  if cur_topic == "" and message.content.startswith('hello'):
    await message.channel.send("Hi my name is stem bot. I am a bot that can help you learn new things and quiz you on things you have learned. Type a subject you would like to learn about. After that I will send you a question and you will have to answer it. If you get it right you will get a point. If you get it wrong you will not get any points. Let's get started!")


  #print(message)
  if message.content.startswith("science"):
    cur_topic = "science"
    ques_index = 0
    current_ans = ""
  elif message.content.startswith("math"):
    prev_topic_total = len(questions[cur_topic])
    if cur_topic != "math" and cur_topic != "":
      msg = "You were doing question on " + cur_topic + ". Your current score is " + str(score) + " out of " + str(prev_topic_total) + "\n Switching to math"
      await message.channel.send(msg)
    score = 0
    cur_topic = "math"
    ques_index = 0
    current_ans = ""

  ques = questions[cur_topic]
  total = len(ques)
  if current_ans == "":
    current_q = ques[ques_index][0]
    current_ans = ques[ques_index][1]
    await message.channel.send(current_q)
  elif current_ans.lower() == message.content.lower():
    score += 1
    msg = "Good Job. Next question..Your current score is " + str(score)
    await message.channel.send(msg)
    if ques_index < total - 1:
      ques_index += 1

    else:
      user_message = "You have finished the quiz. Your final score is "+ str(score) + " out of " + str(total)
      await message.channel.send(user_message)
      score = 0
      ques_index = 0
      current_ans = ""
      return
    current_ques = ques[ques_index][0]
    current_ans = ques[ques_index][1]
    await message.channel.send(current_ques)


  elif message.content == "skip":
    ques_index += 1
    current_ques = ques[ques_index][0]
    current_ans = ques[ques_index][1]
    await message.channel.send(current_ques)
  else:
    await message.channel.send("Sorry that is incorrect. Try again or type skip to skip the question.")

      #await message.channel.send(message.content[::-1])



my_secret = os.environ['DISCORD_BOT_SECRET']
client.run(my_secret)
