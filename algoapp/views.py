# Import necessary modules
from django.http import JsonResponse
from django.shortcuts import render
from .py_files.Fyers_algo import StockAnalysis
from .forms import StockDetailsForm
import plotly.graph_objs as go
import plotly.offline as opy
from plotly.subplots import make_subplots
from .py_files.MarketStructure import MarketStruct

def my_view(request):
    error_message = None
    form = StockDetailsForm()
    if request.method == 'POST':
        try:
            form = StockDetailsForm(request.POST)
            if form.is_valid():
                stock_details = {
                    "symbol": form.cleaned_data["symbol"],
                    "time_from": form.cleaned_data["time_from"].strftime("%Y-%m-%d"),
                    "time_to": form.cleaned_data["time_to"].strftime("%Y-%m-%d"),
                    "time_period": form.cleaned_data["time_period"],
                }
                stock_analysis = StockAnalysis(stock_details)
                dictvalue = stock_analysis.HistoryData()

                # Extract candlestick data and volume data
                candlestick_data = []
                volume_data = []
                dates = []  # List to store dates for the line chart
                open_values = [] 
                MarketStruct.AnalysMarketStruct(dictvalue["candles"])
                for item in dictvalue["candles"]:
                    if len(item) >= 5:
                        x = StockAnalysis.convertEpochToIST(item[0])
                        open_value = item[1]
                        high_value = item[2]
                        low_value = item[3]
                        close_value = item[4]
                        volume = item[5]

                        candlestick_data.append(
                            go.Candlestick(x=[x], open=[open_value], high=[high_value],
                                           low=[low_value], close=[close_value])
                        )
                        volume_data.append(volume)
                        dates.append(x)
                        open_values.append(open_value)

                # Create candlestick trace
                candlestick_trace = go.Candlestick(x=[item[0] for item in dictvalue["candles"]],
                                                   open=[item[1]
                                                         for item in dictvalue["candles"]],
                                                   high=[item[2]
                                                         for item in dictvalue["candles"]],
                                                   low=[item[3]
                                                        for item in dictvalue["candles"]],
                                                   close=[item[4] for item in dictvalue["candles"]])

                # Create volume bar trace
                volume_trace = go.Bar(x=[StockAnalysis.convertEpochToIST(item[0]) for item in dictvalue["candles"]],
                                      y=[item[5]
                                          for item in dictvalue["candles"]],
                                      name='Volume')

                # Create subplot
                fig = make_subplots(
                    rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05)
                fig.add_trace(candlestick_trace, row=1, col=1)
                fig.add_trace(volume_trace, row=2, col=1)

                # Update layout
                fig.update_layout(title='Candlestick Chart with Volume',
                                  xaxis_rangeslider_visible=False)

                # Generate HTML for the subplot
                subplot_html = opy.plot(
                    fig, auto_open=False, output_type='div')
                

                #date and open price
                open_trace = go.Scatter(x=dates, y=open_values, mode='lines', name='Open Values')

                # Create the chart layout
                layout = go.Layout(title='Daily Open Values',
                                xaxis=dict(title='Date'),
                                yaxis=dict(title='Open Value'))

                # Create the figure and generate the HTML
                fig = go.Figure(data=[open_trace], layout=layout)
                chart_html = opy.plot(fig, auto_open=False, output_type='div')

                return render(request, 'index.html', {'chart_html': chart_html})
                return render(request, 'index.html', {'subplot_html': subplot_html, 'form': form})
        except Exception as e:
            error_message = str(e)
    context = {
        'error_message': error_message,
    }
    if error_message is not None:
        return render(request, 'errors.html', context)

    else:
        form = StockDetailsForm()
        return render(request, 'form_template.html', {'form': form})

    return render(request, 'form_template.html', {'form': form})
