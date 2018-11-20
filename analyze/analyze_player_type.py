def analyzePlayerType(message):
    # print("m_strPlayerType: ", self.m_strPlayerType)
    # print(message)
    id = int(robo_tools.getParam(message, "id", 1))
    # print("id: ", id)
    result = {"id":id, "message":message}
    return result
