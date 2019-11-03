def get_line_chart_json(data, title, y_label, x_label = 'Time (minutes)'):
    """
    Return a json file to produce a highcharts line chart.

    Args:
        data: A list of lists, where each entry is a list of coordinate pairs.
    """
        
    line_chart_json = {'chart':{'type':'spline'},
                       'title': {'text': title},
                       'xAxis':{'title': {'text': x_label}},
                       'yAxis':{'title': {'text': y_label}},
                       'legend': {'symbolWidth': 80},
                       'plotOptions': {},
                       'series':[]}
    i = 1                                              
    for line in data:
        temp_dict = {'data':line, 'name':f'Speaker {i}'}
        line_chart_json['series'].append(temp_dict)
        i+= 1
    
    return line_chart_json