import robo_tools

def analyzeVisualMessage(message, play_mode):
    OUT_OF_RANGE = 999
    time = int(robo_tools.getParam(message, "see", 1))
    if time < 1:
        return
    d_neck = robo_tools.getNeckDir(message)
    if d_neck == OUT_OF_RANGE:
        return
    if robo_tools.checkInitialMode(play_mode):
        d_x = self.m_dKickOffX
        d_y = self.m_dKickOffY

    pos = self.estimatePosition(message, d_neck, d_x, d_y)
    d_x = pos["x"]
    d_y = pos["y"]
    if message.find("(b)") == -1:
        return
    ball_dist = robo_tools.getParam(message, "(b)", 1)
    ball_dir = robo_tools.getParam(message, "(b)", 2)
    rad = math.radians(robo_tools.normalizeAngle(d_neck + ball_dir))
    d_ball_x = d_x + ball_dist * math.cos(rad)
    d_ball_y = d_y + ball_dist * math.sin(rad)

    result = {"neck":d_neck, "x":d_x, "y":d_y, "ball_x":d_ball_x, "ball_y", d_ball_y}
