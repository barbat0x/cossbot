from cossbot import CossBot

def main():
    bot = CossBot()
    #print(bot.get_market_price('COS_ETH'))
    #print(bot.get_market_summaries())
    #print(bot.get_market_depth('COS_ETH'))
    #print(bot.get_market_information('COS_ETH'))
    #print(bot.get_exchange_information())
    #print(bot.test_api_connection())
    #print(bot.test_connection_server_time())
    print(bot.get_account_balance())

if __name__ == "__main__":
    # execute only if run as a script
    main()