def analyzeAuralMessage(message):
    index0 = message.find(" ")
    index1 = message.find(" ", index0+1)
    index2 = message.find(" ", index1+1)
    index3 = message.find(")", index2+1)
    str_speaker = message[index1+1:index2]
    str_content = message[index2+1:index3]
    result = {"speaker":str_speaker, "content":str_content}
    return result
