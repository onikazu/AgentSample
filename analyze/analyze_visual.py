import analyze.robo_tools

def analyzeVisualMessage(message, play_mode, dKickOffX, dKickOffY):
    OUT_OF_RANGE = 999
    time = int(analyze.robo_tools.getParam(message, "see", 1))
    if time < 1:
        return
    d_neck = analyze.robo_tools.getNeckDir(message)
    if d_neck == OUT_OF_RANGE:
        return
    if analyze.robo_tools.checkInitialMode(play_mode):
        d_x = dKickOffX
        d_y = dKickOffY

    pos = analyze.robo_tools.estimatePosition(message, d_neck, d_x, d_y)
    d_x = pos["x"]
    d_y = pos["y"]
    if message.find("(b)") == -1:
        return
    ball_dist = analyze.robo_tools.getParam(message, "(b)", 1)
    ball_dir = analyze.robo_tools.getParam(message, "(b)", 2)
    rad = math.radians(analyze.robo_tools.normalizeAngle(d_neck + ball_dir))
    d_ball_x = d_x + ball_dist * math.cos(rad)
    d_ball_y = d_y + ball_dist * math.sin(rad)

    result = {"neck":d_neck, "x":d_x, "y":d_y, "ball_x":d_ball_x, "ball_y":d_ball_y}
