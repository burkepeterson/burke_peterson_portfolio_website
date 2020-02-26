from django.shortcuts import render, redirect
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import components
from datetime import date, timedelta
from yahoo_fin.stock_info import get_data, get_quote_table, get_day_gainers, get_day_losers, get_live_price
from finance.forms import WatchlistForm
from finance.models import Watchlist
import feedparser
from allauth.account.forms import LoginForm, SignupForm


def up_down(close, open_value):
    if open_value > close:
        put = "Down"
    elif open_value < close:
        put = "Up"
    else:
        put = "Equal"
    return put


def finance_stock(request):
    if "stock" in request.GET:
        stock = request.GET.get("stock", "AAPL").upper()
    else:
        stock = "AAPL"
    return stock


def get_stock_price_data(ticker):
    start = date.today() - timedelta(weeks=52)
    end = date.today()
    return get_data(ticker, start_date=start, end_date=end)


def create_stock_price_plot(data):
    hours_12 = 12 * 60 * 60 * 1000
    plot = figure(x_axis_type="datetime", width=1000, height=300, sizing_mode="scale_width")
    plot.grid.grid_line_alpha = 0.25
    data["Status"] = [up_down(close, open_value) for close, open_value in zip(data.close, data.open)]
    data["Center"] = abs((data.open + data.close) / 2)
    data["Height"] = abs(data.open - data.close)
    plot.segment(data.index, data.high, data.index, data.low, color="black")
    plot.rect(data.index[data.Status == "Up"], data.Center[data.Status == "Up"], hours_12,
              data.Height[data.Status == "Up"], fill_color="#FFE4C4", line_color="black")
    plot.rect(data.index[data.Status == "Down"], data.Center[data.Status == "Down"], hours_12,
              data.Height[data.Status == "Down"], fill_color="#DC143C", line_color="black")
    plot.rect(data.index[data.Status == "Equal"], data.Center[data.Status == "Equal"],
              hours_12, data.Height[data.Status == "Equal"], fill_color="black", line_color="black")
    return components(plot, CDN)


def get_stock_summary_data(stock):
    quote_table = get_quote_table(stock)
    bid = quote_table["Bid"]
    bid = bid[:bid.find("x")]
    ask = quote_table["Ask"]
    ask = ask[:ask.find("x")]
    market_cap = quote_table["Market Cap"]
    beta = quote_table["Beta (5Y Monthly)"]
    range_day = quote_table["52 Week Range"]
    estimate = quote_table["1y Target Est"]
    price = get_live_price(stock)
    price = round(price, 2)
    return bid, ask, range_day, market_cap, beta, estimate, price


def get_stock_movers(number_of):
    gainers = get_day_gainers()
    gainers = gainers.head(number_of)
    gainers = gainers[["Name", "Symbol", "% Change"]]
    gainers["type"] = "gainer"
    losers = get_day_losers()
    losers = losers.head(number_of)
    losers = losers[["Name", "Symbol", "% Change"]]
    losers["type"] = "loser"
    losers = losers.reindex(index=losers.index[::-1])
    movers = gainers.append(losers, ignore_index=True)
    movers = movers.rename(columns={"% Change": "Change"})
    return movers


def watchlist_delete(request, item_id):
    watchlist_item = Watchlist.objects.get(pk=item_id)
    watchlist_item.delete()
    return redirect(request.META.get("HTTP_REFERER", "/finance/"))


def finance_website(request):
    if request.method == "GET":
        stock = finance_stock(request)
        data = get_stock_price_data(stock)
        script, div = create_stock_price_plot(data)
        bid, ask, range_day, market_cap, beta, estimate, price = get_stock_summary_data(stock)

        movers = get_stock_movers(5)
        watchlist_list = Watchlist.objects.filter(user=request.user.id)
        url = ("https://feeds.finance.yahoo.com/rss/2.0/headline?s=" + stock + "&region=US&lang=en-US")
        feed = feedparser.parse(url)
        login_form = LoginForm()
        signup_form = SignupForm()

        context = {"stock": stock, "bid": bid, "ask": ask, "range": range_day, "market_cap": market_cap, "beta": beta,
                   "estimate": estimate, "the_script": script, "the_div": div, "movers": movers,
                   "watchlist_list": watchlist_list, "news": feed, "price": price,  "login_form": login_form,
                   "signup_form": signup_form}

        return render(request, "finance.html", context)

    else:
        form = WatchlistForm(request.POST)
        form.save()
        return redirect(request.get_full_path())
