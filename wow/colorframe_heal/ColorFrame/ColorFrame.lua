--[[
颜色1, 十进制(228, 142, 76), 十六进制(E48E4C)
颜色2, 十进制(102, 205, 170), 十六进制(66CDAA)
颜色3, 十进制(255, 182, 193), 十六进制(FFB6C1)
颜色4, 十进制(123, 104, 238), 十六进制(7B68EE)
颜色5, 十进制(240, 128, 128), 十六进制(F08080)
颜色6, 十进制(173, 216, 230), 十六进制(A9DCE6)
颜色7, 十进制(32, 178, 170), 十六进制(20B2AA)
颜色8, 十进制(0, 255, 127), 十六进制(00FF7F)
颜色9, 十进制(255, 255, 0), 十六进制(FFFF00)
颜色10, 十进制(135, 206, 250), 十六进制(87CEFA)
颜色11, 十进制(255, 99, 71), 十六进制(FF6347)
颜色12, 十进制(144, 238, 144), 十六进制(90EE90)
颜色13, 十进制(238, 130, 238), 十六进制(EE82EE)
颜色14, 十进制(255, 69, 0), 十六进制(FF4500)
颜色15, 十进制(0, 191, 255), 十六进制(00BFFF)
颜色16, 十进制(221, 160, 221), 十六进制(DDA0DD)
颜色17, 十进制(152, 251, 152), 十六进制(98FB98)
颜色18, 十进制(255, 20, 147), 十六进制(FF1493)
颜色19, 十进制(72, 61, 139), 十六进制(483D8B)
颜色20, 十进制(175, 238, 238), 十六进制(AFEEEE)
颜色21, 十进制(139, 69, 19), 十六进制(8B4513)
颜色22, 十进制(244, 164, 96), 十六进制(F4A460)
颜色23, 十进制(255, 105, 180), 十六进制(FF69B4)
颜色24, 十进制(0, 255, 255), 十六进制(00FFFF)
颜色25, 十进制(60, 179, 113), 十六进制(3CB371)
颜色26, 十进制(210, 105, 30), 十六进制(D2691E)
颜色27, 十进制(124, 252, 0), 十六进制(7CFC00)
颜色28, 十进制(255, 228, 181), 十六进制(FFE4B5)
颜色29, 十进制(147, 112, 219), 十六进制(9370DB)
颜色30, 十进制(255, 222, 173), 十六进制(FFDEAD)
颜色31, 十进制(50, 205, 50), 十六进制(32CD32)
颜色32, 十进制(255, 127, 80), 十六进制(FF7F50)
颜色33, 十进制(219, 112, 147), 十六进制(DB7093)
颜色34, 十进制(64, 224, 208), 十六进制(40E0D0)
颜色35, 十进制(255, 215, 0), 十六进制(FFD700)
颜色36, 十进制(210, 180, 140), 十六进制(D2B48C)
颜色37, 十进制(238, 232, 170), 十六进制(EEE8AA)
颜色38, 十进制(255, 165, 0), 十六进制(FFA500)
颜色39, 十进制(154, 205, 50), 十六进制(9ACD32)
颜色40, 十进制(255, 240, 245), 十六进制(FFF0F5)
颜色41, 十进制(144, 238, 144), 十六进制(90EE90)
颜色42, 十进制(95, 158, 160), 十六进制(5F9EA0)
颜色43, 十进制(128, 128, 128), 十六进制(808080)
颜色44, 十进制(0, 0, 128), 十六进制(000080)
颜色45, 十进制(173, 216, 230), 十六进制(A9DCE6)
颜色46, 十进制(105, 105, 105), 十六进制(696969)
颜色47, 十进制(255, 0, 255), 十六进制(FF00FF)
颜色48, 十进制(255, 250, 250), 十六进制(FFFAFA)
颜色49, 十进制(255, 235, 205), 十六进制(FFEBED)
颜色50, 十进制(70, 130, 180), 十六进制(4682B4)
]]
-- 定义颜色对应表
local colortable = {
    player = { 228, 142, 76 },
    party1 = { 102, 205, 170 },
    party2 = { 255, 182, 193 },
    party3 = { 123, 104, 238 },
    party4 = { 240, 128, 128 },
}


-- 创建主框体
local frame = CreateFrame("Frame", "ColorFrame", UIParent, "BackdropTemplate")
frame:SetSize(160, 50)  -- 设置框体大小
frame:SetPoint("TOPLEFT", UIParent, "TOPLEFT", 235, -25)  -- 设置框体初始位置为(200, -200) 相对左上角

-- 设置框体背景为实心颜色
frame.texture = frame:CreateTexture(nil, "BACKGROUND")
frame.texture:SetAllPoints(true)
frame.texture:SetColorTexture(0, 0, 0, 1)  -- 实心黑色背景

-- 创建显示文本
--local text = frame:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
--text:SetPoint("CENTER", frame, "CENTER")
--text:SetTextColor(1, 1, 1)  -- 设置文本颜色为白色 (RGB: 1, 1, 1)

-- 注册事件以在玩家登录后立即显示框体
frame:RegisterEvent("PLAYER_LOGIN")
frame:SetScript("OnEvent", function(self, event, ...)
    if event == "PLAYER_LOGIN" then
        frame:Show()
    end
end)

-- 使框体可拖动
frame:SetMovable(true)
frame:EnableMouse(true)
frame:RegisterForDrag("LeftButton")
frame:SetScript("OnDragStart", function(self)
    self:StartMoving()
end)
frame:SetScript("OnDragStop", function(self)
    self:StopMovingOrSizing()
end)

--注册命令行/cfset
--用命令行/cfset给frame设置颜色SetColorTexture, 入参是3个数字
SLASH_CFSET1 = "/cfset"
SlashCmdList["CFSET"] = function(args)
    local r, g, b = string.match(args, "(%d+) (%d+) (%d+)")
    print(r, g, b)
    if r and g and b then
        print('enter')
        frame.texture:SetColorTexture(r / 255, g / 255, b / 255, 1)
    else
        print("Usage: /cfset <r> <g> <b>")
    end
end

local ticker -- 用于存储定时器对象
local timerInterval = 1 -- 每2秒执行一次

--命令行,/cfon, 打印小队所有人的名字
SLASH_CFO1 = "/cfon"
SlashCmdList["CFO"] = function(args)
    -- 创建定时器，并保存到ticker变量中
    ticker = C_Timer.NewTicker(timerInterval, function()
        local status, err = pcall(setColor)
        if not status then
            print('error' .. err)
        end
    end)
end

-- 命令行 /cfoff ,关闭timer
SLASH_CFOFF1 = "/cfoff"
SlashCmdList["CFOFF"] = function(args)
    print("cf off")
    if ticker then
        ticker:Cancel()
        ticker = nil
    end
end

function setColor()
    if not IsInGroup() and not IsInRaid() then
        --print('not in group or raid')
        return
    end
    local groupNum = GetNumGroupMembers()
    local allhealth = {}
    local allhealthi = 1

    local playername = UnitName("player")
    local playerhealth = UnitHealth("player")
    local playermaxhealth = UnitHealthMax("player")
    local playerpercent = playerhealth / playermaxhealth
    --用insert控制数组自增, 不能用[x]的方式, 会丢失自增
    table.insert(allhealth, allhealthi, {
        key = 'player',
        name = playername,
        percent = playerpercent
    })
    allhealthi = allhealthi + 1

    for i = 1, groupNum - 1 do
        local unit = "party" .. i
        local name = UnitName(unit)
        local health = UnitHealth(unit)
        local maxHealth = UnitHealthMax(unit)
        local percent = health / maxHealth

        -- 没有死亡
        if not UnitIsDead(unit) then
            table.insert(allhealth, allhealthi, {
                key = unit,
                name = name,
                percent = percent
            })
            allhealthi = allhealthi + 1
        end
    end

    --for k, v in pairs(allhealth) do
    --    print(k, v.key, v.name, v.percent)
    --end

    local not_heal = true
    for k, v in pairs(allhealth) do
        if v.percent < 0.9 then
            not_heal = false
            break
        end
    end

    if not_heal then
        print('notheal')
        frame.texture:SetColorTexture(0, 0, 0, 1)
        return
    end

    local minHealth = { percent = 1 }
    for k, v in pairs(allhealth) do
        if v.percent < minHealth.percent then
            minHealth = v
        end
    end

    local minHealthKey = minHealth.key
    --print(minHealthKey, allhealth[1].name)
    local r = colortable[minHealthKey][1]
    local g = colortable[minHealthKey][2]
    local b = colortable[minHealthKey][3]
    --print('rgb=', r, g, b)

    frame.texture:SetColorTexture(r / 255, g / 255, b / 255, 1)

end
