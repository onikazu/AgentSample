def analyzePhysicalMessage(message):
    i_time = int(robo_tools.getParam(message, "sense_body", 1))
    # スタミナ情報の解析
    st = message.split(" ")
    for i in range(len(st)):
        if st[i] == "(stamina":
            d_stamina = float(st[i+1])
    result = {"time":i_time, "stamina":d_stamina}
    return result
