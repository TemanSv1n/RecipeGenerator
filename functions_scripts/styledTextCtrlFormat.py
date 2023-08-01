import wx
from wx import stc

def stcf_SetBlackBg(stcf: wx.stc.StyledTextCtrl, styles_list: list):
    tvc = stcf
    styleList = styles_list

    tvc.SetCaretForeground((255, 255, 255))
    for style in styleList:
        tvc.StyleSetBackground(style, (0, 0, 0))
        tvc.StyleSetForeground(style, (255, 255, 255))
        tvc.StyleSetSize(style, tvc.StyleGetSize(style) + 4)
        
def stcf_SetJsonFormat(stcf: wx.stc.StyledTextCtrl):
    tvc = stcf

    tvc.StyleSetSpec(stc.STC_JSON_DEFAULT, "fore:#ffffff,face:%(helv)s,size:%(size)d")
    tvc.StyleSetSpec(stc.STC_JSON_NUMBER, "fore:#007F7F,size:%(size)d")
    tvc.StyleSetSpec(stc.STC_JSON_KEYWORD, "fore:#007F7F,bold,size:%(size)d")
    tvc.StyleSetSpec(stc.STC_JSON_STRING, "fore:#ffc0cb,size:%(size)d")
    tvc.StyleSetSpec(stc.STC_JSON_PROPERTYNAME, "fore:#FF5733,size:%(size)d")
    tvc.StyleSetBold(stc.STC_JSON_PROPERTYNAME, bold=True)
    tvc.StyleSetSpec(stc.STC_JSON_BLOCKCOMMENT, "fore:#008000,size:%(size)d")
    tvc.StyleSetSpec(stc.STC_JSON_LINECOMMENT, "fore:#008000,size:%(size)d")
    tvc.StyleSetSpec(stc.STC_JSON_STRINGEOL, "fore:#ffc0cb,size:%(size)d")
    tvc.StyleSetSpec(stc.STC_JSON_OPERATOR, "fore:#ffffff,size:%(size)d")
    tvc.StyleSetBold(stc.STC_JSON_OPERATOR, bold=True)
    tvc.StyleSetSize(stc.STC_JSON_OPERATOR, tvc.StyleGetSize(stc.STC_JSON_OPERATOR) + 4)
