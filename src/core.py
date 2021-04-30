# coding: utf-8
# vitorgamer58
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
import requests
import os
from conf.settings import BASE_API_URL, TELEGRAM_TOKEN, BISCOINT, PHOEMUR
import logging
import math

logger = logging.getLogger()
logger.setLevel(logging.INFO)


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')



def start(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Olá, eu sou um robô, meus comandos são:"
        "\n"
        "/price + Código da ação (Responde com o valor da ação)"
        "\n"
        "/bitcoin (responde com a cotação do bitcoin na biscoint)"
        "\n"
        "/fundamentus + Código da ação (Responde com o valor da ação)"
        "\n"
        "/graham + Código da ação (Responde com o preço justo segundo a fórmula de Graham)"
    )

def verificaprice(bot, update, args):
    #Verifica se o usuário passou o ticker da ação como argumento.
    if len(args) == 0:
        bot.send_message(
            chat_id=update.message.chat.id,
            text="Você precisa informar o ticket da ação")
    else:
        funpricestock(bot, update, args)

def funpricestock(bot, update, args):
    ticker = args[0].upper()
    busca = BASE_API_URL + "stocks/" + ticker
    json = requests.get(busca)

    if(json.status_code == 200):
        json = json.json()
        priceaction = json['lastPrice']
        changeaction = json['change']
        symbol = json['symbol']

        if priceaction == 0:
            bot.send_message(
                chat_id=update.message.chat_id,
                text=f"Código {ticker} não encontrado, tem certeza que está correto?")
        else:
            bot.send_message(
                chat_id=update.message.chat_id,
                text=f"O preço da ação {symbol} é: R$ {priceaction} sendo a variação no dia de {changeaction}%")

        string_log = f"{ticker}, {priceaction}"
        logging.info(string_log)

    else:

        if(json.status_code == 404):
            bot.send_message(
                chat_id=update.message.chat_id,
                text=f"Código {args[0]} não encontrado, tem certeza que está correto?")
        else:
            bot.send_message(
                chat_id=update.message.chat_id,
                text="O servidor das cotações está indisponível no momento")


def funbitcoin(bot, update):
    buscabtc = BISCOINT
    jsonbtc = requests.get(buscabtc)
    if(jsonbtc.status_code == 200):
        jsonbtc = jsonbtc.json()
        pricebtc = jsonbtc['data']['last']
        bot.send_message(
            chat_id=update.message.chat_id,
            text=f"O preço do Bitcoin é R$ {pricebtc}")
    else:
        bot.send_message(
            chat_id=update.message.chat_id,
            text="Sistema temporariamente indisponível")


def verificafundamentus(bot, update, args):
    if len(args) == 0:
        bot.send_message(
            chat_id=update.message.chat.id,
            text="Você precisa informar o ticket da ação")
    else:
        fundamentus(bot, update, args)


def fundamentus(bot, update, args):
    busca = PHOEMUR
    ticker = args[0].upper()
    busca1 = requests.get(busca)
    busca1 = busca1.json()
    cotacao = busca1[ticker]['Cotacao']
    # função ROUND faz com que o numero só tenha 2 casas decimais
    DY = round(((busca1[ticker]['DY'])*100), 2)
    div_brut_pat = round(((busca1[ticker]['Div.Brut/Pat.'])*100), 2)
    ev_ebit = busca1[ticker]['EV/EBIT']
    ev_ebitda = busca1[ticker]['EV/EBITDA']
    liq_corrente = busca1[ticker]['Liq.Corr.']
    mrg_ebit = round(((busca1[ticker]['Mrg.Ebit'])*100), 2)
    mrg_liq = round(((busca1[ticker]['Mrg.Liq.'])*100), 2)
    p_acl = busca1[ticker]['P/ACL']
    p_ativos = busca1[ticker]['P/Ativo']
    p_cap_giro = busca1[ticker]['P/Cap.Giro']
    p_ebit = busca1[ticker]['P/EBIT']
    p_l = busca1[ticker]['P/L']
    p_vp = busca1[ticker]['P/VP']
    psr = busca1[ticker]['PSR']
    roe = round(((busca1[ticker]['ROE'])*100), 2)
    roic = round(((busca1[ticker]['ROIC'])*100), 2)
    bot.send_message(
        chat_id=update.message.chat_id,
        text=f"FUNDAMENTUS {ticker}"
        "\n"
        f"Cotação no Fundamentus: {cotacao}"
        "\n"
        f"Dividend Yield: {DY}%"
        "\n"
        f"Dívida bruta / Patrimônio Líquido: {div_brut_pat}%"
        "\n"
        f"Margem EBIT: {mrg_ebit}%"
        "\n"
        f"Margem líquida: {mrg_liq}%"
        "\n"
        f"Valor da firma / EBIT: {ev_ebit}"
        "\n"
        f"Valor da firma / EBITDA: {ev_ebitda}"
        "\n"
        f"Liquidez corrente: {liq_corrente}"
        "\n"
        f"Preço / Ativo circulante líquido: {p_acl}"
        "\n"
        f"Preço / Ativos: {p_ativos}"
        "\n"
        f"Preço / Capital de giro: {p_cap_giro}"
        "\n"
        f"Preço / EBIT: {p_ebit}"
        "\n"
        f"Preço / Lucro: {p_l}"
        "\n"
        f"Preço / Valor Patrimonial: {p_vp}"
        "\n"
        f"Price Sales Ratio: {psr}"
        "\n"
        f"ROE: {roe}%"
        "\n"
        f"ROIC: {roic}%"
    )


def verificagraham(bot, update, args):
    if len(args) == 0:
        bot.send_message(
            chat_id=update.message.chat.id,
            text="Você precisa informar o ticket da ação")
    else:
        graham(bot, update, args)

def grahamprice(ticker):
    busca = BASE_API_URL + "stocks/" + ticker
    json = requests.get(busca)
    json = json.json()
    price = json['lastPrice']
    return price


def graham(bot, update, args):
    ticker = args[0].upper()
    graham_url = BASE_API_URL + "stocks/indicators/" + ticker
    json = requests.get(graham_url)
    if(json.status_code == 200):
        json = json.json()
        vpa = json['bookValuePerShare']['value']
        lpa = json['earningsPerShare']['value']
        if (vpa > 0 and lpa > 0):
            graham = round(math.sqrt(22.5 * lpa * vpa), 2)
            price = grahamprice(ticker)
            desconto_agio = round(((price/graham)-1)*100, 2)

            if(desconto_agio <= 0):
                resultado = 'desconto'
            else:
                resultado = 'ágio'

            bot.send_message(
                chat_id=update.message.chat_id,
                text=f"O preço justo da ação {ticker} segundo a fórmula de Graham é: R$ {graham}"
                "\n"
                f"Com um {resultado} de {abs(desconto_agio)}%"
                "\n"
                f"Preço: {price}  VPA: {vpa}  LPA: {lpa}")
            string_log = f"{ticker}, {vpa}, {lpa}"
            logging.info(string_log)
        else:
            if(vpa < 0):
                bot.send_message(
                    chat_id=update.message.chat.id,
                    text="VPA menor que zero, não é possível calcular!"
                    "\n"
                    f"VPA: {vpa}  LPA: {lpa}")

            if(lpa < 0):
                bot.send_message(
                    chat_id=update.message.chat.id,
                    text="LPA menor que zero, não é possível calcular!"                    
                    "\n"
                    f"VPA: {vpa}  LPA: {lpa}")

            if(vpa == 0):
                bot.send_message(
                    chat_id=update.message.chat.id,
                    text=f"API mfinance está fora do ar ou o código {ticker} é inválido.")

    else:
        bot.send_message(
            chat_id=update.message.chat_id,
            text="A API mfinance está indisponível no momento por um motivo desconhecido.")


def unknown(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Não Entendi"
    )


def main():
    updater = Updater(token=TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(
        CommandHandler('start', start)
    )
    dispatcher.add_handler(
        CommandHandler('price', verificaprice, pass_args=True)
    )
    dispatcher.add_handler(
        CommandHandler('bitcoin', funbitcoin, pass_args=False)
    )
    dispatcher.add_handler(
        CommandHandler('fundamentus', verificafundamentus, pass_args=True)
    )
    dispatcher.add_handler(
        CommandHandler('graham', verificagraham, pass_args=True)
    )
    dispatcher.add_handler(
        MessageHandler(Filters.command, unknown)
    )
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    print("press CTRL + C to cancel.")
    main()
