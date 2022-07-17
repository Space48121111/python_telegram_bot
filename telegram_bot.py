import os
import telebot
import yfinance as yf

# emulator
# API_KEY = os.getenv('API_KEY')
API_KEY = ''

bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['greet'])
def greet(message):
    bot.reply_to(message,
    'Hey, hows it going? \nMiten menee? \nHvordan går det?')
    # bot.send_message(message.chat.id, 'Hi!')


@bot.message_handler(commands=['wall street stock'])
def get_stocks(message):
  response = ""
  stocks = ['tsla', 'amzn', 'aapl', 'nok']
  stock_data = []
  for stock in stocks:
    data = yf.download(tickers=stock, period='9d', interval='3d')
    data = data.reset_index()
    response += f"-----{stock}-----\n"
    stock_data.append([stock])
    # first column
    columns = ['stock']
    for index, row in data.iterrows():
      # fetching data from yf on close price and date
      price = round(row['Close'], 2)
      # string formatter
      format_date = row['Date'].strftime('%m-%d')
      response += f"{format_date}: {price}\n"
      stock_data[len(stock_data) - 1].append(price)
      # second and later columns
      columns.append(format_date)
    print()

  response += "\nWall Street Bets"
  # formatting position caret: begins in
  response = f"{columns[0] : <10}{columns[1] : ^10}{columns[2] : >10}\n"
  for row in stock_data:
    response += f"{row[0] : <10}{row[1] : ^10}{row[2] : >10}{row[3] : >15}\n"
  print(response)
  bot.send_message(message.chat.id, response)

def stock_request(message):
  request = message.text.split()
  if len(request) < 2 or request[0].lower() not in "price":
    return False
  else:
    return True

# without / type the command directly
@bot.message_handler(func=stock_request)
def send_price(message):
  request = message.text.split()[1]
  data = yf.download(tickers=request, period='10m', interval='2m')
  if data.size > 0:
    data = data.reset_index()
    # I 12 hour format
    data["format_date"] = data['Datetime'].dt.strftime('%m/%d %I:%M %p')
    data.set_index('format_date', inplace=True)
    print(data.to_string())
    bot.send_message(message.chat.id, data['Close'].to_string(header=False))
  else:
    bot.send_message(message.chat.id, "No data!?")

bot.polling()
